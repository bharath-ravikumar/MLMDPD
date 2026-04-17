

import sys
import os
import numpy as np
import pandas as pd
from .paramgen import FFpara
from .polydata import polycoords
def run(seed):

    def bondcreation(Polymol, Ntypes, Particles, nbtypes, nbonds):
        file2 = open("createbonds.settings", "w")
        polycoords(Polymol, Ntypes, Particles, nbtypes, nbonds)
        file2.write('read_data polymer.data add append offset ' + str(Ntypes-Polymol) + ' 0 0 0 0 shift 0.0 0.0 0.0')
        file2.write('\n')
        file2.write('pair_style            hybrid/overlay mdpd/rhosum mdpd/diffcut ${kBT} ${rc_a} 3854262 11 srp 0.965 * mid exclude yes')
        file2.write('\n')
        file2.write('\n')
        file2.write('\n')
        for i in range(Ntypes):
            file2.write('group   M'+str(i+1)+ '  type  '+str(i+1))
            file2.write('\n')
        file2.write('\n')
        for i in range(Ntypes):
            file2.write('set   type  '+str(i+1)+ '  mol  '+str(i+1))
            file2.write('\n')

    os.system('rm *.settings')

    df1 = pd.read_csv('Boxinput.data', sep='\s+', header = 0)
    df2 = pd.read_csv('Concentration.data', sep='\s+', header = 0)

    file1 = open("createatoms.settings","w")

    N =  int(df1['N'].values[0])
    nbonds = int(df1['nbonds'].values[0])
    p = np.zeros(N,dtype=int)
    conc = np.zeros(N)
    Ntype = N
    nbtypes = 1
    toss = 0

    xlo = 0.0
    xhi = 20.0
    ylo = 0.0
    yhi = 20.0
    zlo = 0.0
    zhi = 20.0

    # Use the provided seed argument
    # seed = int(sys.argv[1])

    ndens = df1['Rho'].values[0]
    conc[0] = df2['Comp1'].values[0]
    totatoms = int(np.round((xhi-xlo)*(yhi-ylo)*(zhi-zlo)*ndens))
    p[0] = totatoms

    if N>1:
        for i in range(1,N):
            conc[i] = df2.iloc[0,i]
        for i in range(N-1,0,-1):
            p[i] = int(conc[i]*totatoms)
            p[0] = p[0]-p[i]
        P = p
        for i in range(N):
            if p[i]==0:
                P=np.delete(p,i,0)

        Ntype = np.size(P)
        Polymol = int(df1['Additives'].values[0])

        file1.write('create_box  '+str(Ntype+1)+' mDPD bond/types '+str(nbtypes)+' extra/bond/per/atom 4 extra/special/per/atom 4')
        file1.write('\n')
        for i in range(Ntype-Polymol):
            file1.write('create_atoms   '+str(i+1)+ '  random  '+str(P[i])+'  '+str(seed)+'  base overlap 0.1 units box')
            file1.write('\n')
            seed += 1000*(i+1)

        if Polymol != 0:
            toss = int(df1['Polytoss'].values[0])
            if toss == 1:
                bondcreation(Polymol,Ntype,P,nbtypes,nbonds)
            else:
                for i in range (Ntype-Polymol,Ntype,1):
                    file1.write('create_atoms   '+str(i+1)+ '  random  '+str(P[i])+'  '+str(seed)+'  additive overlap 0.1 units box')
                    file1.write('\n')
                    seed += 1000*(i+1)
                file1.write('create_atoms   '+str(Ntype+1)+ '  random  '+str(0)+'  '+str(seed)+'  additive')
                file1.write('\n')
                file2 = open("createbonds.settings","w")
                file2.write('pair_style            hybrid/overlay mdpd/rhosum mdpd/diffcut ${kBT} ${rc_a} 3854262 11')
                file2.write('\n')
                for i in range(Ntype):
                    file2.write('group   M'+str(i+1)+ '  type  '+str(i+1))
                    file2.write('\n')
                for i in range(Ntype):
                    file2.write('set   type  '+str(i+1)+ '  mol  '+str(i+1))
                    file2.write('\n')
        else:
            file2 = open("createbonds.settings","w")
            file2.write('pair_style            hybrid/overlay mdpd/rhosum mdpd/diffcut ${kBT} ${rc_a} 3854262 11')
            file2.write('\n')
            for i in range(Ntype):
                file2.write('group   M'+str(i+1)+ '  type  '+str(i+1))
                file2.write('\n')
            for i in range(Ntype):
                file2.write('set   type  '+str(i+1)+ '  mol  '+str(i+1))
                file2.write('\n')

    else:
        file1.write('pair_style            hybrid/overlay mdpd/rhosum mdpd/diffcut ${kBT} ${rc_a} 3854262 11')
        file1.write('\n')
        file1.write('create_box  '+str(N+1)+' mDPD bond/types 1')
        file1.write('\n')
        file1.write('create_atoms   '+str(1)+ '  random  '+str(p[0])+'  '+str(seed)+'  mDPD')
        file1.write('\n')
        file1.write('group   M'+str(1)+ '  type  '+str(1))
        file1.write('\n')
        file1.write('set   type  '+str(1)+ '  mol  '+str(1))
        file1.write('\n')

        file2 = open("createbonds.settings", "w")


