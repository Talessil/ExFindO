from owlready2 import get_ontology, sync_reasoner_pellet
import pandas as pd
import numpy

#print("abrindo ontologia...")
onto = get_ontology("/home/tales/Downloads/NodeESOtaxo.owl").load()

    #populate onto
#insert PullRequests and Tags
dados =  pd.read_csv('tags-pull-nodejs.csv', sep=";", header=0)
array = dados.values
size = 0
for n in array:
    size = size + 1
k = 0
for k in range(size):
    tag = onto.Tag("Tag"+str(array[k][1]))
    tag.tagname.append(str(array[k][1]))
    pull = onto.PullRequest("PullRequest"+str(array[k][0]))
    pull.hasTag.append(tag) 
    k = k + 1
    

sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

#insert developers
dados =  pd.read_csv('author-pull-nodejs.csv', sep=";", header=0)
array = dados.values
size = 0
for n in array:
    size = size + 1
k = 0
for k in range(size):
    pull = onto.PullRequest("PullRequest"+str(array[k][0]))
    dev = onto.Developer("Dev"+str(array[k][1]))
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
    #print(top,stop,mod)
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



#required expertise

top = '[NodeESOtaxo.null]'
stop = '[NodeESOtaxo.C++]'
mod = '[NodeESOtaxo.null]'
di = '[NodeESOtaxo.null]'
pa = '[NodeESOtaxo.null]'

D = onto.search(type = onto.Developer)
num = 0
for j in D:
    num = num + 1
    count = 0
    ex = j.hasExpertise
    for k in ex:
        flag = 1
        if(top != str(k.hasTopic)):
            flag = 0
        if(stop != str(k.hasSpecificTopic)):
            flag = 0
        if(mod != str(k.hasModule)):
            flag = 0
        if(di != str(k.hasDirectory)):
            flag = 0
        if(pa != str(k.hasPA)):
            flag = 0
        if(flag == 1):
            count = count + 1
    wei = onto.Weight("Developer"+str(num)+"Weight")
    wei.weight.append(count)
    #print(count)


onto.save(file = "/home/tales/Downloads/result.owl", format = "rdfxml")
