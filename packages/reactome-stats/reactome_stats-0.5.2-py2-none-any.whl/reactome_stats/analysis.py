#Python 2.7
#Neo4J 3.2.3
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import networkx as nx
import time
import os
import re
import urllib
import json
from collections import Counter
import itertools
import matplotlib.pyplot as plt
from neo4j.v1 import GraphDatabase, basic_auth
import csv
from matplotlib_venn import venn2
from matplotlib_venn import venn3
import matplotlib.patches as mpatches
import uniprot
import kegg
import reactomegraphdb
import goc 
import reactome_stats #<-coherent? 

'''
|==========|
|ANALYSIS 1|
|==========|

Function 'analysis 1' retrieve 4 visualizations related with Reactome events coverage over UniProt resource. UniProt provide information about protein families and also links to Reactome pathways. Some of them are missing and that's why this analysis 1 can highlight to be reported. 

Visualizations:
1)Bar plot number of reactome proteins per family. 
2)Bins plot (normalization)
3)Venn Diagram coverage proteins at Reactome human pathways compared to proteins at UniProt human and reviewed
4)Donugh plot related with the no human or no reviewed proteins at Reactome human patways. 

Two tables result are also provided.
1) Table with number of different Reactome events (polymerisation, reaction, blackbox event, so on) per pathways and top level pathways.
2) All the results provided by the query at Neo4J providing all the uniprotID related with any event at Reactome human pathways (no disease). 

'''
def analysis1(usernam, passwd, toWrite = False, filterN = 50):

	print('''====================\nRunning -Analysis 1-\n====================\n'''+ time.strftime("%H:%M:%S"))

	df_4reactome_ee = reactomegraphdb.get_elementEventReactomeAll(usernam,passwd)
	
	df_1reactome = reactomegraphdb.neo4JCypher(usernam,passwd)
	df_2uniprotAllH = uniprot.get_dfUniProtAllH()

	#also barplot with normalized count of proteins per family which are or not in Reactome. 
	df_3uniprotHR = uniprot.get_dfUniProtHR()

	#BARPLOT
	reactome_stats.showBarPlotReactionsPerFamily(df_4reactome_ee, df_3uniprotHR, filterN = filterN, toWrite = toWrite)		
	
	#VENN DIAGRAM
	listComparisonS = reactome_stats.compareSources(df_1reactome,df_2uniprotAllH, toWrite = toWrite)


	#GRAPH/DENDROGRAM
	df_4reactome_ee_network1 = df_4reactome_ee.groupby(['p.schemaClass', 'rle.schemaClass'])['ReactomeID_child'].nunique().to_frame().reset_index()
	print("Counts of Events per Pathway or TopLevelPathway:\n====================================================")
	print(df_4reactome_ee_network1)
	print("====================================================")

	if toWrite == True:

		df_4reactome_ee.to_csv('output_a1_countPathwaysEvents.csv', index = False, sep = "\t")
		df_4reactome_ee_network1.to_csv('output_a1_PathwaysEventsGraphDB.csv', index = False, sep = "\t")

	print('Analysis finished succesfully at ' + time.strftime("%H:%M:%S"))
	#reactome_stats.showBarPlotReactionsPerFamily(df_familyCounts, filterN = filterN)

	df_rup_familyAll = reactome_stats.get_NpathwaysPerFamily(df_4reactome_ee, df_3uniprotHR, filterN = filterN)

	reactome_stats.barStack_proteinFamiliesPathEvents(df_rup_familyAll, filterN = filterN)
	listTables = [df_4reactome_ee, df_4reactome_ee_network1, df_rup_familyAll]

	return(listTables)



'''
|==========|
|ANALYSIS 2|
|==========|

Function 'analysis 2' retrieve 2 visualizations related with Reactome GO (GO tagged with Reactome at UniProt and Uniprot tagged to GO by GOC annotations). Some GO are not yet annotated at Reactome or some are inferred electronically. This last group is convenient to report it to GOC database.  

Visualizations:
1)Venn Diagram coverage proteins at Reactome human pathways with GO compared to all the proteins annotated at GOC
2)Venn Diagram coverage of GO at Reactome compared to all the GO at GOC


'''
def analysis2( loadCopyNovember2017 = False, toWrite = False):

	print('''====================\nRunning -Analysis 2-\n====================\n'''+ time.strftime("%H:%M:%S"))
	#print("Reactome GraphDB v62 retrieve an issue. Sorry for the issues. So far the GO are retrieved from UniProt Search engine") #update, removed arguments from the function: usernam = None, passwd = None.
	df_3uniprotHR = uniprot.get_dfUniProtHR()
	df_GOC_UniProt= goc.get_gocAnnotation(typeSet = 'all', loadCopyNovember2017 = loadCopyNovember2017)
	df_GOC_UniProt_curated = goc.get_gocAnnotation(typeSet = 'curated', loadCopyNovember2017 = loadCopyNovember2017)
	df_GOC_UniProt_iea = goc.get_gocAnnotation(typeSet = 'iea', loadCopyNovember2017 = loadCopyNovember2017)
	df_3uniprotHRr = df_3uniprotHR[~df_3uniprotHR['ReactomeID'].isin(['No at Reactome'])]
	df_3uniprotHRgo = df_GOC_UniProt[df_GOC_UniProt['DB_Object_ID'].isin(df_3uniprotHRr['DB_Object_ID'].unique())]

	#vennCoverage_3d (table1, table2, table3, colname, vs1="A", vs2="B", vs3="C")
	#comparing proteins with GO annotated in reactome, curated at GOC and inferred at GOC
	listvenn3_up = reactome_stats.vennCoverage_3d(df_3uniprotHRr,df_GOC_UniProt_curated, df_GOC_UniProt_iea, 'DB_Object_ID', vs1="proteins with GO Reactome", vs2="proteins GO curated ", vs3="proteins GO inferred electronically")

	#comparing GO at Reactome, GO curated and GO inferred ellectronically
	listvenn3_go = reactome_stats.vennCoverage_3d(df_3uniprotHRgo,df_GOC_UniProt_curated, df_GOC_UniProt_iea, 'GO_ID', vs1="GO in Reactome", vs2="GO curated ", vs3="GO inferred electronically")

	print('Analysis 2 finished succesfully at' + time.strftime("%H:%M:%S"))
	listIntersections = [listvenn3_up, listvenn3_go]
	return(listIntersections)


'''
|==========|
|ANALYSIS 3|
|==========|

Function 'analysis 3' retrieves 
Tables
1) a human reviewed proteins table associated summarizing different aspects of annotations, 
2) a family Proteins table summarizing different aspects of annotations associated to it . <- interesting to play and create more visualizations
3) Info about kegg (duplicated values, proteins with kegg pathways) <- report to Kegg

Visualizations:
4) barplot of families of interest (one Go with one protein).
'''
def analysis3(toWrite = False, loadCopyNovember2017 = False, filterN = 50):

	print('''====================\nRunning -Analysis 3-\n====================\n'''+ time.strftime("%H:%M:%S"))

	#1 -Loading sources
	#print("Loading UniProt")
	df_up = uniprot.get_dfUniProtHR()
	#print("Loading GOC annotation")  
	df_GOC_UniProt_curated = goc.get_gocAnnotation(typeSet = 'curated')

	#2 -Executing functions
	listKegghsa = uniprot.get_hsaList(df_up)	
	df_keggPathw = kegg.get_keggPathw(listKegghsa,loadCopyNovember2017 = loadCopyNovember2017)

	#print("Executing 'df_KeggReactomePathways'")
	df_KeggReactomePathways = reactome_stats.get_reactomeKeggPathwaysTable(df_up, df_keggPathw)
	#print("Executing 'df_proteinsGOCAnnotation_nu_fam_kegg_reactome_output'")
	df_proteinsGOCAnnotation_nu_fam_kegg_reactome_output = reactome_stats.get_worktable(df_GOC_UniProt_curated, df_up, df_KeggReactomePathways, toWrite = toWrite, loadCopyNovember2017 = loadCopyNovember2017) #<---this can be important for analysis 2 to do the stack bar plot
	#print("Executing 'df_familyCounts'")
	df_familyCounts = reactome_stats.get_clusteredFamily_counts(df_proteinsGOCAnnotation_nu_fam_kegg_reactome_output, toWrite = toWrite)

	#3 -Visualize data
	#print("Executing visualizations with filter predefined (Top 50)")
	reactome_stats.showBarPlot(df_familyCounts, filterN = filterN)

	print('Analysis 3 finished succesfully at' + time.strftime("%H:%M:%S"))

	return(df_proteinsGOCAnnotation_nu_fam_kegg_reactome_output)


'''
|==========|
|ANALYSIS 4|
|==========|

Function 'analysis 4' map all the Kegg Genome associated to UniProt ID and Kegg pathways. later it performe a comparison between proteins annotated at keeg and annotated at Reactome. From here is interesting for curators to search the evidence (publicatiosn) of proteins annotated at Kegg pathways and no reactome human pathways. 

Visualizations:
1) Venn diagram showing the annotated proteins in reactome human pathways and Kegg pathways. 

Tables:
1) association between uniportID, kegggenome and gegg pathways
2) map of counts of kegg pathways , list kegg pathways per kegg genome id. 
3) table of all the proteins no annotated at reactome pathways but yes at kegg pathways. 
'''
def analysis4(loadCopyNovember2017 = False, toWrite = False):

	print('''====================\nRunning -Analysis 4-\n====================\n'''+ time.strftime("%H:%M:%S"))

	#1 -Loading sources
	#print("Loading UniProt")
	df_up = uniprot.get_dfUniProtHR()

	#2 -Executing functions
	#print("Executing 'get_hsaList'")	
	listKegghsa = uniprot.get_hsaList(df_up)
	df_keggPathw = kegg.get_keggPathw(listKegghsa, loadCopyNovember2017 = loadCopyNovember2017, toWrite = toWrite)

	#print("Executing 'df_KeggReactomePathways'")
	df_KeggReactomePathways = reactome_stats.get_reactomeKeggPathwaysTable(df_up, df_keggPathw, toWrite = toWrite)

	#3 -Visualize data
	#print("Executing visualizations Venn Diagram")	
	listUniProtInKegg = (df_KeggReactomePathways[~df_KeggReactomePathways['KeggPathwaysID'].isnull()])['DB_Object_ID'].tolist()
	listUniProtInReactome = (df_up[~df_up['ReactomeID'].isin(['No at Reactome'])])['DB_Object_ID'].tolist()
	venn2([set(listUniProtInKegg), set(listUniProtInReactome)], set_labels = ('UniProtId \n at Kegg', 'UniProtId \n at Reactome'))
	plt.show()	

	print('Analysis 4 finished succesfully at' + time.strftime("%H:%M:%S"))
	listReturn = [df_keggPathw, df_KeggReactomePathways]

	return(listReturn)


'''
|==========|
|ANALYSIS 5|
|==========|

Function 'analysis 5' retrieve a list of all the annotated or no annotated ancestors and childs in reactome. In adition the GO tagged along this function with "[!]" means those annotated GO are not associated to biological, molecular or cellular component. <- to report to GOC or OLS. 

Visualizations:
1) Venn diagram between all the annotated ancestors in reactome, all the childs annotated at reactome and all the ancestors no annotated at reactome.

Tables:
1)list of ancestors no annotated (to add in reactome)
2) list of ancestors already annotated
3) list of children already annotated at reactome
4) table of counts of ancestors annotated or no annotated

'''
def analysis5(toWrite = False, loadCopyNovember2017 = False):

	print('''====================\nRunning -Analysis 5-\n====================\n'''+ time.strftime("%H:%M:%S"))

	#1 -Loading sources
	df_up = uniprot.get_dfUniProtHR()

	#2 -Executing functions
	#print("Extract in a list the GO from UniProt table associated to Reactome.") 
	listGO_unique = uniprot.get_listGOatReactome(df_up)

	#print("Get a list of ancestors of GO Id at Reactome, and write tables with ancestors annotated at Reactome and no annotated. ")
	getListAncestors = reactome_stats.get_ancestors(listGO_unique, toWrite = toWrite, loadCopyNovember2017 = loadCopyNovember2017) 

	#3 -Visualize data

	venn2(subsets = [len(set(getListAncestors[1])), len(set(getListAncestors[2])), len(set(getListAncestors[0]))], set_labels = ('Annotated at \n Reactome', 'No annotated at \n Reactome yet'))

	plt.show()

	print('Analysis 5 finished succesfully at' + time.strftime("%H:%M:%S"))

	#  listAncestorsConnectedDisconnected = [intersectionAncestorsChild, onlyAtReactome, notAtReactome, list_reactomeAncestors_unique,listDisconnectedGO]
	return(getListAncestors)

