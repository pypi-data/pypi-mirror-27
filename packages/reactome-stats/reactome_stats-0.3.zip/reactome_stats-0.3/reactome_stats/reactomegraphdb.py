#Python 2.7
#Neo4J 3.2.3
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
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


'''
FUNCTION reactomegraphdb.neo4JCypher()
'''
def neo4JCypher (usernam , passwd, toWrite = False):

	driver = GraphDatabase.driver("bolt://localhost:7687", auth = basic_auth(usernam, passwd))
	session = driver.session()		

	if toWrite == False:

		#print ("\nStarting Neo4J session "+time.strftime("%H:%M:%S")+"\n")

		#1.-Sending query CYPHER
		result = session.run("""MATCH (p:Pathway {speciesName:{speciesName}})-[:hasEvent*]->(rle:ReactionLikeEvent),
		      (rle)-[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|hasComponent|hasMember|hasCandidate|repeatedUnit*]->(pe:PhysicalEntity),
		      (pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)
		RETURN DISTINCT re.identifier AS DB_Object_ID, rd.displayName AS Database, rle.stId AS ReactionID """, {"speciesName":"Homo sapiens"})

		#2.-Receiving answer in a new file:
		df_proteinUniProtPerReaction_all = pd.DataFrame([dict(record) for record in result])
		#print ("\nEnding Neo4J session "+time.strftime("%H:%M:%S")+"\n")
		session.close()

	if toWrite == toWrite:

		folderPath = os.getcwd()
		pathToWrite = (folderPath+"\\output_a1_pythonCypher_proteinID.csv") 
		df_proteinUniProtPerReaction_all.to_csv(pathToWrite, index = False) # path and file where you are going to save your results
		print("File available at "+ pathToWrite)
	df_proteinUniProtPerReaction = df_proteinUniProtPerReaction_all[df_proteinUniProtPerReaction_all['Database'].isin(['UniProt'])]

	return(df_proteinUniProtPerReaction)


'''
FUNCTION reactomegraphdb.get_elementEventReactome()
'''
#get from neo4J all the reactome elements and events to later merge with uniprot 
def get_elementEventReactome (usernam , passwd):

	driver = GraphDatabase.driver("bolt://localhost:7687", auth = basic_auth(usernam, passwd))
	session = driver.session()	
	#print ("\nStarting Neo4J session "+time.strftime("%H:%M:%S")+"\n")
	result = session.run("""MATCH (e:Event{speciesName:{speciesName}})
	RETURN DISTINCT e.schemaClass AS TypeEvent, e.stId AS ReactomeID""", {"speciesName":"Homo sapiens"})

	df_elementsEventsReactome = pd.DataFrame([dict(record) for record in result])
	session.close()

	return(df_elementsEventsReactome)

'''
FUNCTION reactomegraphdb.get_elementEventReactomeAll()
'''
#get from neo4J all the reactome elements and events to later merge with uniprot 
def get_elementEventReactomeAll (usernam , passwd):

	driver = GraphDatabase.driver("bolt://localhost:7687", auth = basic_auth(usernam, passwd))
	session = driver.session()

	#print("\nStarting Neo4J session at " + time.strftime("%H:%M:%S")+"\n")		

	result = session.run("""MATCH (p:Pathway{speciesName:"Homo sapiens"})-[:hasEvent*]->(rle:ReactionLikeEvent{speciesName:"Homo sapiens"})-[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity{speciesName:"Homo sapiens", isInDisease:FALSE})-[:referenceEntity]->(re:ReferenceEntity{databaseName:"UniProt"})
    RETURN DISTINCT p.stId AS ReactomeID,p.schemaClass, rle.stId AS ReactomeID_child,rle.schemaClass, re.identifier AS DB_Object_ID, re.databaseName""")

	df_elementsEventsReactome_all = pd.DataFrame([dict(record) for record in result])
	df_elementsEventsReactome = df_elementsEventsReactome_all[df_elementsEventsReactome_all["re.databaseName"].isin(["UniProt"])]
	df_elementsEventsReactome.to_csv("output_a1_elementEvent.csv", sep = "\t")
	session.close()

	return(df_elementsEventsReactome)
