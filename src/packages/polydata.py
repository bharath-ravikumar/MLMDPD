import sys
import os
import numpy as np


def polycoords(Polymol,Ntypes,P,nbtypes,Nbonds):

    xlo = ylo = 0.0
    zlo = 15.1
    xhi = yhi = zhi = 20.0

    beads = 0
    bondend = 0
    Base = Ntypes-Polymol
    for i in range(Base):
        P = np.delete(P,0,0)
    for i in range(Polymol):
        beads += P[i]
    typearrays = np.arange(Polymol)
    print(str(P)+'\n'+str(typearrays))

    file3 = open("polymer.data","w")
    file3.write("LAAMPS polymer data")
    file3.write("\n")
    file3.write("\n")
    file3.write(str(beads)+' atoms')
    file3.write("\n")
    file3.write(str(Polymol)+' atom types')
    file3.write("\n")
    chain_length = np.random.randint(5,50)
    print(str(chain_length))
    bcount = 0
    for i in range(1,beads+1,chain_length):
        remain = beads-i+1
        if remain >= chain_length:
            for j in range(chain_length-1):
                bcount += 1
        #leftover = chain_length-remain+1
                if bcount == Nbonds:
                    bondend = 1
                    break
            if bondend == 1:
                break
        #if leftover > 1 and leftover < chain_length:
        #    for j in range(remain-1):
        #        bcount += 1
    file3.write(str(bcount)+ ' bonds')
    file3.write("\n")
    file3.write(str(nbtypes)+' bond types')
    file3.write("\n")
    file3.write("\n")
    file3.write(str(xlo)+' '+ str(xhi)+ " xlo xhi")
    file3.write("\n")
    file3.write(str(ylo)+' '+ str(yhi)+ " ylo yhi")
    file3.write("\n")
    file3.write(str(zlo)+' '+ str(zhi)+ " zlo zhi")
    file3.write("\n")
    file3.write("\n")
    file3.write("Atoms # hybrid")
    file3.write("\n")
    file3.write("\n")

    gap = 0.5
    x_vals = np.arange(xlo,xhi,gap)
    y_vals = np.arange(ylo,yhi,gap)
    z_vals = np.arange(zlo,zhi,gap)

    path = []
    direction_y = 1
    direction_z = 1

    for x in x_vals:
        for y in (y_vals if direction_y == 1 else y_vals[::-1]):
            for z in (z_vals if direction_z == 1 else z_vals[::-1]):
                path.append((x,y,z))
                if len(path) >= beads:
                    break
            direction_z *=-1 # Zigzag in Z direction
        direction_y *=-1 # Zigzag in Y direction
    count = beads
    while count >0:
        assigntype = np.random.choice(typearrays)
        index = np.argmax(typearrays==assigntype)
        file3.write(str(beads-count+1)+' '+str(assigntype+1)+ ' '+'{0:.2f}'.format(path[beads-count][0])+' '+'{0:.2f}'.format(path[beads-count][1])+' '+'{0:.2f}'.format(path[beads-count][2])+' 0.0 1 0 0 0')
        file3.write("\n")
        P[index] -= 1
        count -= 1
        if P[index] == 0:
            P = np.delete(P,index,0)
            typearrays = np.delete(typearrays,index)
            
                    
    file3.write("\n")
    bnumber =1
    bondend = 0
    file3.write("Bonds")
    file3.write("\n")
    file3.write("\n")
    for i in range(1,beads+1,chain_length):
        remain = beads-i+1
        if remain >= chain_length:
            btype = np.random.randint(1,nbtypes+1)
            for j in range(chain_length-1):
                left = int(i+j)
                right = int(left+1)
                file3.write(str(bnumber)+' '+str(btype)+' '+str(left)+' '+str(right))
                file3.write('\n')
                bnumber += 1
        #leftover = chain_length-remain+1
                if bnumber == Nbonds+1:
                    bondend = 1
                    break
            if bondend == 1:
                break
        #if leftover > 1 and leftover < chain_length:
         #   btype = np.random.randint(1,nbtypes+1)
          #  for j in range(remain-1):
           #     left = int(i+j)
           #     right = int(left+1) 
           #     file3.write(str(bnumber)+' '+str(btype)+' '+str(left)+' '+str(right))
           #     file3.write('\n')
           #     bnumber += 1


