from  owlready2 import get_ontology, sync_reasoner_pellet
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import time
from math import sqrt

#if you want to measure time
start_time = time.time()

# lever: control variable
# 0 - populate ontology, 
# 1 - calculate expertise weight
# 2 - calculate semantic weight (new network)
lever = 3

#########################################################################################
############################ ------------------------------- ############################
############################ ****** POPULATE ONTOLOGY ****** ############################
############################            <INPUT>              ############################
############################ ontologia: ExFindOtaxo.owl         #########################
############################ tags file: tags-pull-nodejs.csv    #########################
############################ developers file: author-pull-nodejs.csv ####################
############################            <OUTPUT>                     ####################
#333######################## populated ontology: result.owl          ####################
############################ --------------------------------------- ####################
#########################################################################################

if lever == 0:
    onto = get_ontology("/home/tales/.config/spyder-py3/ExFindO/input/ExFindOtaxo.owl").load()
    
    #insert PullRequests and Tags
    dados =  pd.read_csv('/home/tales/.config/spyder-py3/ExFindO/input/tags-pull-nodejs.csv', sep=";", header=0)
    array = dados.values
    size = 0
    for n in array:
        size = size + 1
    k = 0
    for k in range(size):
        tag = onto.Tag("Tag"+str(array[k][1]))
        tag.tagname.append(str(array[k][1]))
        pull = onto.PullRequest("PullRequest"+str(int(array[k][0])))
        pull.hasTag.append(tag) 
        k = k + 1
    
    #insert developers
    dados =  pd.read_csv('/home/tales/.config/spyder-py3/ExFindO/input/author-pull-nodejs.csv', sep=";", header=0)
    array = dados.values
    size = 0
    for n in array:
        size = size + 1
    k = 0
    for k in range(size):
        pull = onto.PullRequest("PullRequest"+str(int(array[k][0])))
        dev = onto.Developer(str(array[k][1]))
        dev.hasPullRequest.append(pull)
        k = k + 1
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    
        #get all PullRequests
    PR = onto.search(type = onto.PullRequest)
    N = onto.search(type = onto.NULL)
        #for each PullRequest
    for i in PR:
        top = i.hasTopic
        stop = i.hasSpecificTopic
        mod = i.hasModule
        di = i.hasDirectory
        ap = i.hasPA
        cont = 1
        #if empty receiver NULL. Not to block the loop below.
        if(not top):
            top = N
        if(not stop):
            stop = N
        if(not mod):
            mod = N
        if(not di):
            di = N
        if(not ap):
            ap = N
        if(top!=N): 
            for a in top:
                for b in mod:
                    for c in di:
                        for d in ap:
                            #create object expertise
                            ex = onto.Expertise(i.name+"Expertise"+str(cont), hasTopic = [a], hasModule = [b], hasDirectory = [c], hasPA = [d], hasSpecificTopic = N)
                            #create relation PullRequest hasExpertise
                            i.hasExpertise.append(ex)
                            cont = cont + 1
        if(stop!=N): 
            for a in stop:
                for b in mod:
                    for c in di:
                        for d in ap:
                            #create object expertise
                            ex = onto.Expertise(i.name+"Expertise"+str(cont), hasSpecificTopic = [a], hasModule = [b], hasDirectory = [c], hasPA = [d], hasTopic = N)
                            #create relation PullRequest hasExpertise
                            i.hasExpertise.append(ex)
                            cont = cont + 1
        if(stop==N and top==N): 
            for a in top:
                for b in mod:
                    for c in di:
                        for d in ap:
                            #create object expertise
                            ex = onto.Expertise(i.name+"Expertise"+str(cont), hasSpecificTopic = N, hasModule = [b], hasDirectory = [c], hasPA = [d], hasTopic = N)
                            #create relation PullRequest hasExpertise
                            i.hasExpertise.append(ex)
                            cont = cont + 1
    
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    onto.save(file = "/home/tales/Downloads/ExFindO/result.owl", format = "rdfxml")


#########################################################################################
############################ -------------------------------  ###########################
############################ CALCULATE EXPERTISE WEIGHT GIVEN ###########################
############################ A SET OF REQUIRED EXPERTISES!!!  ###########################
############################            <INPUT>               ###########################
############################ network retrieved from neo4j: export.csv ###################
############################ populated ontology: result.owl           ###################
############################ ---------------------------------------- ###################
#########################################################################################

if lever == 1 or lever == 2 :
    #network (get unique dev)
    file = '/home/tales/.config/spyder-py3/ExFindO/input/export.csv'
    dados =  pd.read_csv(file, sep=",", header=0)
    array = dados.values
    size = 0
    for n in array:
        size = size + 1
        
    #get the higher value and normalize network edges' weight (sintatic weights)
    """
    higher = 0
    for i in range(size):
        if array[i][2] > higher:
            higher = array[i][2]
    
    for i in range(size):
        print( array[i][2]/higher )
    """
        
    unique_dev = []
    for k in range(size):
        if array[k][0] not in unique_dev:
            unique_dev.append(array[k][0])
        if array[k][1] not in unique_dev:
            unique_dev.append(array[k][1])
    
    onto = get_ontology("/home/tales/Downloads/ExFindO/result.owl").load()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    
    #required expertise (topic, specific topic, module, directory, pa)
    number_of_expertises = 15
    re = numpy.empty(number_of_expertises, dtype=object)
    #all expertises (topics specific topics)
    re[0] = ['[result.Diagnostics]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[1] = ['[result.Memory]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[2] = ['[result.Performance]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[3] = ['[result.Security]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[4] = ['[result.ProjectManagement]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[5] = ['[result.CI]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[6] = ['[result.Testing]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[7] = ['[result.Updating]', '[result.null]', '[result.null]', '[result.null]', '[result.null]']
    re[8] = ['[result.null]', '[result.C++]', '[result.null]', '[result.null]', '[result.null]']
    re[9] = ['[result.null]', '[result.Python]', '[result.null]', '[result.null]', '[result.null]']
    re[10] = ['[result.null]', '[result.ES6+]', '[result.null]', '[result.null]', '[result.null]']
    re[11] = ['[result.null]', '[result.NewFeature]', '[result.null]', '[result.null]', '[result.null]']
    re[12] = ['[result.null]', '[result.CoreFeature]', '[result.null]', '[result.null]', '[result.null]']
    re[13] = ['[result.null]', '[result.OperationalErrors]', '[result.null]', '[result.null]', '[result.null]']
    re[14] = ['[result.null]', '[result.ProgrammerErrors]', '[result.null]', '[result.null]', '[result.null]']
    
    #semantic matrix (structure with the knowledge weight related to required expertises)
    size = 0
    for k in unique_dev:
        size = size + 1
    matrix = [[0 for x in range(number_of_expertises)] for y in range(size)] 
    
    #weight calculus
    #for each developer
    for i in range(size):
        D = onto.search_one(iri = "*" + str(unique_dev[i]))
        ex = D.hasExpertise
        count = 0
        for j in ex:
            c = 0 #counter for each required expertise (for each developer)
            for k in re: #for each required expertise
                v = k
                flag = 1 #flag to say if the developer has or not the expertise
                if( str(j.hasTopic)!=v[0] and v[0]!='[result.null]' ):
                    flag = 0
                if( str(j.hasSpecificTopic)!=v[1] and v[1]!='[result.null]' ):
                    flag = 0
                if( str(j.hasModule)!=v[2] and v[2]!='[result.null]' ):
                    flag = 0
                if( str(j.hasDirectory)!=v[3] and v[3]!='[result.null]'):
                    flag = 0
                if( str(j.hasPA)!=v[4] and v[4]!='[result.null]'):
                    flag = 0
                if(flag == 1):
                    matrix[i][c] = matrix[i][c] + 1
                c = c + 1
    
    #get the higher expertise values
    higher = [0] * number_of_expertises
    for i in range(size):
        aux = matrix[i]
        for j in range(number_of_expertises):
            if aux[j] > higher[j]:
                higher[j] = aux[j]
    
    #normalize
    for i in range(size):
        for j in range(number_of_expertises):
            if(higher[j]==0):
               matrix[i][j] = 0
            else:
                matrix[i][j] = matrix[i][j]/higher[j]
            
    #print each unique developers and its expertise weight
    a = 0
    for i in unique_dev:
        a = a + 1
    for i in range(a):
        print(unique_dev[i], matrix[i])


#########################################################################################
############### --------------------------------------------------------- ###############
############### ------------ CALCULATE EXPERTISE WEIGHT GIVEN ----------- ###############
############### SemanticCollaborationWeight(SCW) = OldEdgeWeight(OEW) * X ###############
############### X = 1 - DistEucl(TP,E_i) / sqrt(|T|)                      ###############
############### -------------------------------------------------------- ################
############### --------------------------------------------------------- ###############
###############  ***number_of_expertises = 3 is default in this step***  ################
###############  ***change in the step above***                          ################
############### --------------------------------------------------------- ###############
#########################################################################################

if lever == 2:
    SCW = []
    OEW = dados["w.total"]
    source = dados["b.idpessoa"]
    target = dados["a.idpessoa"]
    
    size = 0
    for i in OEW:
        size = size + 1
    
    mode = 4
    
    #MODE 1 (semantic weight * syntatic weight )
    if mode == 1:
        for i in range(size):
            index = unique_dev.index(source[i])
            DistEucl = sqrt( pow(1 - matrix[index][0], 2) + pow(1 - matrix[index][1], 2) + pow(1 - matrix[index][2], 2) )
            X = 1 - ( DistEucl / sqrt(number_of_expertises) )
            scw = OEW[i] * X
            SCW.append(scw)
        print(SCW)
    
    #MODE 2 (semantic weight)
    if mode == 2:
        for i in range(size):
            index = unique_dev.index(source[i])
            DistEucl = sqrt( pow(1 - matrix[index][0], 2) + pow(1 - matrix[index][1], 2) + pow(1 - matrix[index][2], 2) )
            X = 1 - ( DistEucl / sqrt(number_of_expertises) )
            SCW.append(X)
        print(SCW)
    
    #MODE 3 (semantic weight(EXPERTISE UNION) * syntatic weight)
    if mode == 3:
        for i in range(size):
            index = unique_dev.index(source[i])
            index2 = unique_dev.index(target[i])
            x1 = max(matrix[index][0], matrix[index2][0]) 
            y1 = max(matrix[index][1], matrix[index2][1])
            z1 = max(matrix[index][2], matrix[index2][2]) 
            DistEucl = sqrt( pow(1 - x1, 2) + pow(1 - y1, 2) + pow(1 - z1, 2) )
            X = 1 - ( DistEucl / sqrt(number_of_expertises) )
            scw = OEW[i] * X
            SCW.append(scw)
        print(SCW)
    
    #MODE 4 (EXPERTISE UNION)
    if mode == 4:
        for i in range(size):
            index = unique_dev.index(source[i])
            index2 = unique_dev.index(target[i])
            x1 = max(matrix[index][0], matrix[index2][0]) 
            y1 = max(matrix[index][1], matrix[index2][1])
            z1 = max(matrix[index][2], matrix[index2][2]) 
            DistEucl = sqrt( pow(1 - x1, 2) + pow(1 - y1, 2) + pow(1 - z1, 2) )
            X = 1 - ( DistEucl / sqrt(number_of_expertises) )
            SCW.append(X)
        print(SCW)

#########################################################################################
################### ------------------------------------------------- ###################
################### ****** POPULATE ONTOLOGY WITH WEIGHT OBJECTS **** ###################
################### ****** AND GENERATE GRAPHICS!!!              **** ###################
################### ------------------------------------------------- ###################
#########################################################################################

"""
D = onto.search(type = onto.Developer)
num = 0
dev = []
w = []
#for each developer
for j in D:
    num = num + 1
    count = 0
    ex = j.hasExpertise
    #for each expertise 'k' of developer 'j'
    for k in ex:
        flag = 1
        for i in re:
            v = re[i]
            if( str(k.hasTopic)!=v[0] and v[0]!='[result.null]' ):
                flag = 0
            if( str(k.hasSpecificTopic)!=v[1] and v[1]!='[result.null]' ):
                flag = 0
            if( str(k.hasModule)!=v[2] and v[2]!='[result.null]' ):
                flag = 0
            if( str(k.hasDirectory)!=v[3] and v[3]!='[result.null]'):
                flag = 0
            if( str(k.hasPA)!=v[4] and v[4]!='[result.null]'):
                flag = 0
            if(flag == 1):
                count = count + 1
    #insert weight into ontology
    wei = onto.Weight("Developer"+str(num)+"Weight")
    wei.weight.append(count)
    if(count != 0):
        dev.append(str(j.name))
        w.append(count)

"""

#GRAPHICS
"""
print(dev)
print(w)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(dev,w)
plt.xticks(rotation=90)
ax.set_xlabel('Developers')
ax.set_ylabel('Expertise Weight')
ax.set_title('Expert Rank')
plt.show()        
"""

print("--- %s seconds ---" % (time.time() - start_time))