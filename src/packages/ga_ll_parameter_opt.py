import os
import numpy as np
import pandas as pd
import pickle
from deap import base, creator, tools, algorithms
import networkx as nx
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
from scipy.optimize import minimize


    #for key,vals in Modelsdict.items():
def Modeliter(key,vals):
        models_dir = os.path.join(os.path.dirname(__file__), 'Models')
        Original_data = pd.read_csv(str(models_dir)+'/'+str(key)+'/'+str(vals[1]), sep='\s+', header=0)
        r,c = Original_data.shape

        max_beads = 5

        X = Original_data[['Rho', 'Ratio', 'nbonds', 'A11', 'A12', 'A13', 'A14', 'A15', 'A22', \
                'A23', 'A24', 'A25', 'A33', 'A34', 'A35', 'A44', 'A45', 'A55', \
                'B', 'Gamma', 'rD', 'kB', 'Fsrp', 'Rsrp', \
                'Press2', \
                'Comp1', 'Comp2', 'Comp3', 'Comp4', 'Comp5']]

        Target = pd.read_csv('Target.data', sep='\s+', header=0)
        model = pickle.load(open(str(models_dir)+'/'+str(key)+'/'+str(vals[0]),'rb'))
        ytargets = 5
#target_y = np.array([5.9828, 37143.287, 737.948, 721.471, 275.219]) # Desired output values
        target_y = np.ones(ytargets)
        target_y[0] = np.multiply(Target['Sigma'].values[0] ,0.1)#np.multiply(target_y[0],0.1)
        target_y[1] = np.multiply(Target['Emol'].values[0],0.0001)
        target_y[2] = np.log10(Target['Sc_solvent'].values[0])
        target_y[3] = np.log10(Target['Sc_all'].values[0])
        target_y[4] = np.multiply(Target['Press1'].values[0],0.01)
#target_y = pd.read_csv('TargetData.txt', sep='\s+', header = 0)
#target_y[['Sc_solvent','Sc_all']] = np.log(target_y[['Sc_solvent','Sc_all']])
#target_y[['Emol']] = np.multiply(target_y[['Emol']],0.0001)
#target_y[['Sigma']] = np.multiply(target_y[['Sigma']],0.1)
        print(target_y)

        Parainput = pd.read_csv('Boxinput.data', sep='\s+', header=0)
        Beadtypes = int(Parainput['N'].values[0]) #int(Parainput.loc[Parainput["Parameters"] == 'Beadtypes','Value'].values[0])
        Conc = pd.read_csv('Concentration.data', sep='\s+', header = 0)
        Adict = dict()
        for i in range(max_beads):
            for j in range(i,max_beads,1):
                Adict.update({'A'+str(i+1)+str(j+1):0.0})

        for i in range(Beadtypes):
            Adict.update({'A'+str(i+1)+str(i+1):-50.0})
            for j in range(i,Beadtypes,1):
                Adict.update({'A'+str(i+1)+str(j+1):-50.0})
        Boxinput_values = Parainput[['Rho','Ratio','nbonds']]
        #print(Boxinput_values)
        Nonfixed_para = Original_data.loc[0,['B','Gamma','rD','kB','Fsrp','Rsrp']].to_frame().transpose()
        Adataframe=pd.DataFrame([Adict])
        Press2_values = Parainput['Press2']
        initial_input = Boxinput_values.join([Adataframe,Nonfixed_para,Press2_values,Conc])

        Afixed_columns = [key for key, val in Adict.items() if val==0.0]

        Amix_cols = []
        Adiag_cols = []
        for i in range(Beadtypes):
            for j in range(i,Beadtypes,1):
                if i != j:
                    Amix_cols = Amix_cols+['A'+str(i+1)+str(j+1)]
                else:
                    Adiag_cols = Adiag_cols+['A'+str(i+1)+str(j+1)]

        Boxinputfixed_columns = ['Rho','Ratio','nbonds']
        Presscolumns = ['Press2']
        Concfixed_columns = [*Conc]

#initial_input = pd.read_csv('initial_input.txt',sep='\s+', header= 0)
#fixed_columns = ['Rho','Ratio','nbonds','A13','A14','A15','A23','A24','A25','A33','A34','A35','A44','A45','A55','Press1','Press2','Comp1','Comp2','Comp3','Comp4','Comp5']
        fixed_columns = Boxinputfixed_columns+Afixed_columns+Presscolumns+Concfixed_columns #['Rho','Ratio','nbonds','A14','A15','A24','A25','A34','A35','A44','A45','A55','Press2','Comp1','Comp2','Comp3','Comp4','Comp5']

#fixed_columns = ['Rho','Ratio','nbonds','Comp1','Comp2','Comp3','Comp4','Comp5']
        fixed_values = initial_input[fixed_columns]
        #print(fixed_values)
        fixed_indices = [initial_input.columns.get_loc(col) for col in fixed_columns]
        non_fixed_columns = [col for col in initial_input.columns if col not in fixed_columns]
        non_fixed_indices = [initial_input.columns.get_loc(col) for col in non_fixed_columns]
        #print(non_fixed_columns)
        feature_name_to_index = {name: idx for idx, name in enumerate(non_fixed_columns)}
        #print(feature_name_to_index)

        Amixed_columns = [col for col in initial_input.columns if col in Amix_cols]
        mixed_indices = [initial_input.columns.get_loc(col) for col in Amixed_columns]
        Asimilar_columns = [col for col in initial_input.columns if col in Adiag_cols]
        similar_indices =  [initial_input.columns.get_loc(col) for col in Asimilar_columns]

        X_min, X_max = X[non_fixed_columns].min().values, X[non_fixed_columns].max().values
        feature_range = X_max-X_min # Has to be an array of Feature_Max - Feature_Min values

        def fitness_function(individual):
            full_input = np.zeros(initial_input.shape[1])
            full_input[fixed_indices] = fixed_values # Set fixed values
            full_input[non_fixed_indices] = individual # Set optimized values
            full_input  = full_input.reshape(1,-1)
            #print(full_input)
            full_input_df = pd.DataFrame(full_input,columns=initial_input.columns)
            y_pred = model.predict(full_input_df)
            #print(y_pred)
            error = np.sum((y_pred -target_y)**2)
            #print(error)
            return (error,)

        creator.create("MinimaFitness", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.MinimaFitness)

        sigma_values = feature_range * 0.1

        def random_float():
            return [np.random.uniform(X_min[i], X_max[i]) for i in range(len(non_fixed_columns))]

        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initIterate, creator.Individual, random_float)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def custom_crossover(ind1, ind2, alpha=0.5):
            for i in range(len(ind1)):
        # Blend crossover: Interpolate between two parents
                gamma = (1.0 + 2.0 * alpha) * np.random.rand() - alpha
                ind1[i] = (1.0 - gamma) * ind1[i] + gamma * ind2[i]
                ind2[i] = gamma * ind1[i] +(1.0 - gamma) * ind2[i]

        # Clip values to stay within feature range

                ind1[i] = np.clip(ind1[i], X_min[i], X_max[i])
                ind2[i] = np.clip(ind2[i], X_min[i], X_max[i])
            return ind1, ind2

        def custom_mutate(individual, indpb=0.1):
            for i in range(len(individual)):
                if np.random.rand() < indpb: # Mutation probability
                    individual[i] += np.random.normal(0, sigma_values[i])
            return individual,

        def special_mutation(edgeless, pos):
            edgeless += 0.5*np.random.normal(0,sigma_values[pos])
            edgeless = np.clip(edgeless, X_min[pos], X_max[pos])
            return edgeless

        toolbox.register("evaluate", fitness_function)
        toolbox.register("mate", custom_crossover)
        toolbox.register("mutate", custom_mutate)
        toolbox.register("select", tools.selTournament, tournsize=3)

        def build_interaction_graph(X):

   # pop_array = np.array(population)

            G = nx.Graph()
            features = X.columns.tolist()
            num_vars = len(features)

            for var in features:
                G.add_node(var)

            for i in range(num_vars):
                for j in range(i+1, num_vars):
                    mi = mutual_info_regression(X[[features[i]]], X[features[j]])[0]
                    if mi >= 0.2:
                        G.add_edge(features[i], features[j], weight = mi)

            return G

        def mate_with_linkage(ind1, ind2, linkage_graph, name_to_index, alpha = 0.7):

            child1, child2 = np.clip(ind1[:], X_min[:], X_max[:]), np.clip(ind2[:], X_min[:], X_max[:])
            #print (len(child1))
            #print (len(child2))
            for node in linkage_graph.nodes:
                if node not in name_to_index:
                    continue
                i = name_to_index[node]
                if linkage_graph.degree[node] == 0:
            #print(node)
            #child1[i],child2[i] = child2[i],child1[i]
                    child1[i] = special_mutation(child1[i],i)
                    child2[i] = special_mutation(child2[i],i)

                neighbors = list(linkage_graph.neighbors(node))
                for neighbor in neighbors:
                #if neighbor not in name_to_index:
                #    continue
                #j = name_to_index[neighbor]
                    if np.random.random() < alpha:
                        if neighbor in name_to_index:
                            weight = linkage_graph[node][neighbor].get("weight", 0.0)
                            if weight > 0.1:
                                j = name_to_index[neighbor]
                                child1[j], child2[j] = child2[j], child1[j]
                        else:
                            weight = linkage_graph[node][neighbor].get("weight", 0.0)
                            if weight > 0.1:
                                child1[i], child2[i] = child2[i], child1[i]

            return creator.Individual(child1), creator.Individual(child2)


        population_size = 500
        population = toolbox.population(n=population_size)

        NGEN = 250
        CXPB, MUTPB = 0.5, 0.2

        linkage_graph = build_interaction_graph(X)

        print("Built")

#algorithms.eaSimple(population, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=None, halloffame=None, verbose=True)
        for gen in range(NGEN):

            offspring = []
            while len(offspring) < len(population):
                ind1, ind2 = toolbox.select(population,2)
                if linkage_graph:
                    child1, child2 = mate_with_linkage(ind1, ind2, linkage_graph, feature_name_to_index)
                else:
                    child1, child2 = toolbox.mate(ind1, ind2)

                toolbox.mutate(child1)
                toolbox.mutate(child2)
                del child1.fitness.values
                del child2.fitness.values
                offspring.append(child1)
                offspring.append(child2)

            offspring = offspring[:len(population)]
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(toolbox.evaluate, invalid_ind))
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            population [:] = toolbox.select(offspring, k = len(population))

        temp_individual = tools.selBest(population, k=1)[0]
        temp_error = temp_individual.fitness.values[0]
        print(key)
        print(temp_error)

        optimal_X = np.zeros(initial_input.shape[1])
        optimal_X[fixed_indices] = fixed_values.values.flatten()
        optimal_X[non_fixed_indices] = temp_individual
        optimal_X_df = pd.DataFrame(optimal_X.reshape(1,-1), columns = initial_input.columns)
        ypred = model.predict(optimal_X_df)
        print(ypred)

        return temp_individual,temp_error,initial_input,fixed_values,fixed_indices,non_fixed_indices
