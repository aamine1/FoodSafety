import xlrd
import networkx as nx
import numpy as np
import matplotlib as mpl
import pylab as plt
from networkx.algorithms import bipartite
import xlsxwriter
import itertools
import pickle

file_location = "C:\\Users\\Amine\\Desktop\\new_honey.xlsx"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)

file_location_bad = "C:\\Users\\Amine\\Desktop\\high_risk_graph.xlsx"
workbook_bad=xlrd.open_workbook(file_location_bad)
sheet_bad=workbook_bad.sheet_by_index(0)

G_bad=nx.Graph()
for r in range(sheet_bad.nrows):
	G_bad.add_node(sheet_bad.cell_value(r,0),Type='CONSIGNEE',weight=[],status='bad',US_Port=[])
for r in range(sheet_bad.nrows):
	G_bad.add_node(sheet_bad.cell_value(r,1),Type='SHIPPER',weight=[], status='bad',US_Port=[])
for r in range(sheet_bad.nrows):
        G_bad.add_edge(sheet_bad.cell_value(r,0),sheet_bad.cell_value(r,1),weight=[],date=[])

    
file_location_overall = "C:\\Users\\Amine\\Desktop\\overall_graph.xlsx"
workbook_overall=xlrd.open_workbook(file_location_overall)
sheet_overall=workbook_overall.sheet_by_index(0)

G_overall=nx.Graph()
for r in range(sheet_overall.nrows):
	G_overall.add_node(sheet_overall.cell_value(r,0),Type='CONSIGNEE',weight=[], status='good',US_Port=[])
for r in range(sheet_overall.nrows):
	G_overall.add_node(sheet_overall.cell_value(r,1),Type='SHIPPER',weight=[], status='good',US_Port=[])
for r in range(sheet_overall.nrows):
    for r1 in range(sheet.nrows):
        if (sheet_overall.cell_value(r,1)==sheet.cell_value(r1,2)):
            G_overall.node[G_overall.nodes()[r]]['US_Port']=G_overall.node[G_overall.nodes()[r]]['US_Port']+[sheet.cell_value(r1,6)]
for r in range(sheet_overall.nrows):
        G_overall.add_edge(sheet_overall.cell_value(r,0),sheet_overall.cell_value(r,1),weight=[],date=[])
        for r1 in range(sheet.nrows):
                if (sheet_overall.cell_value(r,0)==sheet.cell_value(r1,1) and sheet_overall.cell_value(r,1)==sheet.cell_value(r1,2)):
                        G_overall[sheet_overall.cell_value(r,0)][sheet_overall.cell_value(r,1)]['weight']=G_overall[sheet_overall.cell_value(r,0)][sheet_overall.cell_value(r,1)]['weight']+[sheet.cell_value(r1,5)]
                        G_overall[sheet_overall.cell_value(r,0)][sheet_overall.cell_value(r,1)]['date']=G_overall[sheet_overall.cell_value(r,0)][sheet_overall.cell_value(r,1)]['date']+[sheet.cell_value(r1,3)]
        

for i in range(len(G_bad.nodes())):
    if (G_bad.nodes()[i] in G_overall.nodes()):
            G_overall.node[G_bad.nodes()[i]]['status']='bad'

for i in range(len(G_overall.nodes())):
    if G_overall.node[G_overall.nodes()[i]]['Type']=='SHIPPER':
        for neighbor in G_overall.neighbors(G_overall.nodes()[i]):
            G_overall.node[G_overall.nodes()[i]]['weight']=G_overall.node[G_overall.nodes()[i]]['weight']+[G_overall[G_overall.nodes()[i]][neighbor]['weight']]

nx.write_gpickle(G_overall,"Overall_Graph.gpickle")

##List_weights_bad_shippers=[]
##for i in range(len(G_overall.nodes())):
##        if (G_overall.node[G_overall.nodes()[i]]['status']=='bad' and G_overall.node[G_overall.nodes()[i]]['color']=='BLUE'):
##                List_weights_bad_shippers=List_weights_bad_shippers+[(G_overall.nodes()[i],G_overall.node[G_overall.nodes()[i]]['weight'])]
##
##New_list_weights_bad_shippers=len(List_weights_bad_shippers)*[0]
##New_list_variance_bad_shippers=len(List_weights_bad_shippers)*[0]
##for k in range(len(List_weights_bad_shippers)):
##        New_list_weights_bad_shippers[k]=list(itertools.chain.from_iterable(List_weights_bad_shippers[k][1]))
##        New_list_variance_bad_shippers[k]=[(List_weights_bad_shippers[k][0],np.nanstd(New_list_weights_bad_shippers[k])/np.nanmean(New_list_weights_bad_shippers[k]))]
##                

##
##List_bad_shippers_degrees=[]
##for i in range(len(G_overall.nodes())):
##    if (G_overall.node[G_overall.nodes()[i]]['status']=='bad' and G_overall.node[G_overall.nodes()[i]]['color']=='BLUE'):
##        List_bad_shippers_degrees=List_bad_shippers_degrees+[G_overall.degree(G_overall.nodes()[i])]
##
##List_bad_consignees_degrees=[]
##for i in range(len(G_overall.nodes())):
##    if (G_overall.node[G_overall.nodes()[i]]['status']=='bad' and G_overall.node[G_overall.nodes()[i]]['color']=='RED'):
##        List_bad_consignees_degrees=List_bad_consignees_degrees+[G_overall.degree(G_overall.nodes()[i])]
##
##List_good_shippers_degrees=[]
##for i in range(len(G_overall.nodes())):
##    if (G_overall.node[G_overall.nodes()[i]]['status']=='good' and G_overall.node[G_overall.nodes()[i]]['color']=='BLUE'):
##        List_good_shippers_degrees=List_good_shippers_degrees+[G_overall.degree(G_overall.nodes()[i])]
##
##List_good_consignees_degrees=[]
##for i in range(len(G_overall.nodes())):
##    if (G_overall.node[G_overall.nodes()[i]]['status']=='good' and G_overall.node[G_overall.nodes()[i]]['color']=='RED'):
##        List_good_consignees_degrees=List_good_consignees_degrees+[G_overall.degree(G_overall.nodes()[i])]
##        
