import os
import sys
import numpy as np
import pandas as pd

def run():
	df = pd.read_csv('mDPDInputTable.data', sep='\s+', header = 0)

	#constants
	Na = 6.022E23 # Avogadro Number
	kB = 1.38E-23 # Boltzmann Constant (J/K)
	atm2Pa = 1.01325E5
	gtokg = 1E-3
	kcalmol2J = 6.9477E-21 # kcal/mol to J/molecule

	Nm = df.loc[df["Parameters"] == 'Nm','Value'].values[0]
	Rhostar = df.loc[df["Parameters"] == 'Rhostar','Value'].values[0]
	Mw = df.loc[df["Parameters"] == 'Mw','Value'].values[0]
	Rho = df.loc[df["Parameters"] == 'Rho','Value'].values[0]
	P = df.loc[df["Parameters"] == 'P','Value'].values[0]
	Gamma = df.loc[df["Parameters"] == 'Gamma','Value'].values[0]
	nbonds = df.loc[df["Parameters"] == 'nbonds','Value'].values[0]
	Ebperbond = df.loc[df["Parameters"] == 'Ebperbond','Value'].values[0]
	Temp = df.loc[df["Parameters"] == 'Temp','Value'].values[0]
	Sc_solvent = df.loc[df["Parameters"] == 'Sc_solvent','Value'].values[0]
	Sc_all = df.loc[df["Parameters"] == 'Sc_all','Value'].values[0]
	Beadtypes = df.loc[df["Parameters"] == 'Beadtypes','Value'].values[0]
	Polytoss = df.loc[df["Parameters"] == 'Polytoss','Value'].values[0]
	Additives = df.loc[df["Parameters"] == 'Additives','Value'].values[0]
	Ratio = df.loc[df["Parameters"] == 'Ratio','Value'].values[0]
	Press2 = df.loc[df["Parameters"] == 'Press2','Value'].values[0]

	#Parameters in real units
	mbead = Nm*Mw*gtokg/Na
	p_SI = P*atm2Pa
	rC = np.power(Rhostar*mbead/Rho,0.3333)
	BE = nbonds*Ebperbond*kcalmol2J
	tphys = rC*np.power(mbead/kB/Temp,0.5)

	#Parameters in reduced units
	pstar = np.round(p_SI*rC*rC*rC/kB/Temp, decimals=4)
	Gammastar = np.round(Gamma*rC*rC/kB/Temp, decimals=4)
	Emol = np.round(BE/kB/Temp, decimals=2)

	Target = np.array([Gammastar, Emol, Sc_solvent, Sc_all, pstar])
	targetcolumns = ['Sigma','Emol','Sc_solvent','Sc_all','Press1']
	Target_df = pd.DataFrame(Target.reshape(1,-1), columns = targetcolumns)
	Target_df.to_csv('Target.data', sep=' ', header=True)

	Boxinput = np.array([Rhostar, Beadtypes, Ratio, nbonds, Press2, Additives, Polytoss])
	Inputcolumns = ['Rho', 'N','Ratio', 'nbonds','Press2', 'Additives', 'Polytoss']
	Boxinput_df = pd.DataFrame(Boxinput.reshape(1,-1), columns = Inputcolumns)
	Boxinput_df.to_csv('Boxinput.data', sep=' ', header=True)
