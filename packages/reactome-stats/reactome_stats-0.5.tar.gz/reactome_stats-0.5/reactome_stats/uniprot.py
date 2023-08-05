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
import urllib2
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
FUNCTION uniprot.get_dfUniProtHR()
'''
def get_dfUniProtHR():

  df_UniProt = pd.read_csv("http://www.uniprot.org/uniprot/?query=organism:9606+AND+reviewed:yes&format=tab&columns=id,reviewed,genes(PREFERRED),database(KEGG),database(Reactome),go(biological%20process),go(cellular%20component),go(molecular%20function),go-id,families",sep ="\t")

  df_UniProt = df_UniProt.rename(columns = {'Entry':'DB_Object_ID', 'Status':'Status',  'Gene names':'HGNCSymbol',  'Cross-reference (KEGG)':'KeggID',  'Cross-reference (Reactome)':'ReactomeID',  'Gene ontology (biological process)':'GO_BP', 'Gene ontology (cellular component)':'GO_CC', 'Gene ontology (molecular function)':'GO_MF', 'Gene ontology IDs':'GO_ID',  'Protein families':'ProteinFamily'})

  df_UniProt['ProteinFamily'] = df_UniProt.ProteinFamily.replace(np.NaN, 'No Family assigned')
  df_UniProt['ReactomeID'] = df_UniProt.ReactomeID.replace(np.NaN, 'No at Reactome')
  df_UniProt['KeggID'] = df_UniProt.KeggID.replace(np.NaN, 'No at Kegg')

  return(df_UniProt)


'''
FUNCTION uniprot.get_dfUniProtAllH()
'''
def get_dfUniProtAllH():

  df_uniprotAllH = pd.read_csv("http://www.uniprot.org/uniprot/?query=organism:9606&format=tab&columns=id,reviewed,genes(PREFERRED),database(Reactome)",sep ="\t")
  df_uniprotAllH = df_uniprotAllH.rename(columns = {'Entry':'DB_Object_ID', 'Status':'Status',  'Gene names':'HGNCSymbol', 'Cross-reference (Reactome)':'ReactomeID'})
  df_uniprotAllH['ReactomeID'] = df_uniprotAllH.ReactomeID.replace(np.NaN, 'No at Reactome')

  return(df_uniprotAllH)


'''
FUNCTION uniprot.get_dfUnfoldByReactome()
'''
def get_dfUnfoldByReactome(tableUniprot):

  #print ("\nUnfolding UniProt table based on ReactomeID at "+time.strftime("%H:%M:%S")+"\n")

  listReactomeUnfolded = [] 
  listUniProtRep = []
  listFamilyProtRep = []

  lsRid = tableUniprot['ReactomeID'].tolist()
  lsUid = tableUniprot['DB_Object_ID'].tolist()
  lsFid = tableUniprot['ProteinFamily'].tolist()

  for i in range(0 ,len(tableUniprot)):

    strReactomeId = lsRid[i]
    listReactomeId = strReactomeId.split(";")
    listReactomeUnfolded = (listReactomeUnfolded + listReactomeId)

    for j in listReactomeId:

      listUniProtRep.append(lsUid[i])
      listFamilyProtRep.append(lsFid[i])


  df_unfoldedReactomeFamily = pd.DataFrame({'DB_Object_ID':listUniProtRep, 'ReactomeID':listReactomeUnfolded, 'ProteinFamily':listFamilyProtRep}).reset_index().drop_duplicates()

  return(df_unfoldedReactomeFamily)


'''
FUNCTION uniprot.get_hsaList()
'''
def get_hsaList(tableUniprot):

  listKhsa =[]

  listKeggUnprocessed = tableUniprot['KeggID'].tolist()
  listKeggUnprocessed_1 = filter(None,listKeggUnprocessed)
  listKeggUnprocessed_2 = [ v for v in listKeggUnprocessed_1 if not v.startswith('No at Kegg') ] 

  for i in listKeggUnprocessed_2:

    i_GenomeKegg = filter(None,(i.split(";")))
    listKhsa = listKhsa+i_GenomeKegg

  return(listKhsa)     


'''
FUNCTION uniprot.get_listGOatReactome()
'''
def get_listGOatReactome(tableUniprot):

  #print ("Extracting individual GO Id from UniProt "+time.strftime("%H:%M:%S"))

  df_ReactomeGraphDB_GO = tableUniprot[~tableUniprot['ReactomeID'].isin(['No at Reactome'])] 
  listGO = []

  for i in df_ReactomeGraphDB_GO['GO_ID'].tolist():
    ###>>>> THIS PART OF THE FUNCTION CAN BE DONE BYSPLIT RATHER THAN REGEX
    valGO = str(i)

    if valGO != "":

      regex = r'GO:([0-9]+)'
      s_ID = re.findall(regex, valGO)
      listGO = (listGO + s_ID)

  listGO_unique = list(set(listGO)) 

  #print ("\nFinished succesfully at "+time.strftime("%H:%M:%S"))

  return(listGO_unique) 



