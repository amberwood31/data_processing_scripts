#!/usr/bin/python

# This is part of the Vertigo suite.
# Niko Suenderhauf
# Chemnitz University of Technology
# niko@etit.tu-chemnitz.de

## No. Not any more. I've changed too much @fwu
## fang.wu@polymtl.ca


from optparse import OptionParser
import sys
import random
from math import *
import numpy as np


# =================================================================
def checkOptions(options):
    """Make sure the options entered by the user make sense."""

    if options.outliers<0:
        print "Number of outliers (--outliers) must be >=0."
        return False
    

    if options.groupsize<0:
        print "Groupsize (--groupsize) must be >=0."
        return False

    if options.switchCov<=0.0:
        print "Switch covariance (--switchCov) must be >0."
        return False

    if options.switchable and options.maxmix:
        print "Please specify only one of --switchable or --maxmix."
        return False

    if options.filename == "" or options.filename==None:
        print "Dataset to read (--in) must be given."
        return False

    if options.information == "":
        options.information=None
    
    
    if options.information:
        if (options.information.count(",") != 0) and (options.information.count(",") != 5) and  (options.information.count(",") != 20):
            print "Information matrix must be given in full upper-triangular form. E.g. --information=42,0,0,42,0,42 or as a single value that is used for all diagonal entries, e.g. --information=42."
            return False
    


    return True
    
    
# =================================================================
def readDataset(filename, vertexStr='VERTEX_SE2', edgeStr='EDGE_SE2'):

    # read the complete file
    f = file(filename,'r')
    lines=f.readlines()


    # determine whether this is a 3D or 2D dataset
    mode=None
    
    for i in range(len(lines)):
        if lines[i].startswith("VERTEX_SE2"):
            mode=2
            break
        elif lines[i].startswith("VERTEX_SE3"):
            mode=3
            break
        
                                       
    if mode == 2:
        vertexStr='VERTEX_SE2'
        edgeStr='EDGE_SE2'               
    elif mode == 3:
        vertexStr='VERTEX_SE3:QUAT'
        edgeStr='EDGE_SE3:QUAT'
       
        


    # build a dictionary of vertices and edges
    v=[]
    e=[]
    
    for line in lines:
        if line.startswith(vertexStr):
            idx=line.split()[1]            
            v.append(line)

        elif line.startswith(edgeStr):
            idx=(line.split()[1],line.split()[2]) 
            e.append(line)

    return (v,e, mode)


# ==================================================================
def euler_to_quat(yaw,  pitch,  roll):
   sy = sin(yaw*0.5)
   cy = cos(yaw*0.5)
   sp = sin(pitch*0.5)
   cp = cos(pitch*0.5)
   sr = sin(roll*0.5)
   cr = cos(roll*0.5)
   w = cr*cp*cy + sr*sp*sy
   x = sr*cp*cy - cr*sp*sy
   y = cr*sp*cy + sr*cp*sy
   z = cr*cp*sy - sr*sp*cy

   return (w,x,y,z)

def generate_one_edge(poseCount, lc_edges, doLocal, doLinkdown):

    # determine random indices for the two vertices that are connected by an outlier edge
    v1=1    # don't use pose 0 @fwu
    v2=1    # don't use pose 0
    while v1==v2 or [v1, v2] in lc_edges: # 2nd condition makes sure that generated edge aren't already in the dataset @fwu
        v1=random.randint(1,poseCount-1-1)# don't use pose 0
        # the second -1 can be removed, but is kept to be consistent with previous version of the script
        if doLocal<1:
            v2=random.randint(1,poseCount-1-1)
        else: 
            v2=random.randint(v1,min(poseCount-1-1, v1+20)) 

        if v1>v2:
            tmp=v1
            v1=v2
            v2=tmp                       
        if v2==v1+1:
            v2=v1+2

        if doLinkdown:
            tmp=v1
            v1=v2
            v2=tmp 

    return v1, v2

def compute_and_write_one_edge(v1, v2, f, mode, edgeStr, perfectMatch, poseCount, switchCount, switchPrior, switchInfo, maxmixScale, maxmixWeight, informationMatrix, doSwitchable, doMaxMix, doMaxMixAgarwal):


    # determine coordinates of the loop closure constraint
    if mode == 2:
        x1=random.gauss(0,3)
        x2=random.gauss(0,3)
        x3=random.gauss(0,10*pi/180.0)

    if mode == 3:
        x1=random.gauss(0,3)
        x2=random.gauss(0,3)
        x3=random.gauss(0,3)
        
        
        sigma = 10.0*pi/180.0
        roll = random.gauss(0,sigma)
        pitch = random.gauss(0,sigma)
        yaw = random.gauss(0,sigma)            
        (q3, q0, q1, q2) = euler_to_quat(yaw, pitch, roll)

    if perfectMatch:
        x1=x2=x3=0
        q3=1
        q0=q1=q2=0


    info_str = informationMatrix.replace(",", " ")

    if doSwitchable:

        s=' '.join(['VERTEX_SWITCH', str(poseCount + switchCount), str(switchPrior)])
        f.write(s+'\n')

        s=' '.join(['EDGE_SWITCH_PRIOR',str(poseCount + switchCount), str(switchPrior), str(switchInfo)])
        f.write(s+'\n')

        n=[v1, v2, poseCount + switchCount, x1, x2, x3]
        if mode == 3:
            n.extend([q0, q1, q2, q3])
            
        s = ' '.join([edgeStr+'_SWITCHABLE'] + [str(x) for x in n]) + " " + info_str
        f.write(s+'\n')
        
    elif doMaxMix: 
        n=[v1, v2, maxmixScale, x1, x2, x3]
        if mode == 3:
            n.extend([q0, q1, q2, q3])
            
        s = ' '.join([edgeStr+'_MAXMIX'] + [str(x) for x in n]) + " " + info_str
        f.write(s+'\n')
    elif doMaxMixAgarwal:
        n= v1, v2, x1, x2, x3

        # edge component 1
        edge1 = ' '.join([edgeStr, "1"] + [str(x) for x in n]) + " " + info_str
    
        # edge component 2
        w = float(maxmixScale)
        weighted_info_str = [str(float(x)*w) for x in info_str.split()]        
        edge2 = ' '.join([edgeStr, str(maxmixWeight)] + [str(x) for x in n] + weighted_info_str)

        # put it together
        s =  ' '.join([edgeStr+'_MIXTURE', str(v1), str(v2), "2"]) + " " +  edge1 + " " + edge2
        f.write(s+'\n')

    else:
        n=[v1, v2, x1, x2, x3]
        if mode == 3:
            n.extend([q0, q1, q2, q3])                    
            s = ' '.join([edgeStr+":QUAT"] + [str(x) for x in n]) + " " + info_str
        else:
            s = ' '.join([edgeStr] + [str(x) for x in n]) + " " + info_str
        f.write(s+'\n')


def write_group_edges(f, outliers, groupSize, lc_edges, poseCount, switchCount, switchPrior, switchInfo, edgeStr, maxmixScale, maxmixWeight, doLocal, doLinkdown, doSwitchable, doMaxMix, doMaxMixAgarwal, perfectMatch, mode, informationMatrix):

    loop_counter = 0
    while loop_counter < outliers:
        random_group_range = random.randint(1, groupSize)
        #print("random group range:", random_group_range)

        if random_group_range == 1:

            v1, v2 = generate_one_edge(poseCount, lc_edges, doLocal, doLinkdown)

            compute_and_write_one_edge(v1, v2, f, mode, edgeStr, perfectMatch, poseCount, switchCount, switchPrior, switchInfo, maxmixScale, maxmixWeight, informationMatrix, doSwitchable, doMaxMix, doMaxMixAgarwal)

            if doSwitchable:
                switchCount = switchCount + 1
        
            lc_edges.append([v1, v2]) # append newly generated edge to the dataset, to make sure following iterations doesn't generate redundant edges 

            loop_counter += 1
        
        else: 
            # this is the number of loop closures from this specific perceptual aliasing incident
            random_group_size = random.randint(2, random_group_range)

            
            # this two are the means of two uniform distribution of grouped outliers
            v1, v2 = generate_one_edge(poseCount, lc_edges, doLocal, doLinkdown)


            counter = 0
            while counter < random_group_size:      
                
                v3 = 1
                v4 = 1
                while v3 == v4 or [v3, v4] in lc_edges:
                    v3 = random.randint(v1 - random_group_range/2, v1 + random_group_range/2)
                    v4 = v3 - v1 + v2 + random.randint(-1,1) # add a noise with std = 1

                    if v3>v4:
                        tmp=v3
                        v3=v4
                        v4=tmp                       
                    if v4==v3+1:
                        v4=v3+2

                    
                    if v3 <= 0: 
                        #if negative int value (or 0, rtabmap doesn't accept pose 0) is generated for v3, move both v3 and v4 
                        v4 = v4-v3+1
                        v3 = 1

                    if doLinkdown:
                        tmp=v3
                        v3=v4
                        v4=tmp 


                compute_and_write_one_edge(v3, v4, f, mode, edgeStr, perfectMatch, poseCount, switchCount, switchPrior, switchInfo, maxmixScale, maxmixWeight, informationMatrix, doSwitchable, doMaxMix, doMaxMixAgarwal)

                if doSwitchable:
                    switchCount = switchCount + 1
        
                lc_edges.append([v3, v4]) # append newly generated edge to the dataset, to make sure following iterations doesn't generate redundant edges 
                counter += 1

            loop_counter += random_group_size          


def write_random_edges(f, outliers, lc_edges, poseCount, switchCount, switchPrior, switchInfo, edgeStr, maxmixScale, maxmixWeight, doLocal, doLinkdown, doSwitchable, doMaxMix, doMaxMixAgarwal, perfectMatch, mode, informationMatrix):


    for i in range(outliers):        

        v1, v2 = generate_one_edge(poseCount, lc_edges, doLocal, doLinkdown)

        compute_and_write_one_edge(v1, v2, f, mode, edgeStr, perfectMatch, poseCount, switchCount, switchPrior, switchInfo, maxmixScale, maxmixWeight, informationMatrix, doSwitchable, doMaxMix, doMaxMixAgarwal)

        if doSwitchable:
            switchCount = switchCount + 1
    
        lc_edges.append([v1, v2]) # append newly generated edge to the dataset, to make sure following iterations doesn't generate redundant edges 



# ==================================================================
def writeDataset(filename, vertices, edges, mode, outliers, switchPrior, switchSigma, maxmixWeight, maxmixScale, groupSize, doLocal, informationMatrix, doSwitchable, doLinkdown, doMaxMix, doMaxMixAgarwal, perfectMatch):

    
    switchInfo=1.0/switchSigma**2
  
    # first write out all pose vertices (no need to change them)
    f = file(filename, 'w')
    for n in vertices:
        f.write(n)


    # edges and vertices are called differently, depending on 2D or 3D mode ...
    if mode == 2:
        edgeStr='EDGE_SE2'

        # check entries for information matrix for additional loop closure constraints (outliers)
        if not informationMatrix:
            print "Determining information matrix automatically..."                                      
        else:        
            if informationMatrix.count(",")==0:
                # if there is only a single value, convert it into full upper triangular form with that value on the diagonal
                try:                
                    diagEntry=float(informationMatrix)
                except:
                    print "! Invalid value for information matrix. If you give only a single value, it must be a number, e.g. --information=42"
                    return False
                informationMatrix = "%f,0,0,%f,0,%f" % (diagEntry,diagEntry,diagEntry)
        
            elif informationMatrix.count(",")!=5:
                print "! Invalid number of entries in information matrix. Full upper triangular form has to be given, e.g. --information=42,0,0,42,0,42."
                return False
            
    elif mode == 3:
        edgeStr='EDGE_SE3'

        # check entries for information matrix for additional loop closure constraints (outliers)        
        if not informationMatrix:
            print "Determining information matrix automatically"                                      
        else:        
            if informationMatrix.count(",")==0:
                # if there is only a single value, convert it into full upper triangular form with that value on the diagonal
                try:                
                    diagEntry=float(informationMatrix)
                except:
                    print "! Invalid value for information matrix. If you give only a single value, it must be a number, e.g. --information=42"
                    return False
                informationMatrix = "%f,0,0,0,0,0,%f,0,0,0,0,%f,0,0,0,%f,0,0,%f,0,%f" % (diagEntry,diagEntry,diagEntry,diagEntry, diagEntry, diagEntry)
            elif informationMatrix.count(",")!=20:
                print "! Invalid number of entries in information matrix (--information). Full upper triangular form has to be given."
                return False
    else:
        print "! Invalid mode. It must be either 2 or 3 but was", mode
        return False
    

        
    # now for every edge we need to write out a switchable edge
    # therefore we need a switch vertex and an associated prior edge


    # how many poses are there?
    poseCount = len(vertices)

    switchCount=0

    # for every edge, create a new switch node and its associated prior and write the new switchable edges
    lc_edges = [] # store all the nonsequential edges
    lc_edges_information = []
    for oldStr in edges:

      (a,b) = oldStr.split()[1:3]
      if int(float(a)) != int(float(b))-1: 
        isOdometryEdge = False
        lc_edges.append([int(float(a)), int(float(b))])
      else:
        isOdometryEdge = True

      # compute the average information matrix of all loop closure edges in the original dataset, save it as information matrix for additional outliers
      # @fwu
      if not isOdometryEdge and informationMatrix==None:
          elem = oldStr.split()
          if mode==2:
              informationMatrix_str = ' '.join(elem[-6:])
              str_splited = informationMatrix_str.split(' ')
              lc_edges_information.append([float(value) for value in str_splited])                  
              
          else:
              informationMatrix_str = ' '.join(elem[-21:])
              str_splited = informationMatrix_str.split(' ')
              lc_edges_information.append([float(value) for value in str_splited])

          
      # carry on adding switchable or MaxMix edges
      if doSwitchable and not isOdometryEdge:
        s=' '.join(['VERTEX_SWITCH', str(poseCount + switchCount), str(switchPrior)])
        f.write(s+'\n')

        s=' '.join(['EDGE_SWITCH_PRIOR',str(poseCount + switchCount), str(switchPrior), str(switchInfo)])
        f.write(s+'\n')
    
        elem = oldStr.split()
        s = ' '.join([edgeStr+'_SWITCHABLE', elem[1], elem[2], str(poseCount + switchCount)] + elem[3:])
        f.write(s+'\n')

        switchCount = switchCount + 1
      elif doMaxMix and not isOdometryEdge:
        elem = oldStr.split()
        s = ' '.join([edgeStr+'_MAXMIX'] + [elem[1], elem[2], str(maxmixScale)] + elem[3:])
        f.write(s+'\n')

      elif doMaxMixAgarwal and not isOdometryEdge:
        elem = oldStr.split()

        # first component edge
        edge1 = ' '.join([edgeStr, "1"] + elem[1:])
          
          
        # length of information matrix entry
        if mode==2:
            nInfo = 6
        else:
            nInfo=21

        # build the weighted information matrix for the second component
        info_str = elem[-nInfo:]         
        w = float(maxmixScale)
        weighted_info_str = [str(float(x)*w) for x in info_str]          
  
        # second component edge
        edge2 = ' '.join([edgeStr, str(maxmixWeight)]+ elem[1:-nInfo] + weighted_info_str)

        # put it together
        s = ' '.join([edgeStr+'_MIXTURE'] + [elem[1], elem[2], "2", edge1, edge2])
        f.write(s+'\n')
          
      else:
      
        f.write(oldStr)


    lc_edges_information_array = np.array(lc_edges_information)
    information = np.mean(lc_edges_information_array, axis=0)
    information_str = ["%.2f" % x for x in information]
    informationMatrix =' '.join(information_str)
    print(informationMatrix)

    if groupSize == 1:
        write_random_edges(f, outliers, lc_edges, poseCount, switchCount, switchPrior, switchInfo, edgeStr, maxmixScale, maxmixWeight, doLocal, doLinkdown, doSwitchable, doMaxMix, doMaxMixAgarwal, perfectMatch, mode, informationMatrix)
    else:
        write_group_edges(f, outliers, groupSize, lc_edges, poseCount, switchCount, switchPrior, switchInfo, edgeStr, maxmixScale, maxmixWeight, doLocal, doLinkdown, doSwitchable, doMaxMix, doMaxMixAgarwal, perfectMatch, mode, informationMatrix)
    
    f.close()

    return True

# ==================================================================    
# ==================================================================
# ==================================================================

if __name__ == "__main__":


    # let's start by preparing to parse the command line options
    parser = OptionParser()
    
    # string or numeral options
    parser.add_option("-i", "--in", help = "Path to the original dataset file (in g2o format).", dest="filename")
    parser.add_option("-o", "--out", help = "Results will be written into this file.", default="new.g2o")
    parser.add_option("-n", "--outliers", help = "Spoil the dataset with this many outliers. Default = 100.", default=100, type="int")
    parser.add_option("-g", "--groupsize", help = "Use this groupsize. Default = 1.", default=1, type="int")
    parser.add_option("--switchCov", help = "Set the switch covariance matrix. Default = 1.0", default=1.0, type="float")
    parser.add_option("--information", help = "Set the information matrix for the additional false positive loop closure constraints. Provide either a single value e.g. --information=42 that will be used for all diagonal entries. Or provide the full upper triangular matrix using values separated by commas, but no spaces: --information=42,0,0,42,0,42 etc.")  #, default="42.7,0,0,42.7,0,42.7")
    parser.add_option("--seed", help = "Random seed. If >0 it will be used to initialize the random number generator to create repeatable random false positive loop closures.", default=None, type="int")
    parser.add_option("--maxmixWeight", help = "Weight factor for the null hypothesis used in the max-mixture model. Default = 0.01", default=0.01, type="float")
    parser.add_option("--maxmixScale", help = "Scale factor for the null hypothesis used in the max-mixture model. Default = 10e-12", default=10e-12, type="float")
    
    # boolean options
    parser.add_option("-s", "--switchable", help = "Use the switchable loop closure constraints.", action="store_true", default=False)
    parser.add_option("-m", "--maxmix", help = "Use the max-mixture loop closure constraints.", action="store_true", default=False)
    parser.add_option("--maxmixAgarwal", help = "Use the max-mixture loop closure constraints but create a dataset file that is compatible to the format of Pratik Agarwal's original Max-Mixture code.", action="store_true", default=False)
    parser.add_option("-l", "--local", help = "Create only local false positive loop closure constraints.", action="store_true", default=False)
    parser.add_option("-p", "--perfectMatch", help = "Loop closures match perfectly, i.e. the transformation between both poses is (0,0,0).", action="store_true", default=False)

    # options added by @fwu
    parser.add_option("--linkdown", help = "For all link: vertex_from > vertex_to.", action="store_true", default=False)
    
    
    # parse the command line options
    (options, args) = parser.parse_args()


    # check if the options are valid and sound       
    if checkOptions(options):

        # initialize the random number generator
        random.seed(options.seed)

        # read the original dataset
        print "Reading original dataset", options.filename, "..."        
        (vertices, edges, mode) = readDataset(options.filename)

        # build and save the modified dataset with additional false positive loop closures
        print "Writing modified dataset", options.out, "..."
        if writeDataset(options.out, vertices, edges, mode,
                     options.outliers,
                     1,
                     options.switchCov,
                     options.maxmixWeight,
                     options.maxmixScale,
                     options.groupsize,
                     options.local,
                     options.information,
                     options.switchable,
                     options.linkdown,
                     options.maxmix,                     
                     options.maxmixAgarwal,
                     options.perfectMatch):
            print "Done."


    # command line options were not ok
    else: 
        print
        print "Please use --help to see all available command line parameters."


    
