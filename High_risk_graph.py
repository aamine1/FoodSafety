import xlrd
import networkx as nx
import numpy as np
import matplotlib as mpl
import pylab as plt
from networkx.algorithms import bipartite
import xlsxwriter
import pickle

file_location = "C:\\Users\\Amine\\Desktop\\high_risk_graph.xlsx"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)
G=nx.Graph()
for r in range(sheet.nrows):
	G.add_node(sheet.cell_value(r,0),color='RED',weight=0)
for r in range(sheet.nrows):
	G.add_node(sheet.cell_value(r,1),color='BLUE',weight=0)
for r in range(sheet.nrows):
	G.add_edge(sheet.cell_value(r,0),sheet.cell_value(r,1),weight=0)

##List_degrees=[]
##for node in range(nx.number_of_nodes(G)):
##	List_degrees=List_degrees+[nx.degree(G,G.nodes()[node],weight=None)]
##		
List_consignees_and_degrees=[]
List_consignees_degrees=[]
for node in range(nx.number_of_nodes(G)):
	if (G.node[G.nodes()[node]]['color']=='RED'):
		List_consignees_and_degrees=List_consignees_and_degrees+[(G.nodes()[node],nx.degree(G,G.nodes()[node],weight=None))]
		List_consignees_degrees=List_consignees_degrees+[nx.degree(G,G.nodes()[node],weight=None)]

nx.write_gpickle(G,"bg.gpickle")

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
##
##List_shippers_and_degrees=[]
##List_shippers_degrees=[]
##for node in range(nx.number_of_nodes(G)):
##	if (G.node[G.nodes()[node]]['color']=='BLUE'):
##		List_shippers_and_degrees=List_shippers_and_degrees+[(G.nodes()[node],nx.degree(G,G.nodes()[node],weight=None))]
##		List_shippers_degrees=List_shippers_degrees+[nx.degree(G,G.nodes()[node],weight=None)]
##
##def nb_consignees_degree_one(G):
##        L=[]
##        l=[]
##        for i in range(len(List_consignees_and_degrees)):
##                if (List_consignees_degrees[i]==1):
##                        L=L+[List_consignees_and_degrees[i]]
##                        l=l+[List_consignees_degrees[i]]
##        #print ("The consignees working with one shipper are", L)       
##        return len(l)
##
##giant = max(nx.connected_component_subgraphs(G), key=len)




##print ("The number of nodes is", nx.number_of_nodes(G))
##print ("The number of consignees is", len(List_consignees_degrees))
##print ("The number of shippers is", nx.number_of_nodes(G)-len(List_consignees_degrees))
##print ("The number of edges is", nx.number_of_edges(G))
#print ("Is the graph bipartite ?", nx.is_bipartite(G))
#print ("The max degree of consignees and the consignee with the highest degree is", np.max(List_consignees_degrees),List_consignees_and_degrees[np.argmax(List_consignees_degrees)][0])
##print ("The mean degree is", np.mean(List_degrees))
##print ("The mean degree of consignees is", np.mean(List_consignees_degrees))
##print ("The max degree of consignees is", np.max(List_consignees_degrees))
##print ("The min degree of consignees is", np.min(List_consignees_degrees))
##print ("The std of consignees degrees is", np.std(List_consignees_degrees))
##print ("The mean degree of shippers is", np.mean(List_shippers_degrees))
##print ("The max degree of shippers is", np.max(List_shippers_degrees))
##print ("The min degree of shippers is", np.min(List_shippers_degrees))
##print ("The std of shippers degrees is", np.std(List_shippers_degrees))
#print ("The standard deviation of the degree distribution is", np.std(List_degrees))
#print ("The median degree is", np.median(List_consignees_degrees))
##print ("The 10 percentile is ", np.percentile(List_consignees_degrees,10))
##print ("The 20 percentile is ", np.percentile(List_consignees_degrees,20))
##print ("The 25 percentile is ", np.percentile(List_consignees_degrees,25))
##print ("The 90 percentile is ", np.percentile(List_consignees_degrees,90))
##print ("The 80 percentile is ", np.percentile(List_consignees_degrees,80))
##print ("The 75 percentile is ", np.percentile(List_consignees_degrees,75))
##print ("The 10 percentile is s", np.percentile(List_shippers_degrees,10))
##print ("The 20 percentile is s", np.percentile(List_shippers_degrees,20))
##print ("The 25 percentile is s", np.percentile(List_shippers_degrees,25))
##print ("The 90 percentile is s", np.percentile(List_shippers_degrees,90))
##print ("The 80 percentile is s", np.percentile(List_shippers_degrees,80))
##print ("The 75 percentile is s", np.percentile(List_shippers_degrees,75))
#print ("The number of connected components is", nx.number_connected_components(G))
#print ("The ratio of shippers by consignees is", (nx.number_of_nodes(G)-len(List_consignees_degrees))/len(List_consignees_degrees))
#print ("The ratio of edges by nodes is", nx.number_of_edges(G)/nx.number_of_nodes(G))
#print ("The average bipartie clustering coefficient is", bipartite.average_clustering(G))
#print ("The number of consignees working with one shipper is", nb_consignees_degree_one(G))
#print ("The size of the max connected component is", nx.number_of_nodes(giant))

##workbook = xlsxwriter.Workbook('summary.xlsx')
##worksheet = workbook.add_worksheet()
##
##worksheet.write(0,1, "Number of nodes")
##worksheet.write(1,1, nx.number_of_nodes(G))
##worksheet.write(0,2, "Number of consignees")
##worksheet.write(1,2, len(List_consignees_degrees))
##worksheet.write(0,3, "Number of shippers")
##worksheet.write(1,3, nx.number_of_nodes(G)-len(List_consignees_degrees))
##worksheet.write(0,4, "Number of edges")
##worksheet.write(1,4, nx.number_of_edges(G))
##worksheet.write(0,5, "Is the graph bipartite ?")
##worksheet.write(1,5, nx.is_bipartite(G))
##worksheet.write(0,6, "The highest degree of a consignee")
##worksheet.write(1,6, np.max(List_consignees_degrees))
##worksheet.write(0,7, "The consignee with the highest degree is")
##worksheet.write(1,7, List_consignees_and_degrees[np.argmax(List_consignees_degrees)][0])
##worksheet.write(0,8, "The mean degree is")
##worksheet.write(1,8, np.mean(List_degrees))
##worksheet.write(0,9, "The standard deviation of the degree distribution is")
##worksheet.write(1,9, np.std(List_degrees))
##worksheet.write(0,10, "The median degree is")
##worksheet.write(1,10, np.median(List_consignees_degrees))
##worksheet.write(0,11, "The 25 percentile is ")
##worksheet.write(1,11, np.percentile(List_consignees_degrees,25))
##worksheet.write(0,12, "The 75 percentile is")
##worksheet.write(1,12, np.percentile(List_consignees_degrees,75))
##worksheet.write(0,13, "The number of connected components is")
##worksheet.write(1,13, nx.number_connected_components(G))
##worksheet.write(0,14, "The ratio of shippers by consignees is")
##worksheet.write(1,14, (nx.number_of_nodes(G)-len(List_consignees_degrees))/len(List_consignees_degrees))
##worksheet.write(0,15, "The ratio of edges by nodes is")
##worksheet.write(1,15, nx.number_of_edges(G)/nx.number_of_nodes(G))
##worksheet.write(0,16, "The average bipartie clustering coefficient is")
##worksheet.write(1,16, bipartite.average_clustering(G))
##worksheet.write(0,17, "The number of consignees working with one shipper is")
##worksheet.write(1,17, nb_consignees_degree_one(G))
##worksheet.write(0,18, "The size of the max connected component is")
##worksheet.write(1,18, nx.number_of_nodes(giant))
##
##workbook.close()


