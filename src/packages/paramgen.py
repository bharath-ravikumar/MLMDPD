# paramgen.py>

import os
import sys
import numpy as np
import pandas as pd

#function

def FFpara (Ntype,toss,nbtypes):
    
    df = pd.read_csv('OptimalInput_LL.txt',sep='\s+', header=0)
    
    Brep = np.round(df['B'].values[0],decimals=2)
    gamma = np.round(df['Gamma'].values[0],decimals=2)
    rD = np.round(df['rD'].values[0],decimals=2)
    Fsrp = np.round(df['Fsrp'].values[0],decimals=1)
    Rsrp = np.round(df['Rsrp'].values[0],decimals=2)

    file3 = open("parameters.settings","w")

    for i in range(1,Ntype+1):
        file3.write('pair_coeff  '+str(i)+' '+str(i)+' mdpd/rhosum 0.75 ')
        file3.write('\n')
    if Ntype>1:
        for i in range(1,Ntype+1):
            for j in range(i+1,Ntype+1):
                file3.write('pair_coeff  '+str(i)+' '+str(j)+' mdpd/rhosum 0.75 ')
                file3.write('\n')

    for i in range(1,Ntype+1):
        Aii = np.round(df['A'+str(i)+str(i)].values[0],decimals=2)
        file3.write('pair_coeff  '+str(i)+' '+str(i)+' mdpd/diffcut '+ str(Aii)+' '+ str(Brep)+' '+ str(gamma)+' 1.0 0.75 '+ str(rD)+' 1.00 1.00')
        file3.write('\n')
    if Ntype>1:
        for i in range(1,Ntype+1):
            for j in range(i+1,Ntype+1):
                Aij = np.round(df['A'+str(i)+str(j)].values[0],decimals=2)
                file3.write('pair_coeff  '+str(i)+' '+str(j)+' mdpd/diffcut '+str(Aij)+' '+ str(Brep)+' '+str(gamma)+' 1.0 0.75 '+ str(rD)+' 1.00 1.00')
                file3.write('\n')

    if toss==1:
        file3.write('\n')
        for i in range(1,Ntype+1):
            file3.write('pair_coeff '+str(i)+' '+str(Ntype+1)+' none')
            file3.write('\n')
        file3.write('pair_coeff '+str(Ntype+1)+' '+str(Ntype+1)+' srp '+str(Fsrp)+' '+str(Rsrp))
        file3.write('\n')
        for j in range(nbtypes):
            kfene = np.round(df['kB'].values[0],decimals=1)
            file3.write('bond_coeff '+str(j+1)+' '+str(kfene)+' 1.5 1 1.0 ')
            file3.write('\n')

    else:
        file3.write('bond_coeff 1 '+str(0.0)+' 1.0 1 1.0 ')
        file3.write('\n')
        for i in range(1,Ntype+2):
            file3.write('pair_coeff '+str(i)+' '+str(Ntype+1)+' none')
            file3.write('\n')



