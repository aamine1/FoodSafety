import xlrd
import networkx as nx
import numpy as np
import matplotlib as mpl
import pylab as plt
from networkx.algorithms import bipartite
import xlsxwriter

file_location_good = "C:\\Users\\Amine\\Desktop\\good_graph.xlsx"
workbook_good=xlrd.open_workbook(file_location_good)
sheet_good=workbook_good.sheet_by_index(0)
G_good=nx.Graph()
for r in range(sheet_good.nrows):
	G_good.add_node(sheet_good.cell_value(r,0),color='RED',weight=0)
for r in range(sheet_good.nrows):
	G_good.add_node(sheet_good.cell_value(r,1),color='BLUE',weight=0)
for r in range(sheet_good.nrows):
	G_good.add_edge(sheet_good.cell_value(r,0),sheet_good.cell_value(r,1),weight=0)




file_location_overall = "C:\\Users\\Amine\\Desktop\\overall_graph.xlsx"
workbook_overall=xlrd.open_workbook(file_location_overall)
sheet_overall=workbook_overall.sheet_by_index(0)
G_overall=nx.Graph()
for r in range(sheet_overall.nrows):
	G_overall.add_node(sheet_overall.cell_value(r,0),color='RED',weight=0)
for r in range(sheet_overall.nrows):
	G_overall.add_node(sheet_overall.cell_value(r,1),color='BLUE',weight=0)
for r in range(sheet_overall.nrows):
	G_overall.add_edge(sheet_overall.cell_value(r,0),sheet_overall.cell_value(r,1),weight=0)

def does_belong(e,list):
    if list!=[]:
        for r in range(len(list)):
            if (list[r]==e):
                return True
        return False

def remove_element(e,list):
    while list!=[]:
        if does_belong(e,list)==True:
            list = list.remove(e)
    return list
        
       

	
List_degrees=[]
for node in range(nx.number_of_nodes(G_overall)):
	List_degrees=List_degrees+[nx.degree(G_overall,G_overall.nodes()[node],weight=None)]
		
List_consignees_and_degrees=[]
List_consignees_degrees=[]
for node in range(nx.number_of_nodes(G_good)):
	if (G_good.node[G_good.nodes()[node]]['color']=='RED'):
		List_consignees_and_degrees=List_consignees_and_degrees+[(G_good.nodes()[node],nx.degree(G_overall,G_good.nodes()[node],weight=None))]
		List_consignees_degrees=List_consignees_degrees+[nx.degree(G_overall,G_good.nodes()[node],weight=None)]

##def average_degree(G, node):
##        m=0
##        for i in G.neighbors(node):
##                m=m+G.degree(i)
##        return m/G.degree(node)
##
##List_consignees_and_average_degrees=[]
##List_consignees_average_degrees=[]
##for node in range(nx.number_of_nodes(G)):
##	if (G.node[G.nodes()[node]]['color']=='RED'):
##		List_consignees_and_average_degrees=List_consignees_and_average_degrees+[G.nodes()[node],average_degree(G,G.nodes()[node])]
##		List_consignees_average_degrees=List_consignees_average_degrees+[average_degree(G,G.nodes()[node])]

List_shippers_and_degrees=[]
List_shippers_degrees=[]
for node in range(nx.number_of_nodes(G_good)):
	if (G_good.node[G_good.nodes()[node]]['color']=='BLUE'):
		List_shippers_and_degrees=List_shippers_and_degrees+[(G_good.nodes()[node],nx.degree(G_overall,G_good.nodes()[node],weight=None))]
		List_shippers_degrees=List_shippers_degrees+[nx.degree(G_overall,G_good.nodes()[node],weight=None)]

##def nb_consignees_degree_one(G):
##        L=[]
##        l=[]
##        for i in range(len(List_consignees_and_degrees)):
##                if (List_consignees_degrees[i]==1):
##                        L=L+[List_consignees_and_degrees[i]]
##                        l=l+[List_consignees_degrees[i]]
##        #print ("The consignees working with one shipper are", L)       
##        return len(l)

#giant = max(nx.connected_component_subgraphs(G), key=len)


List_consignees_degrees=remove_element({},List_consignees_degrees)
List_shippers_degrees=remove_element({},List_shippers_degrees)

print ("The number of nodes is", nx.number_of_nodes(G_good))
print ("The number of consignees is", len(List_consignees_degrees))
print ("The number of shippers is", nx.number_of_nodes(G_good)-len(List_consignees_degrees))
print ("The number of edges is", nx.number_of_edges(G_good))
#print ("Is the graph bipartite ?", nx.is_bipartite(G))
#print ("The max degree of consignees and the consignee with the highest degree is", np.max(List_consignees_degrees),List_consignees_and_degrees[np.argmax(List_consignees_degrees)][0])
print ("The mean degree is", np.nanmean(List_degrees))
print ("The mean degree of consignees is", np.nanmean(List_consignees_degrees))
print ("The max degree of consignees is", np.max(List_consignees_degrees))
print ("The min degree of consignees is", np.min(List_consignees_degrees))
print ("The std of consignees degrees is", np.nanstd(List_consignees_degrees))
print ("The mean degree of shippers is", np.nanmean(List_shippers_degrees))
print ("The max degree of shippers is", np.max(List_shippers_degrees))
print ("The min degree of shippers is", np.min(List_shippers_degrees))
print ("The std of shippers degrees is", np.nanstd(List_shippers_degrees))
#print ("The standard deviation of the degree distribution is", np.std(List_degrees))
#print ("The median degree is", np.median(List_consignees_degrees))
print ("The 10 percentile is ", np.percentile(List_consignees_degrees,10))
print ("The 20 percentile is ", np.percentile(List_consignees_degrees,20))
print ("The 25 percentile is ", np.percentile(List_consignees_degrees,25))
print ("The 90 percentile is ", np.percentile(List_consignees_degrees,90))
print ("The 80 percentile is ", np.percentile(List_consignees_degrees,80))
print ("The 75 percentile is ", np.percentile(List_consignees_degrees,75))
print ("The 10 percentile is s", np.percentile(List_shippers_degrees,10))
print ("The 20 percentile is s", np.percentile(List_shippers_degrees,20))
print ("The 25 percentile is s", np.percentile(List_shippers_degrees,25))
print ("The 90 percentile is s", np.percentile(List_shippers_degrees,90))
print ("The 80 percentile is s", np.percentile(List_shippers_degrees,80))
print ("The 75 percentile is s", np.percentile(List_shippers_degrees,75))
#print ("The number of connected components is", nx.number_connected_components(G))
#print ("The ratio of shippers by consignees is", (nx.number_of_nodes(G)-len(List_consignees_degrees))/len(List_consignees_degrees))
#print ("The ratio of edges by nodes is", nx.number_of_edges(G)/nx.number_of_nodes(G))
#print ("The average bipartie clustering coefficient is", bipartite.average_clustering(G))
#print ("The number of consignees working with one shipper is", nb_consignees_degree_one(G))
#print ("The size of the max connected component is", nx.number_of_nodes(giant))
