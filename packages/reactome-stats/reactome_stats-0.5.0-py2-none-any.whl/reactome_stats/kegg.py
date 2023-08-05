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
FUNCTION kegg.get_keggPathw()
'''
def get_keggPathw(listKegg_i = None, toWrite = False, loadCopyNovember2017 = False):

  if loadCopyNovember2017 == True:

    #print ("\nLoading copy of Kegg map table at 29th November 2017 "+time.strftime("%H:%M:%S")+"\n")
    urlKeggGP = 'https://raw.githubusercontent.com/corinabioinformatic/Neo4J_at_Reactome/ReactomeStats/Examples/input_loadCopyNovember2017/output_a4_keggGenomekeggPathways.csv'
    df_KeggGenomPath = pd.read_table(urlKeggGP, sep = ',')

  elif loadCopyNovember2017 == False:

    lenKegg = len(listKegg_i)
    counter = 0
    list_nKeggPath =[]
    list_KeggPath = []
    df_KeggGenomPath = pd.DataFrame({'KeggGenomeId':listKegg_i})

    for i in listKegg_i:
      #print(i)
      lenKegg = lenKegg-1
      if lenKegg%1000==0:

        print ("Processed "+str(counter)+" proteins")
        print("Working the other..."+str(lenKegg))
        print("listKegg"+str(len(list_KeggPath)))

      url = "http://rest.kegg.jp/link/pathway/"+i
      df_pathwaysKegg = pd.read_csv(url, sep = "\t",names= ["KeggID", "KeggPathID"])
      list_pathwaysKegg = df_pathwaysKegg["KeggPathID"].tolist()
      miniListKegg= []

      if len(list_pathwaysKegg) != 0:

        miniListKegg = miniListKegg + list_pathwaysKegg

      miniListKegg_unique = list(set(miniListKegg)) 
      mini_nListKegg_unique = len(miniListKegg_unique)

      list_KeggPath.append(";".join(miniListKegg_unique)) #list kegg pathways per uniprot ID
      list_nKeggPath.append(mini_nListKegg_unique) #number kegg pathways per uniprot ID

      counter = counter + 1

    df_KeggGenomPath['KeggPathwaysID'] = list_KeggPath
    df_KeggGenomPath['n_KeggPathwaysID'] = list_nKeggPath
    
  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite = folderPath+"output_a4_keggGenomekeggPathways.csv"
    df_KeggGenomPath.to_csv(pathToWrite, index = False)

    print("File available at "+ pathToWrite)

  return(df_KeggGenomPath)
