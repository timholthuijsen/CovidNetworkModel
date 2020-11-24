import networkx as nx
from networkx.algorithms import community
import csv
import pandas

#G is used for the graph without any measures
G = nx.DiGraph()
#F is used for implemnting the first measure
F = nx.DiGraph()
#E for the second measure
E = nx.DiGraph()
E = G
#H for both measures together
H = nx.DiGraph()
H = F


#Converts the moreno file to a list
def read_in(filename):
    f = open(filename, 'r')
    f = f.readlines()
    new_list = []
    f.pop(0), f.pop(0)
    for i in f:
        strng = i.strip()
        new_list.append(strng.split(' '))
    return(new_list)

#adds nodes from lstoData to a graph
def addNodes(lstoData, graph):
    for p in range(len(lstoData)):
        graph.add_node(lstoData[p][0])

#adds edges from lstoData to a graph
def addEdges(lstoData, graph):
    for p in range(len(lstoData)):
        dataPerson = lstoData[p]
        graph.add_edge(dataPerson[0], dataPerson[1], weight = dataPerson[2])

#creates a graph and turns it into a gexf file
def main(lstoData, graph, name):
    addNodes(lstoData, graph)
    addEdges(lstoData, graph)
    
    nx.write_gexf(graph,name)

#an old version of our connection cutter
"""
def con_cutter(lst):
    #if connection between certain individuals is not high enough then cut relationship
    new =[]
    for i in lst:
        if int(i[2])<=2:
            new.append(i)
    return new
"""
def data_analyser(lst): #find the average connection weight between graph members
    ave = 0
    dictt = {}
    for i in lst:
        ave += int(i[2])
        if i[2] not in dictt:
            dictt[i[2]]= 1
        else:
            dictt[i[2]] = int(dictt[i[2]])+1
    ave = ave/len(lst)
    #print(ave)
    #print('number of types of connections:\t',dictt)
    

def con_cutter(lst):
    #if connection weight between certain individuals is not high enough then cut relationship
    counter = 0
    final = []
    temp1 = []
    visited = []
    for i in lst:
        temp = []
        if i[0] not in visited: 
            visited.append(i[0])
            for j in range(counter, len(lst)):
                if lst[j][0] == lst[counter][0]:
                    if len(temp) < 2:
                        temp.append(lst[j])
                    elif lst[j][2] > temp[0][2]:
                        temp.remove(temp[0])
                        temp.append(lst[j])
                    elif lst[j][2] > temp[1][2]: 
                        temp.remove(temp[1])
                        temp.append(lst[j])
                else:
                    break
            
        counter += 1
        temp1.append(temp)
    for i in temp1:
        for j in i:
            final.append(j)
    return final




"""
Reads a csv file where all nodes have been assigned to a specific community 
which has been defined by Clauset-Newman-Moore modularity clustering
"""
with open('graphclassescsv.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

#removes the header
classednode = {}
for node in data:
    classednode[node[0]]=node[2]
del classednode['Id']

#gets the moreno database    
lstoData = read_in("out.moreno_health_health")

"""
A function that makes a list containing all edges that need to be removed
because they connect two nodes that are not in the same cluster
"""
removelist = []    
def removeoutsiders(lstoData,classednode):
    for node in lstoData:
        group = classednode[str(node[0])]
        group1 = classednode[str(node[1])]
        if group != group1:
            additions = [node[0],node[1],node[2]]
            removelist.append(additions)
    return removelist

removeoutsiders(lstoData,classednode)

#removes the edges that need to be removed and writes a new graph file
def isolategroups(removelist,filename):
    E.remove_edges_from(removelist)
    nx.write_gexf(E,filename)


#Find communities in graph using Clauset-Newman-Moore greedy modularity maximization.   
#greedy_modularity_communities(G)                
                
    
#creates graphs and files
isolategroups(removelist,"isolatedcommunities.gexf")
lstoData = read_in("out.moreno_health_health")
lstoData2 = con_cutter(lstoData)
data_analyser(lstoData)
main(lstoData, G, "original.gexf")
main(lstoData2, F, "onlybestfriends.gexf")

