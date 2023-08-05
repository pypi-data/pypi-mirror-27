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
import matplotlib as mpl
from matplotlib_venn import venn2
from matplotlib_venn import venn3
import matplotlib.patches as mpatches
import uniprot
import kegg
import reactomegraphdb
import goc 
import analysis
import random


'''
|===============================================|
| FUNCTIONS ANALYSIS 5: Gene Ontology ancestors |
|===============================================|

- reactome_stats.writeGOtable()
- reactome_stats.writeStats()
- reactome_stats.get_root_ancestors()
- reactome_stats.get_ancestors()

'''
def writeGOtable (listGOid, nameDf, df_GOConto, toWrite = True):

  df_ancestorX = df_GOConto[df_GOConto['GO_ID'].isin(listGOid)]

  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite = (folderPath+nameDf+".csv")  
    df_ancestorX.to_csv(pathToWrite, index = False)
    print ("Table is already available at: "+pathToWrite) 

def writeStats (list1, list2, list3, list4 , list5, toWrite = False):

  dfResults = pd.DataFrame({'allGOID_uniqueReactome':[len(list1)],'allGOancestors_fromGOReactome':[len(list2)],'n_GOIntersectionChildAndAncestors':[len(list3)],'n_GOonlyChildAtReactome':[len(list4)],'n_GOnotAtReactome':[len(list5)]})
  #Little summary table of the results
  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite = (folderPath+'\\output_a5_resultsAncestors.csv')
    dfResults.to_csv(pathToWrite)

    print ("Table is already available at: "+pathToWrite)

def get_root_ancestors ():

  ###*~*LOADING_ROOT_ANCESTORS*~*###

  url2 = "https://www.ebi.ac.uk/ols/api/ontologies/go/terms/roots"
  response2 = urllib.urlopen(url2)
  data2 = json.loads(response2.read())
  data2_embedded = data2['_embedded']

  list_data2_embedded_terms = data2_embedded['terms']

  list_root_id = []
  #counter2 = 1
  for i in list_data2_embedded_terms:
    if i['obo_id'] != None:
      root_id_n = i['obo_id']
      list_root_id.append(root_id_n)
      #counter2 = counter + 1 

  return(list_root_id) 

def get_ancestors (listReactome, toWrite = False, loadCopyNovember2017 = False):

  df_gocOnto = goc.get_gocAnnotation(loadCopyNovember2017 = loadCopyNovember2017)

  #print ("\nLoading main roots from GO "+time.strftime("%H:%M:%S")+"\n")

  ###*~*GET_ROOT_ANCESTORS*~*###

  listRootAncestors = get_root_ancestors()
  #print("There are " +str(len(listRootAncestors))+ "root ancestors")
  lenListGOReactome = len(listReactome)

  ###*~*GET_ANCESTORS*~*###
    
  listAncestors = []
  s_goReactome = listReactome
  listDisconnectedGO = []  


  for i in s_goReactome:

    listGOsearch = ["GO", i]
    iSearch = "_".join(listGOsearch)

    url = ("https://www.ebi.ac.uk/ols/api/ontologies/go/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F"+iSearch+"/ancestors?size=500")
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #1..._embedded
    data_embedded = data['_embedded']

    #"2...terms"
    list_data_embedded_terms = data_embedded['terms']

    #"3...get from list (items) -> obo_id"
    list_obo_id = []

    for ii in list_data_embedded_terms:

      if ii['obo_id'] != None:

        obo_id_n = ii['obo_id']
        #checkList
        list_obo_id.append(obo_id_n)
        #finalList
        listAncestors.append(obo_id_n) #<--- should I use symetric_difference rather than save all in one list?
        #counter = counter + 1 

    if (any(x in listRootAncestors for x in list_obo_id)) == False: #    if any of the ancestors is the root is a connected graph

      #print(len(list_obo_id))
      #print(list_obo_id)
      print ("[!]Something is wrong to arrive to the main ancestors of :"+iSearch)
      listDisconnectedGO.append(iSearch)

    lenListGOReactome = lenListGOReactome-1

    if lenListGOReactome%5000==0:

      print ("Processed "+str(lenListGOReactome)+" GO")

  listAncestorsUnique = set(listAncestors)

  list_reactomeGO_unique = []

  for i in listReactome:

    list_i = ['GO',i]
    list_reactomeGO_unique.append(":".join(list_i)) 

  list_reactomeAncestors_unique = list(set(listAncestorsUnique))

  intersectionAncestorsChild = list(set(list_reactomeGO_unique).intersection(set(list_reactomeAncestors_unique)))
  onlyAtReactome = list(set(list_reactomeGO_unique).difference(set(list_reactomeAncestors_unique))) #should be 0
  notAtReactome = list(set(list_reactomeAncestors_unique).difference(set(list_reactomeGO_unique)))  #this is the interesting list to fill at the DB

  listAncestorsConnectedDisconnected = [intersectionAncestorsChild, onlyAtReactome, notAtReactome, list_reactomeAncestors_unique,listDisconnectedGO]

  if toWrite == True:

    #print ("Writing lists and Statistics about ancestors "+time.strftime("%H:%M:%S"))

    writeGOtable(notAtReactome, 'ancestorNoAnnotatedAtReactome', df_gocOnto)
    writeGOtable(onlyAtReactome, 'GOId_ChilAtReactome', df_gocOnto)
    writeGOtable(intersectionAncestorsChild, 'GOId_ChildAndAncestorAtReactome', df_gocOnto)

    #print("Number of unique GO Id annotated at Reactome:")
    #print(len(listReactome))

    #print("Number of GO ancestor unique in Reactome:")
    #print(len(list_reactomeAncestors_unique))

    #print("Number of GO Id annotated at Reactome ancestor from other GO Id at Reactome")
    #print(len(intersectionAncestorsChild))

    #print("Number of GO Id only child annotated at Reactome")
    #print(len(onlyAtReactome))

    #print("Number of ancestors no at Reactome")
    #print(len(notAtReactome))
    #print(notAtReactome)

    writeStats(listReactome,list_reactomeAncestors_unique, intersectionAncestorsChild,onlyAtReactome, notAtReactome)

  return(listAncestorsConnectedDisconnected) 

'''
|===============================================|
| FUNCTIONS ANALYSIS 4: Kegg Pathways Coverage |
|===============================================|

- reactome_stats.df_keggPathw()
- reactome_stats.get_reactomeKeggPathwaysTable()

'''

def df_keggPathw(listKegg_i = None, toWrite = False, loadCopyNovember2017 = False):

  if loadCopyNovember2017 == True:

    #print ("\nLoading copy of Kegg map table at 29th November 2017 "+time.strftime("%H:%M:%S")+"\n")
    urlKeggGP = 'https://raw.githubusercontent.com/corinabioinformatic/Neo4J_at_Reactome/Analysis_4/output_a4_keggGenomekeggPathways.csv'
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

      #writeKeggGP = open('output_4a_keggGP.txt','w+')
      #writeKeggGP.write("KeggGenome\tn_KeggPathways\tKeggPathways"+"\n")
      #writeKeggGP.write(str(i)+"\t"+str(mini_nListKegg_unique)+"\t"+(";".join(miniListKegg_unique))+"\n")
      counter = counter + 1

    df_KeggGenomPath['KeggPathwaysID'] = list_KeggPath
    df_KeggGenomPath['n_KeggPathwaysID'] = list_nKeggPath
    
  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite = folderPath+"output_a4_keggGenomekeggPathways.csv"
    df_KeggGenomPath.to_csv(pathToWrite, index = False)

    print("File available at "+ pathToWrite)

  return(df_KeggGenomPath)


def get_reactomeKeggPathwaysTable (df_UniProt, df_KeggMapAll, toWrite = False):

  #print ("\nCreate merged table with Reactome and Kegg Pathways per UniProtID at "+time.strftime("%H:%M:%S")+"\n")

  #removing all the Kegg genome ids with no pathway associated
  df_KeggMap = df_KeggMapAll[~df_KeggMapAll['KeggPathwaysID'].isin([0])] 

  listUniProt_ID = []
  listKegg_ID = []
  listReactome_ID = []
  listProteinFamily = []

  lenUniprot = len(df_UniProt['DB_Object_ID'].tolist())
  #print(lenUniprot)

  #loop to create a dataframe with the mapp genome-proteins

  for i in range(0,len(df_UniProt['DB_Object_ID'].tolist())):

    keggId = df_UniProt.iloc[i]['KeggID']
    listKeggId = keggId.split(';')

    for j in listKeggId:

      listUniProt_ID.append(df_UniProt.iloc[i]['DB_Object_ID'])
      listKegg_ID.append(j)
      listReactome_ID.append(df_UniProt.iloc[i]['ReactomeID'])
      listProteinFamily.append(df_UniProt.iloc[i]['ProteinFamily'])

    lenUniprot = lenUniprot-1
    if lenUniprot%5000==0:
      print ("Processed "+str(lenUniprot)+" proteins")

  #print (time.strftime("%H:%M:%S"))

  df_UniProtUnfolded = pd.DataFrame({'DB_Object_ID':listUniProt_ID,'ReactomeID':listReactome_ID,'KeggGenomeId':listKegg_ID, 'ProteinFamily':listProteinFamily})

  #print(len(df_KeggMap['DB_Object_ID'].unique()))
  df_UniProtKeggPathways = pd.merge(df_UniProtUnfolded, df_KeggMap, how='inner', on = 'KeggGenomeId')


  #print('len table  unique')
  #print(len(df_UniProtKeggPathways.drop_duplicates()))
  #print('len Uniprot unique')
  #print(len(df_UniProtKeggPathways['DB_Object_ID'].unique()))
  df_KeggPathways =  df_UniProtKeggPathways[~df_UniProtKeggPathways['KeggPathwaysID'].isnull()].drop_duplicates()
  #print('len df kegg without duplicated rows')
  #print(len(df_KeggPathways.drop_duplicates()))
  #print("unique proteins with kegg pathway")
  #print(len(df_KeggPathways['DB_Object_ID'].unique()))
  #print(df_KeggPathways.iloc[0])
  df_KeggPathways2 = df_KeggPathways.loc[:,['DB_Object_ID','KeggPathwaysID', 'nKeggPathwaysID']].drop_duplicates()
  #print('len df kegg without duplicated rows excluding keggG')
  #print(len(df_KeggPathways2.drop_duplicates()))

  mylist = df_KeggPathways2['DB_Object_ID'].tolist()
  print("Duplicated values (two UniprotID with different size of Kegg pathways per Kegg genome associated):")
  print([k for k,v in Counter(mylist).items() if v>1])

  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite = (folderPath+'\\output_a4_keggGPReactome.csv')    
    df_UniProtKeggPathways.to_csv(pathToWrite, index = False)

    print("Data available at : "+pathToWrite)
    df_NoReactome = df_UniProtKeggPathways[df_UniProtKeggPathways['ReactomeID'].isin(['No at Reactome'])]
    df_NoReactomeYesKegg =  df_NoReactome[~df_NoReactome['KeggPathwaysID'].isnull()]
    pathToWrite2 = (folderPath+'\\output_a4_ProteinsNoAtReactomeYesKeggPath.csv')  
    print("Data available at : "+pathToWrite2)  
    #print(len(df_NoReactomeYesKegg['KeggGenomeId'].unique()))
    #number of proteins no at reactome, but with kegg pathway.
    #print(len(df_NoReactomeYesKegg['DB_Object_ID'].unique()))

    df_NoReactomeYesKegg.to_csv(pathToWrite2, index = False)

  return(df_UniProtKeggPathways) 

'''
|===============================================|
| FUNCTIONS ANALYSIS 3: Merged table counts and annotations  |
|===============================================|

- reactome_stats.get_worktable()
- reactome_stats.get_clusteredFamily_counts()
- reactome_stats.showBarPlot()
- reactome_stats.showBarPlotReactionsPerFamily()
- reactome_stats.get_dfUnfoldByReactome()
- reactome_stats.barplotReactionsFamily()
'''

def get_worktable(dfGOC= None, dfUniprot = None, df_KeggGP_0 = None, toWrite = False,loadCopyNovember2017 = False):

  if loadCopyNovember2017 == False:

    #print ("\nCreating merged table from multiple sources  STEP 1 at "+time.strftime("%H:%M:%S")+"\n")

    df_KeggGP_00 = df_KeggGP_0[~df_KeggGP_0['n_KeggPathwaysID'].isin([0])].drop_duplicates()
    df_KeggGP = df_KeggGP_00.loc[:,['DB_Object_ID']].drop_duplicates()
    df_KeggGP["WithKeggPathway"] = "yes"

    n_goBp = []
    n_goCc = []
    n_goMf = []
    n_goAll = []
    list_goBp = []
    list_goCc = []
    list_goMf = []
    list_goAll = []

    #2.- Subset df_UniProt curated to get only columns DBobject, prot family and ReactomeID and KEgg Id
    #>>> table to filter by human reviewed proteins  & to merge because it has PRotein family, KEggGenome, etc
    df_UniProt_subset = dfUniprot.loc[:,['DB_Object_ID', 'ProteinFamily', 'ReactomeID', 'KeggID']]
    #>>>table of GOC filtered by reviewed human proteins
    df_UniqueProtGOC = dfGOC[dfGOC['DB_Object_ID'].isin(df_UniProt_subset['DB_Object_ID'])]
    #>>> table of GOC which provides the main counts og GOIDs.
    #df_proteinsGOCAnnotation_n = df_UniqueProtGOC.groupby(['DB_Object_ID'])['GO_ID'].nunique().to_frame().reset_index().rename(columns= {'DB_Object_ID':'DB_Object_ID','GO_ID':'n_GO_ID'})

    listUniqueProtGOC = df_UniqueProtGOC['DB_Object_ID'].unique()
    counterProt = len(listUniqueProtGOC)

    for i in listUniqueProtGOC:

      counterProt = counterProt -1
      dfGOC_i = df_UniqueProtGOC[df_UniqueProtGOC['DB_Object_ID'].isin([i])]

      dfGOC_i_bp = len(dfGOC_i[dfGOC_i['Aspect'].isin(['P'])])
      dfGOC_i_cc = len(dfGOC_i[dfGOC_i['Aspect'].isin(['C'])])    
      dfGOC_i_mf = len(dfGOC_i[dfGOC_i['Aspect'].isin(['F'])])
      dfGOC_i_all= len(dfGOC_i)
      n_goBp.append(dfGOC_i_bp)
      n_goCc.append(dfGOC_i_cc)
      n_goMf.append(dfGOC_i_mf)
      n_goAll.append(dfGOC_i_all)

      dfGOC_i_bp_toList = (dfGOC_i[dfGOC_i['Aspect'].isin(['P'])])['GO_ID'].unique().tolist()
      dfGOC_i_cc_toList = (dfGOC_i[dfGOC_i['Aspect'].isin(['C'])])['GO_ID'].unique().tolist()   
      dfGOC_i_mf_toList = (dfGOC_i[dfGOC_i['Aspect'].isin(['F'])])['GO_ID'].unique().tolist()
      dfGOC_i_all_toList = (dfGOC_i['GO_ID'].unique().tolist())
      list_goBp.append(dfGOC_i_bp_toList)
      list_goCc.append(dfGOC_i_cc_toList)
      list_goMf.append(dfGOC_i_mf_toList)
      list_goAll.append(dfGOC_i_all_toList)

      if counterProt%5000==0:

        print ("\nProcessed "+str(counterProt)+" proteins")

    df_GOaspect = pd.DataFrame({"DB_Object_ID":df_UniqueProtGOC['DB_Object_ID'].unique().tolist()})
    #print("****CONTROL CHECK")
    #print(len(df_GOaspect))
    df_GOaspect['n_GOBP'] = n_goBp
    df_GOaspect['n_GOCC'] = n_goCc
    df_GOaspect['n_GOMF'] = n_goMf
    df_GOaspect['n_GOall'] = n_goAll
    df_GOaspect['list_GOBP'] = list_goBp
    df_GOaspect['list_GOCC'] = list_goCc
    df_GOaspect['list_GOMF'] = list_goMf
    df_GOaspect['list_GOAll'] = list_goAll

    #3.-Merge by column
    df_proteinsGOCAnnotation_nuu_fam_kegg_reactome = (df_UniProt_subset.merge(df_GOaspect, how='left', on= 'DB_Object_ID'))
    #print(len(df_proteinsGOCAnnotation_nuu_fam_kegg_reactome))

    df_proteinsGOCAnnotation_nu_fam_kegg_reactome = (df_proteinsGOCAnnotation_nuu_fam_kegg_reactome.merge(df_KeggGP, how='left', on= ['DB_Object_ID']))

    df_proteinsGOCAnnotation_nu_fam_kegg_reactome['list_GOAll'].fillna('-', inplace=True)
    df_proteinsGOCAnnotation_nu_fam_kegg_reactome['list_GOBP'].fillna('-', inplace=True)
    df_proteinsGOCAnnotation_nu_fam_kegg_reactome['list_GOCC'].fillna('-', inplace=True)
    df_proteinsGOCAnnotation_nu_fam_kegg_reactome['list_GOMF'].fillna('-', inplace=True)

    #print(len(df_proteinsGOCAnnotation_nu_fam_kegg_reactome))

    if toWrite == True:

      folderPath = os.getcwd()
      pathToWrite3 = folderPath+"output_a3_uniprotGOCcount.csv"

      print("Table write at "+pathToWrite3)
      df_proteinsGOCAnnotation_nu_fam_kegg_reactome.to_csv(pathToWrite3,index = False, sep = "\t")

    #print ("\nSuccesfully finished at  "+time.strftime("%H:%M:%S")+ " !")

  elif loadCopyNovember2017 == True:

    df_proteinsGOCAnnotation_nu_fam_kegg_reactome = pd.read_csv('https://raw.githubusercontent.com/corinabioinformatic/Neo4J_at_Reactome/ReactomeStats/Examples/input_loadCopyNovember2017/output_a3_uniprotGOCcount.csv', sep = "\t")

    if toWrite == True:

      folderPath = os.getcwd()
      pathToWrite3 = folderPath+"output_a3_uniprotGOCcount.csv"

      print("Table write at "+pathToWrite3)
      df_proteinsGOCAnnotation_nu_fam_kegg_reactome.to_csv(pathToWrite3,index = False, sep = "\t")

  return(df_proteinsGOCAnnotation_nu_fam_kegg_reactome)

def get_clusteredFamily_counts(df_fam_kegg_reactome, toWrite = False):

  #print ("\nCreating counts table from multiple sources  STEP 2 at "+time.strftime("%H:%M:%S")+"\n")

  listReactomeStatus = []
  listKeggStatus = []
  listProteinsOneGOStatus = []
  list_nProteinsFamily = []
  list_nProteinsFamilyAtReactom = []
  list_nProteinsFamilyNoAtReactome = []
  list_nProteinsFamilyAtKegg = []
  list_nProteinsFamilyNoAtKegg = [] 
  list_nGOperFamily = []
  list_nGOBPperFamily = []
  list_nGOCCperFamily = []
  list_nGOMFperFamily = []
  list_nProteinsOneGO = []
  listProteinsOneGO = []
  list_GOperFamily = []
  list_GOBPperFamily = []
  list_GOCCperFamily = []
  list_GOMFperFamily = []

  proteinFamilies = df_fam_kegg_reactome['ProteinFamily'].unique()
  #print("***CONTROL CHECK")
  #print(len(proteinFamilies))
  #print(len(df_fam_kegg_reactome['DB_Object_ID']))

  #print(len(df_fam_kegg_reactome['DB_Object_ID'].unique()))

  for family in proteinFamilies:
    #subset of all the proteins in a family:
    df_familyX = df_fam_kegg_reactome[df_fam_kegg_reactome['ProteinFamily'].isin([family])]

    #proteins at Reactome
    df_familyX_atReactome = df_familyX[~df_familyX["ReactomeID"].isin(['No at Reactome'])]
    df_familyX_NotAtReactome = df_familyX[df_familyX["ReactomeID"].isin(['No at Reactome'])]
    
    #proteins with just one GO annotated
    df_familyX_oneGOstatus = df_familyX.loc[df_familyX["n_GOall"].isin([1])]
    df_familyX_noOneGOstatus = df_familyX[~df_familyX["n_GOall"].isin(df_familyX_oneGOstatus['n_GOall'])]
    #print(df_familyX["list_GOAll"].tolist()) #df[1].fillna(0, inplace=True) ## df_UniProt['ProteinFamily'] = df_UniProt.ProteinFamily.replace(np.NaN, 'No Family assigned')
            
    s_goID = list(set(itertools.chain.from_iterable(df_familyX["list_GOAll"].tolist())))
    s_goIDBP = list(set(itertools.chain.from_iterable(df_familyX["list_GOBP"].tolist())))
    s_goIDCC = list(set(itertools.chain.from_iterable(df_familyX["list_GOCC"].tolist())))
    s_goIDMF = list(set(itertools.chain.from_iterable(df_familyX["list_GOMF"].tolist())))

    #proteins only withKegg Pathways
    df_familyX_withKeggPathways = df_familyX[df_familyX["WithKeggPathway"].isin(['yes'])]
    df_familyX_noKeggPathways = df_familyX[~df_familyX["WithKeggPathway"].isin(['yes'])]

    #1st CONDITIONAL 
    if ((len(df_familyX_atReactome) > 0) and (len(df_familyX_NotAtReactome) >0)):

      listReactomeStatus.append("Some")

    elif ((len(df_familyX_atReactome) == 0) and (len(df_familyX_NotAtReactome) >0)) :

      listReactomeStatus.append("None")

    elif ((len(df_familyX_atReactome) > 0) and (len(df_familyX_NotAtReactome) ==0)) :

      listReactomeStatus.append("All")

    else:

      break

    #2nd CONDITIONAL 
    if ((len(df_familyX_withKeggPathways) > 0) and (len(df_familyX_noKeggPathways) >0)) :

      listKeggStatus.append("Some")

    elif ((len(df_familyX_withKeggPathways) == 0) and (len(df_familyX_noKeggPathways) >0)) :

      listKeggStatus.append("None")

    elif ((len(df_familyX_withKeggPathways) > 0) and (len(df_familyX_noKeggPathways) ==0)) :

      listKeggStatus.append("All")

    else:

      break

    #3rd CONDITIONAL
    if ((len(df_familyX_oneGOstatus) > 0) and (len(df_familyX_noOneGOstatus) > 0)):

      listProteinsOneGOStatus.append("All")
      listProteinsOneGO.append(str(df_familyX_oneGOstatus['DB_Object_ID'].tolist()))
      list_nProteinsOneGO.append(len(df_familyX_oneGOstatus['DB_Object_ID'].tolist()))

    elif ((len(df_familyX_oneGOstatus) == 0) and (len(df_familyX_noOneGOstatus) > 0)):

      listProteinsOneGOStatus.append("None")
      listProteinsOneGO.append("-")
      list_nProteinsOneGO.append(0)

    elif ((len(df_familyX_oneGOstatus) > 0) and (len(df_familyX_noOneGOstatus) == 0)):

      listProteinsOneGOStatus.append("Some")
      listProteinsOneGO.append(str(df_familyX_oneGOstatus['DB_Object_ID'].tolist()))
      list_nProteinsOneGO.append(len(df_familyX_oneGOstatus['DB_Object_ID'].tolist()))

    else:

      break

    list_nProteinsFamily.append(len(df_familyX['DB_Object_ID']))
    list_nProteinsFamilyAtReactom.append(len(df_familyX_atReactome['DB_Object_ID']))
    list_nProteinsFamilyNoAtReactome.append(len(df_familyX_NotAtReactome['DB_Object_ID']))

    list_nProteinsFamilyAtKegg.append(len(df_familyX_withKeggPathways['DB_Object_ID']))
    list_nProteinsFamilyNoAtKegg.append(len(df_familyX_noKeggPathways['DB_Object_ID']))
    
    list_nGOperFamily.append(len(s_goID))
    list_nGOBPperFamily.append(len(s_goIDBP))
    list_nGOCCperFamily.append(len(s_goIDCC))
    list_nGOMFperFamily.append(len(s_goIDMF))

    list_GOperFamily.append(str(list(set(s_goID))))
    list_GOBPperFamily.append(str(list(set(s_goIDBP))))
    list_GOCCperFamily.append(str(list(set(s_goIDCC))))
    list_GOMFperFamily.append(str(list(set(s_goIDMF))))

  finalDf_h = pd.DataFrame(proteinFamilies, columns = ['ProteinFamily'])
  finalDf_h['atReactome'] = listReactomeStatus
  finalDf_h['atKegg'] = listKeggStatus  
  finalDf_h['oneGOIDperProtein'] = listProteinsOneGOStatus
  finalDf_h['n_proteinsPerFamily'] = list_nProteinsFamily
  finalDf_h['n_proteinsPerFamily_atReactome'] = list_nProteinsFamilyAtReactom
  finalDf_h['n_proteinsPerFamily_noReactome'] = list_nProteinsFamilyNoAtReactome
  finalDf_h['n_proteinsPerFamily_atKegg'] = list_nProteinsFamilyAtKegg
  finalDf_h['n_proteinsPerFamily_noKegg'] = list_nProteinsFamilyNoAtKegg  
  finalDf_h['n_GOIDperFamily'] = list_nGOperFamily
  finalDf_h['n_GOBPperFamily'] = list_nGOBPperFamily
  finalDf_h['n_GOCCperFamily'] = list_nGOCCperFamily
  finalDf_h['n_GOMFperFamily'] = list_nGOMFperFamily
  finalDf_h['n_proteinsWithOneGOId'] = list_nProteinsOneGO 
  finalDf_h['proteinsWithOneGOId'] = listProteinsOneGO #list_nProteinsOneGO
  finalDf_h['GOIDperfamily'] = list_GOperFamily
  finalDf_h['GOBPperfamily'] = list_GOBPperFamily
  finalDf_h['GOCCperfamily'] = list_GOCCperFamily
  finalDf_h['GOMFperfamily'] = list_GOMFperFamily

  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite4 = folderPath+"output_a3_family_GO_reactome_nprotCount.csv"

    finalDf_h.to_csv(folderPath, index = False)
    #print("Table write at "+pathToWrite4)
    #print ("\nSuccesfully finished at  "+time.strftime("%H:%M:%S")+ " !")


  return(finalDf_h)

def showBarPlot(table1, filterN = 50):

  #print ("\nBarplot from Families Table output of analysis 3 "+time.strftime("%H:%M:%S")+"\n")

  #Q1: barplot of all the family of proteins with proteins with at least one GO
  table1go = table1[~table1['n_proteinsWithOneGOId'].isin([0])]
  table1_groupedBy = table1go.sort_values(['n_proteinsWithOneGOId'], ascending = [False])

  height50 = (table1_groupedBy['n_proteinsWithOneGOId'].tolist())[0:filterN] #n_proteinsPerFamily
  
  bars50_unmodified = (table1_groupedBy['ProteinFamily'].tolist())[0:filterN] #ProteinFamily
  bars50 = []

  for i in bars50_unmodified:

    newString = i.replace('family', '')
    newString2 = newString.replace(',', '\n')
    bars50.append(newString2)

  y_pos = np.arange(len(bars50))

  # Create bars
  plt.bar(y_pos, height50, color = 'blue')
  plt.title('Top 50 families with some proteins with just one GO')

  # Create names on the x-axis
  plt.xticks(y_pos, bars50, rotation=90, size = 9)

  # Create labels
  position = range(1,len(bars50))

  # Text on the top of each barplot
  for i in range(len(position)):

    plt.text(x = position[i]-0.5 , y = height50[i], s = height50[i], size = 5)

  plt.show()

def showBarPlotReactionsPerFamily(table_ee, table_up, filterN = 50, normalized = False, toWrite = False):
  #table ee is reactionID per ee
  #print("underConstruction")
  #table_upr = table_up[table_up['ReactomeID'].isin(['No at Reactome'])]
  table_up_counts  = table_up.groupby(['ProteinFamily'])['DB_Object_ID'].nunique().to_frame().reset_index() #counts proteins per family
  #print("lenfamiliesUniprot")
  #print(len(table_up_counts))
  table_ee_up = table_up[table_up['DB_Object_ID'].isin(table_ee['DB_Object_ID'].unique())]
  #print(len(table_ee))
  #print(len(table_ee_up))
  table_ee_up_counts = table_ee_up.groupby(['ProteinFamily'])['DB_Object_ID'].nunique().to_frame().reset_index() #counts of DB_Object_ID at reactome for that protein family. 
  #print("lenfamiliesUniprotReactome")
  #print(len(table_ee_up_counts))  
  table_up_counts_toMerge = table_up_counts[table_up_counts['ProteinFamily'].isin(table_ee_up_counts['ProteinFamily'])]
  table_ee_up_counts['total_proteinsPerFamily'] = table_up_counts_toMerge['DB_Object_ID'].tolist()
  table_ee_up_counts['proteinsReactome/totalProteinsFamily'] = (table_ee_up_counts['DB_Object_ID']*100)/table_ee_up_counts['total_proteinsPerFamily']
  #print("unque normalized values")
  #print(table_ee_up_counts['proteinsReactome/totalProteinsFamily'].unique())

  mpl_fig = plt.figure()
  ax = mpl_fig.add_subplot(111)
  #print ("\nBarplot from Families Table output of analysis 3 at "+time.strftime("%H:%M:%S")+"\n")

  table_ee_up_counts_sorted = table_ee_up_counts.sort_values(by = 'DB_Object_ID', ascending = False)
  height50 = (table_ee_up_counts_sorted['DB_Object_ID'].tolist())[0:filterN] #n_proteinsPerFamily
  plt.title('Top 50 families with annotated proteins at Reactome')

  bars50_unmodified = (table_ee_up_counts_sorted['ProteinFamily'].tolist())[0:filterN] #ProteinFamily
  bars50 = []

  for i in bars50_unmodified:

    newString = i.replace('family', '')
    newString2 = newString.replace(',', '\n')
    bars50.append(newString2)

  y_pos = np.arange(len(bars50))

  # Create bars

  plt.bar(y_pos, height50, color = 'cyan')


  # Create names on the x-axis
  plt.xticks(y_pos, bars50, rotation=90 ,size = 8)
  ax.set_ylabel('Number of proteins per family')
  ax.set_xlabel('Protein Families')
  # Create labels
  position = range(1,len(bars50))

  # Text on the top of each barplot
  for i in range(len(position)):

    plt.text(x = position[i]-0.5 , y = height50[i], s = height50[i], size = 8)

  plt.show()

  #______________________________________________________________________

  mpl_fig = plt.figure()
  ax = mpl_fig.add_subplot(111)
  #print ("\nBarplot from Families Table output of analysis 3 at "+time.strftime("%H:%M:%S")+"\n")

  table_ee_up_counts_sort = table_ee_up_counts.groupby(['proteinsReactome/totalProteinsFamily'])['ProteinFamily'].nunique().to_frame().reset_index()

  table_ee_up_counts_sorted = table_ee_up_counts_sort.sort_values(by = 'proteinsReactome/totalProteinsFamily', ascending = False)  
  height50 = (table_ee_up_counts_sorted['proteinsReactome/totalProteinsFamily'].round(decimals=1).tolist()) #n_proteinsPerFamily
  plt.title('Top 50 families with annotated proteins at Reactome (normalized)')
  bars50 = table_ee_up_counts_sorted['ProteinFamily']

  y_pos = np.arange(len(bars50))

  # Create bars

  plt.bar(y_pos, height50, color = 'cyan')


  # Create names on the x-axis
  plt.xticks(y_pos, bars50, rotation=90 ,size = 9)
  ax.set_ylabel('(n proteins annotated at Reactome / Total n of proteins in that family)%')
  ax.set_xlabel('n of Protein Families')
  # Create labels
  position = range(1,len(bars50))

  # Text on the top of each barplot
  for i in range(len(position)):

    plt.text(x = position[i]-0.5 , y = height50[i], s = height50[i], size = 6, rotation = 90)

  plt.show()


  #______________________________________________________________________



  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite5 = folderPath+"output_a1_tableNormalizedTableProteinsperFamily.csv"

    print("Table write at "+pathToWrite5)
    table_ee_up_counts_sorted.to_csv(pathToWrite5, index = False, sep = "\t")

def get_dfUnfoldByReactome (tableUniProt):
  #print ("\nUnfolding UniProt table based on ReactomeID at "+time.strftime("%H:%M:%S")+"\n")

  listReactomeUnfolded = [] 
  listUniProtRep = []
  listFamilyProtRep = []

  lsRid = tableUniProt['ReactomeID'].tolist()
  lsUid = tableUniProt['DB_Object_ID'].tolist()
  lsFid = tableUniProt['ProteinFamily'].tolist()

  for i in range(0 ,len(tableUniProt)):

    strReactomeId = lsRid[i]
    listReactomeId = strReactomeId.split(";")
    listReactomeUnfolded = (listReactomeUnfolded + listReactomeId)

    for j in listReactomeId:

      listUniProtRep.append(lsUid[i])
      listFamilyProtRep.append(lsFid[i])


  df_unfoldedReactomeFamily = pd.DataFrame({'DB_Object_ID':listUniProtRep, 'ReactomeID':listReactomeUnfolded, 'ProteinFamily':listFamilyProtRep}).reset_index().drop_duplicates()

  return(df_unfoldedReactomeFamily) #at uniprot.py

def barplotReactionsFamily (tableReactome, tableUniProtUnfold):

  #print("ongoing...")
  listUniqueReactome = set(tableReactome['ReactionID'].tolist())
  #print(len(set(tableReactome['ReactionID'].tolist())))
  listUniqueUniProt = set(tableUniProtUnfold['ReactomeID'].tolist())
  #print(len(set(tableUniProtUnfold['ReactomeID'].tolist())))
  #print(intersect(listUniqueReactome, listUniqueUniProt))
  #search proteins involved and no involved. 
  df_countFamily = tableUniProtUnfold.groupby(['ProteinFamily'])['ReactomeID'].nunique().to_frame().reset_index()
  #print(df_countFamily)

  return(df_reactionsPerFamily)


'''
|===============================================|
| FUNCTIONS ANALYSIS 2: GO ontologies, GO annotations and GO Ids annotated at Reactome coverage. |
|===============================================|

- reactome_stats.venn2_compareRidsSources()
- reactome_stats.stackBarPlot_compareRidSources()
- reactome_stats.vennCoverage_3d()

'''

def venn2_compareRidsSources (tableGrouped, tableFilter, columnCompare = 'all', label1 = "A", label2 = "B"):

  mpl_fig = plt.figure()
  ax = mpl_fig.add_subplot(111)    
  #tableGroupedBy1 = tableGrouped.groupby(['TypeEvent'])['ReactomeID'].nunique().reset_index()

  tableFiltered = tableGrouped[tableGrouped['ReactomeID'].isin(tableFilter['ReactomeID'])]
  #tableGroupedBy2 = tableFiltered.groupby(['TypeEvent'])['ReactomeID'].nunique().reset_index()
  #column to be compared should be BlackBoxEvent, Depolymerisation, FailedReaction, Pathway, Polymarisation, Reaction, TopLevelPathway.
  #print(tableGrouped.iloc[0])
  #print(tableFiltered.iloc[0])  

  if (columnCompare in ['BlackBoxEvent','Depolymerisation' , 'FailedReaction','Pathway','Polymerisation','Reaction','TopLevelPathway']) == True:

    df1 = tableGrouped[tableGrouped['TypeEvent'].isin([columnCompare])]
    df2 = tableFiltered[tableFiltered['TypeEvent'].isin([columnCompare])]

    l1 = df1['ReactomeID'].unique().tolist()
    l2 = df2['ReactomeID'].unique().tolist()

    ax.set_title("Compare ReactomeID annotated at UniProt and ReactomeGraphDBv62")
    venn2([set(l1), set(l2)], set_labels = (label1, label2))
    plt.show()

    tableMerged = pd.merge(df1, df2, how = 'left')

    return(tableMerged)

  elif (columnCompare == 'all'):

    l1 = tableGrouped['ReactomeID'].unique().tolist()
    l2 = tableFiltered['ReactomeID'].unique().tolist()

    ax.set_title("Compare ReactomeID annotated at UniProt and ReactomeGraphDBv62")
    venn2([set(l1), set(l2)], set_labels = (label1, label2))
    plt.show()

    tableMerged = pd.merge(tableGrouped, tableFiltered, how = 'left')

    return(tableMerged)

  else:

    print('Please introduce a valid Type of Event to be compared')

def stackBarPlot_compareRidSources (tableGrouped, tableFilter, label1 = "A", label2 = "B"):

  mpl_fig = plt.figure()
  ax = mpl_fig.add_subplot(111)

  tableGroupedBy1 = tableGrouped.groupby(['TypeEvent'])['ReactomeID'].nunique().reset_index()
  tableGroupedBy1 = tableGroupedBy1.rename(columns = {'TypeEvent':'TypeEvent', 'ReactomeID':'n_ReactomeIDatGraphDB'})
  #print(tableGroupedBy1)
  tableFiltered = tableGrouped[tableGrouped['ReactomeID'].isin(tableFilter['ReactomeID'])]
  tableGroupedBy2 = tableFiltered.groupby(['TypeEvent'])['ReactomeID'].nunique().reset_index()
  tableGroupedBy2 = tableGroupedBy2.rename(columns = {'TypeEvent':'TypeEvent', 'ReactomeID':'n_ReactomeIDatUniProt'})
  #print(tableGroupedBy2)

  tableMerged = pd.merge(tableGroupedBy1, tableGroupedBy2 ,  on = 'TypeEvent', how = 'left')
  #print(tableMerged.iloc[0])

  #**********************************************
  # set width of bar
  barWidth = 0.25

  bars1 = tableMerged['n_ReactomeIDatGraphDB'].tolist()
  bars2 = tableMerged['n_ReactomeIDatUniProt'].tolist()

  # Heights of bars1 + bars2 (TO DO better)
  bars = (tableMerged['n_ReactomeIDatGraphDB']+tableMerged['n_ReactomeIDatUniProt']).tolist()
   
  # Set position of bar on X axis
  r1 = np.arange(len(bars1))
  r2 = [x + barWidth for x in r1]  

  # Make the plot
  plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label=label1)
  plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label=label2)

  # Add xticks on the middle of the group bars
  plt.xlabel('group', fontweight='bold')
  plt.xticks([r + barWidth for r in range(len(bars1))], tableMerged['TypeEvent'].unique().tolist(), rotation =45)

  # Create labels
  position = range(1,len(bars))

  ax.set_title("Compare ReactomeID annotated at UniProt and ReactomeGraphDBv62")
  ax.set_ylabel('Number of Reactome ID')
  ax.set_xlabel('Type of Reactome Event')

  ax.set_yscale('log')   
  # Create legend & Show graphic
  plt.legend()
  plt.show()

  #**********************************************
  return(tableMerged)

def vennCoverage_3d (table1, table2, table3, colname, vs1="A", vs2="B", vs3="C"):

  go_Term = (str(vs1)+" vs "+str(vs2)+" vs "+str(vs3))

  s1 = table1[colname].unique()
  s2 = table2[colname].unique()
  s3 = table3[colname].unique()

  out = venn3([set(s1),set(s2),set(s3)])#venn3(subsets = sets, set_labels = ('GOC experimental', 'Reactome', 'GOC no experimental'), alpha =1)

  if out.get_patch_by_id('100'):
    out.get_patch_by_id('100').set_color('lightskyblue')
  if out.get_patch_by_id('010'):    
    out.get_patch_by_id('010').set_color('blue')  
  if out.get_patch_by_id('001'):
    out.get_patch_by_id('001').set_color('cyan')  

  blue_patch = mpatches.Patch(color='lightskyblue', label=(vs1)) # ('+str(sets[0])+')'))
  lblue_patch = mpatches.Patch(color='blue', label=(vs2)) # ('+str(sets[1])+')'))
  cyan_patch = mpatches.Patch(color='cyan', label=(vs3)) #sss ('+str(sets[2])+')'))

  for text in out.set_labels:
      text.set_fontsize(0)

  plt.legend(handles=[blue_patch, lblue_patch, cyan_patch]) 

  plt.title(go_Term)
  plt.show()

  #np.setdiff1d(a, b)
  #np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])
  #numpy.concatenate((a1, a2, ...), axis=0)
  only_a = np.setdiff1d(s1,np.concatenate((s2,s3), axis = 0))
  only_b = np.setdiff1d(s2,np.concatenate((s1,s3), axis = 0))
  only_c = np.setdiff1d(s3,np.concatenate((s1,s2), axis = 0)) 
  ab = np.setdiff1d(np.intersect1d(s1,s2),s3)
  ac = np.setdiff1d(np.intersect1d(s1,s3),s2)
  bc = np.setdiff1d(np.intersect1d(s2,s3),s1)
  abc = np.intersect1d(s1,np.intersect1d(s2,s3))

  listVennSets= [only_a,only_b,only_c, ab, ac, bc, abc]

  return(listVennSets)


'''
|===============================================|
| FUNCTIONS ANALYSIS 2: GO ontologies, GO annotations and GO Ids annotated at Reactome coverage. |
|===============================================|

- reactome_stats.compareSources()

compare resources Reactome and UniProt

'''

def compareSources(tableReactome, tableUniProtAllh, drawVenn = True, drawPie = True, toWrite = False):

  #print ("\nComparing sources at  "+time.strftime("%H:%M:%S")+"\n")

  tableUniProtAllhr = tableUniProtAllh[tableUniProtAllh['Status'].isin(['reviewed'])]
  tableUniProtAllhr_withReactome = tableUniProtAllhr[~tableUniProtAllhr['ReactomeID'].isin(['No at Reactome'])]

  tableReactome_noAtUniProt = tableReactome[~tableReactome['DB_Object_ID'].isin(tableUniProtAllhr_withReactome['DB_Object_ID'].unique())]

  listNoHumanReviewedUniProtIDAtReactome = tableReactome_noAtUniProt['DB_Object_ID'].unique()
  s= ","
  strNoHumanReviewedUniProtIDAtReactome = s.join(listNoHumanReviewedUniProtIDAtReactome)
  url = "http://www.uniprot.org/uniprot/?query="+strNoHumanReviewedUniProtIDAtReactome+"&format=tab&columns=id,reviewed,genes(PREFERRED),database(Reactome),organism"
  df_Reactome_noAtUniProtHR = pd.read_csv(url,sep ="\t")
  df_Reactome_noAtUniProtHR_clean = df_Reactome_noAtUniProtHR[df_Reactome_noAtUniProtHR['Entry'].isin(listNoHumanReviewedUniProtIDAtReactome)]

  if toWrite == True:

    folderPath = os.getcwd()
    pathToWrite1 = folderPath+"output_a1_noHumanReviewedProteinsAtReactomeHumanPathways.csv"

    print("Table write at "+pathToWrite1)
    df_Reactome_noAtUniProtHR_clean.to_csv(pathToWrite1,index = False, sep = "\t")      

  if drawVenn == True :

    #VENN DIAGRAMM 1: comparing if all reactome proteins are already at UniProt human reviewed proteins. Coverage. 

    out = venn3(subsets = [set(tableReactome['DB_Object_ID'].tolist()), set(tableUniProtAllhr['DB_Object_ID'].tolist()), set(tableUniProtAllhr_withReactome['DB_Object_ID'].tolist())], set_labels = ('Reactome', 'UniProt/\nSwissProt', "Reactome\nand\nUniProt"))
    plt.title("UniProt ID annotated in different sources")

    plt.show()


  if drawPie == True:

    df_pie = df_Reactome_noAtUniProtHR_clean.groupby(['Status','Organism'])['Entry'].nunique().reset_index()
    df_pie_rev = df_pie[df_pie['Status'].isin(['reviewed'])]
    df_pie_unrev = df_pie[df_pie['Status'].isin(['unreviewed'])]

    group_names = df_pie['Status'].unique().tolist()
    group_size = [df_pie_rev['Entry'].sum(), df_pie_unrev['Entry'].sum()]

    listOrganismEntry = []

    for i in range(0,len(df_pie)):

      organism_i = df_pie['Organism'].tolist()[i] 
      nEntries_i = df_pie['Entry'].tolist()[i]  

      if nEntries_i > 8:

        listOrganismEntry.append(str(organism_i+"\n"+str(nEntries_i)))

      else:

        listOrganismEntry.append("")


    df_pie['OrganismEntry'] = listOrganismEntry
    subgroup_names = df_pie['OrganismEntry'].tolist() 
    subgroup_size = df_pie['Entry'].tolist()
     
    # Create colors
    a, b, c=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]
    #a, b=[plt.cm.Blues, plt.cm.Reds]
    # First Ring (outside)

    mpl.rcParams['font.size'] = 10.0  
    fig, ax = plt.subplots()
    ax.axis('equal')

    mypie, _ = ax.pie(group_size, radius = 1.3, labels = group_names, colors = [a(0.6), b(0.6)])
    plt.setp(mypie, width=0.3, edgecolor='white')
    
    # Second Ring (Inside)
    mypie2, _ = ax.pie(subgroup_size, radius = 1.3-0.3, labels = subgroup_names, labeldistance = 0.7, colors = [c(0.4)])
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0,0)
    ax.set_title("No human reviewed proteins annotated in Reactome human pathways")
    
    # show it
    plt.show()

  print("List of proteins annotated or no in different sources. Ready.")
  return(df_Reactome_noAtUniProtHR_clean)

