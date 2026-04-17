import numpy as np
import pandas as pd
from multiprocessing import Manager, Process, Lock
from .ga_ll_parameter_opt import Modeliter
from .paramgen import FFpara

def Modelopt(key, vals, shared_state, lock):
    temp_individual, temp_error, initial_input, fixed_values, fixed_indices, non_fixed_indices = Modeliter(key, vals)

    optimal_X = np.zeros(initial_input.shape[1])
    optimal_X[fixed_indices] = fixed_values.values.flatten()
    optimal_X[non_fixed_indices] = temp_individual

    with lock:
        if temp_error < shared_state.best_error:
            shared_state.best_error = temp_error
            shared_state.optimal_X = optimal_X.tolist()
            shared_state.columns = initial_input.columns.tolist()
            shared_state.nbonds = initial_input['nbonds'].values[0]
            shared_state.beadtypes = int(pd.read_csv('Boxinput.data', sep=r'\s+', header=0)['N'].values[0])

def run():
    Modelsdict = {
        'Model1': ['ForestmodelSD1', 'SubsetData1.txt'],
        #'Model2': ['ForestmodelSD2', 'SubsetData2.txt'],
        'Model3': ['ForestmodelSD3', 'SubsetData3.txt'],
        'Model5': ['ForestmodelSD5', 'SubsetData5.txt'],
        'Model7': ['ForestmodelSD7', 'SubsetData7.txt'],
        'Model8': ['ForestmodelSD8', 'SubsetData8.txt']
    }

    manager = Manager()
    shared_state = manager.Namespace()
    shared_state.best_error = 1e6
    shared_state.optimal_X = []
    shared_state.columns = []
    shared_state.nbonds = 0
    shared_state.beadtypes = 0

    lock = Lock()

    processes = []
    for key, vals in Modelsdict.items():
        p = Process(target=Modelopt, args=(key, vals, shared_state, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Save optimal_X to file
    optimal_X_df = pd.DataFrame(np.array(shared_state.optimal_X).reshape(1, -1), columns=shared_state.columns)
    optimal_X_df.to_csv('OptimalInput_LL.txt', sep=' ', header=True, index=False)

    # Call FFpara based on nbonds
    if shared_state.nbonds > 0:
        FFpara(shared_state.beadtypes, 1, 1)
    else:
        FFpara(shared_state.beadtypes, 0, 0)

if __name__ == "__main__":
    run()
