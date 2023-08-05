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
import goc
import kegg
import reactome_stats
#_____________________________________________________

def _vennCoverage_3d (table1, table2, table3, colname, vs1="A", vs2="B", vs3="C"):

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

def _vennDiagramGOReactomeCoverageAll_2d (tableGOC, tableReactome, vs1 = 'A', vs2 = 'B'):

  go_Term = (str(vs1)+" vs "+str(vs2))

  s1=tableGOC['ProteinFamily'].unique()
  s2=tableReactome['ProteinFamily'].unique()

  out = venn2([set(s1),set(s2)]) 
  
  if out.get_patch_by_id('10'):
    out.get_patch_by_id('10').set_color('lightskyblue') 
  if out.get_patch_by_id('01'):
    out.get_patch_by_id('01').set_color('blue') 
  if out.get_patch_by_id('11'):
    out.get_patch_by_id('11').set_color('cyan')

  for text in out.set_labels:
      text.set_fontsize(0)

  #create legend from handles and labels: 

  blue_patch = mpatches.Patch(color='lightskyblue', label=(vs1))# ('+str(sets[0])+')'))
  lblue_patch = mpatches.Patch(color='blue', label=(vs2))# ('+str(sets[1])+')'))
  cyan_patch = mpatches.Patch(color='cyan', label=(str(vs1)+' & '+str(vs2)))#sss ('+str(sets[2])+')'))

  plt.legend(handles=[blue_patch, lblue_patch, cyan_patch])

  plt.title(go_Term)
  plt.show()

  #np.setdiff1d(a, b)
  #np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])
  #numpy.concatenate((a1, a2, ...), axis=0)
  only_a = np.setdiff1d(s1, s2)
  only_b = np.setdiff1d(s2, s1)
  ab = np.intersect1d(s1, s2)

  dfIntersec = [only_a, only_b, ab]

  return(dfIntersec)

def _countGO (serieGO):

  listGO = []
  listOflist = serieGO.get_values()
  #print(listOflist[0])

  for i in listOflist:
    try:
      nGOs = len(i)
    except:
      ##print("no GO:  "+str(i))
      nGOs = 0
    listGO.append(nGOs)
  #print(listGO[0])
  #print("done!")

  return(listGO)

def _getSerieGOs (tableFam):

  s_BP = tableFam.GO_BP.str.findall(r'\[GO:([0-9]+)\]')
  s_CC = tableFam.GO_CC.str.findall(r'\[GO:([0-9]+)\]')
  s_MF = tableFam.GO_MF.str.findall(r'\[GO:([0-9]+)\]')
  s_allgo = tableFam.GO_ID.str.findall(r'GO:([0-9]+)')
  listSeries = [s_BP, s_CC, s_MF, s_allgo]

  return(listSeries)

def _addCountsToTable (tableFam, s_BPr, s_CCo, s_MFu, s_allg):

  tableFam['numberGO_BP_ID'] = pd.Series(countGO(s_BPr),index=tableFam.index)
  tableFam['numberGO_CC_ID'] = pd.Series(countGO(s_CCo),index=tableFam.index)
  tableFam['numberGO_MF_ID'] = pd.Series(countGO(s_MFu),index=tableFam.index)
  tableFam['total_GO_ID'] = pd.Series(countGO(s_allg),index=tableFam.index)

  tableFamSorted = tableFam.sort_values(by = ['total_GO_ID'], ascending = False)


  return(tableFamSorted)

def _getProtFamTable (tableToCount):
  #col1
  listLabelsFamilyBarPlot = tableToCount['ProteinFamily'].unique()

  listGoBPFamiliesBarPlot = []
  listGoCCFamiliesBarPlot = []
  listGoMFFamiliesBarPlot = []
  listAllGoFamiliesBarPlot = []

  numberProtPerFamily = []
  listNormGoBPFamiliesBarPlot = []
  listNormGoCCFamiliesBarPlot = []
  listNormGoMFFamiliesBarPlot = []  
  listNormAllGoFamiliesBarPlot = []

  for i in listLabelsFamilyBarPlot:

    df_family_i = tableToCount[tableToCount['ProteinFamily'].isin([i])]
    nProt = len(df_family_i['ProteinFamily'])
    #col2,3,4,5

    sumBP = df_family_i['numberGO_BP_ID'].sum()
    sumCC = df_family_i['numberGO_CC_ID'].sum()
    sumMF = df_family_i['numberGO_MF_ID'].sum()
    sumAll = df_family_i['total_GO_ID'].sum()

    normalizedValue_BP = round(float(sumBP)/float(nProt),1)
    normalizedValue_CC = round(float(sumCC)/float(nProt),1)
    normalizedValue_MF = round(float(sumMF)/float(nProt),1)
    normalizedValue_all = round(float(sumAll)/float(nProt),1)

    listGoBPFamiliesBarPlot.append(int(sumBP))
    listGoCCFamiliesBarPlot.append(int(sumCC))
    listGoMFFamiliesBarPlot .append(int(sumMF))
    listAllGoFamiliesBarPlot.append(int(sumAll))
    numberProtPerFamily.append(nProt)
    listNormGoBPFamiliesBarPlot.append(normalizedValue_BP)
    listNormGoCCFamiliesBarPlot.append(normalizedValue_CC)
    listNormGoMFFamiliesBarPlot.append(normalizedValue_MF)
    listNormAllGoFamiliesBarPlot.append(normalizedValue_all)


  dfFamilies = pd.DataFrame(listLabelsFamilyBarPlot, columns=['ProteinFamily'])

  dfFamilies['sumGO_BP_ID'] = listGoBPFamiliesBarPlot
  dfFamilies['sumGO_CC_ID'] = listGoCCFamiliesBarPlot
  dfFamilies['sumGO_MF_ID'] = listGoMFFamiliesBarPlot
  dfFamilies['sumAllGO_ID'] = listAllGoFamiliesBarPlot
  dfFamilies['numberProtPerFamily'] = numberProtPerFamily
  dfFamilies['normGOBP_ID'] = listNormGoBPFamiliesBarPlot
  dfFamilies['normGOCC_ID'] = listNormGoCCFamiliesBarPlot
  dfFamilies['normGOMF_ID'] = listNormGoMFFamiliesBarPlot
  dfFamilies['normAllGO_ID'] = listNormAllGoFamiliesBarPlot

  return (dfFamilies)

def _get_elemTuples (tableCounts, normaliz):

  labelsCounts = []
  listGoFamiliesBarPlot = []

  if normaliz == "no":

    dfFamilies_sorted = tableCounts.sort_values(by = ['sumAllGO_ID'], ascending = False).reset_index(drop=True)
    ##print(dfFamilies_sorted['sumAllGO_ID'][0:5])

    for j in range(0,len(dfFamilies_sorted['ProteinFamily'])):

      listGoFamiliesBarPlot.append((dfFamilies_sorted['sumGO_BP_ID'][j], dfFamilies_sorted['sumGO_CC_ID'][j] ,dfFamilies_sorted['sumGO_MF_ID'][j]))

    labelsCounts = [dfFamilies_sorted['ProteinFamily'], listGoFamiliesBarPlot, dfFamilies_sorted['sumAllGO_ID']]

  elif normaliz == "yes":

    dfFamilies_sorted = tableCounts.sort_values(by = ['normAllGO_ID'], ascending = False).reset_index(drop=True)
    ##print(dfFamilies_sorted['sumAllGO_ID'][0:5])

    for j in range(0,len(dfFamilies_sorted['ProteinFamily'])):

      listGoFamiliesBarPlot.append((dfFamilies_sorted['normGOBP_ID'][j], dfFamilies_sorted['normGOCC_ID'][j] ,dfFamilies_sorted['normGOMF_ID'][j]))

    labelsCounts = [dfFamilies_sorted['ProteinFamily'], listGoFamiliesBarPlot, dfFamilies_sorted['normAllGO_ID']]

  elif normaliz == "no-special":
    #df.sort(['c1','c2'], ascending=[False,True])
    #dfFamilies_sorted = tableCounts.sort_values(by = ['n_protAtReactome']).reset_index(drop=True)
    dfFamilies_sorted = tableCounts.sort(['n_protAtReactome','sumAllGO_ID'], ascending=[True, False]).reset_index(drop=True)
    ##print(dfFamilies_sorted['sumAllGO_ID'][0:5])

    for j in range(0,len(dfFamilies_sorted['ProteinFamily'])):

      listGoFamiliesBarPlot.append((dfFamilies_sorted['sumGO_BP_ID'][j], dfFamilies_sorted['sumGO_CC_ID'][j] ,dfFamilies_sorted['sumGO_MF_ID'][j]))

    labelsCounts = [dfFamilies_sorted['ProteinFamily'], listGoFamiliesBarPlot, dfFamilies_sorted['n_protAtReactome']]

  return(labelsCounts)

def _chooseBarplotReactomeGO (tableCountsTo, filter = 25, normalized = "no"):

  listBarPlot = get_elemTuples(tableCountsTo, normaliz = normalized)
  #listBarPlot_1[0],listBarPlot_1[1], listBarPlot_1[2]
  #print("!!!!!!")
  #print(len(listBarPlot))
  labels_all = listBarPlot[0] #legend
  elements_all = listBarPlot[1]
  tot_all = listBarPlot[2]
  
  #FILTERING TO PLOT SOME
  elements = elements_all[0:filter] #limit25
  ##print("========****")
  ##print(elements[0:10])
  label_full_0 = labels_all[0:filter] #limit25
  label_full =  [a.replace("family", "") for a in label_full_0] #limit25
  labels =[b.replace(" ", "\n") for b in label_full]  

  tot_filter = tot_all[0:filter]

  ##print(tot[0:10])
  df2 = pd.DataFrame.from_records(elements, columns=["GO Ids (BP)","GO Ids (CC)","GO Ids (MF)"]) #x axis, y axis colors
  

  #plt.xticks(ind, ('BBE', 'CandidateSet', 'Complex', 'DefinedSet', 'Depolymeristio', 'EWAS','FailedReaction','GenomeEncodedEntity','OpenSet','Pathway','Polymer','Polymerisation','Reaction', 'TopLevelPathway'), rotation =90)

  ax =df2.plot(kind='bar', stacked=True)  #df2!
  ax.set_xticklabels(labels,fontsize=6)

  if normalized == "no":
    ax.set_title('Number of GO IDs \n  per Protein Families')
  elif normalized == "yes":
    ax.set_title('Normalized number of GO IDs \n  per Protein Families')


  #for p in ax.patches:
  # ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
  #sumList = []
  #counter = 0

  #list number of GO per bar.

  listNgo = tot_filter
  counter = 0

  if normalized != "no-special":

    for p in ax.patches:

      if counter < len(listNgo): #list!

        #print("Axis=========")
        #print(p.get_x())
        #print(listNgo[counter]) 
        #print("=============")
        ax.annotate(listNgo[counter], 
          (p.get_x(),
          listNgo[counter]+(listNgo[counter]*0.05)), #put the number
          ha='left', 
          va='top').set_fontsize(8)#,
          #xytext=(0, 100),
          #textcoords='offset points').set_fontsize(10)

        counter = counter+1

  #plt.xticks(rotation=45)
  plt.show()
  #print("going...")

def _getProtFamInOutReactomeTable (tableToCount2):
  #col1
  listLabelsFamilyBarPlot = tableToCount2['ProteinFamily'].unique()

  listGoBPFamiliesBarPlot = []
  listGoCCFamiliesBarPlot = []
  listGoMFFamiliesBarPlot = []
  listAllGoFamiliesBarPlot = []

  numberProtPerFamily = []
  numberProtPerFamily_atR = []
  numberProtPerFamily_noR = []

  for i in listLabelsFamilyBarPlot:

    df_family_i = tableToCount2[tableToCount2['ProteinFamily'].isin([i])]
    df_R = df_family_i[~df_family_i['ReactomeID'].isnull()]
    df_nR = df_family_i[df_family_i['ReactomeID'].isnull()]

    nProt = len(df_family_i['ProteinFamily'])
    nProt_R = len(df_R['ReactomeID'])
    nProt_noR = len(df_nR['ReactomeID'])
    #col2,3,4,5

    sumBP = df_family_i['numberGO_BP_ID'].sum()
    sumCC = df_family_i['numberGO_CC_ID'].sum()
    sumMF = df_family_i['numberGO_MF_ID'].sum()
    sumAll = df_family_i['total_GO_ID'].sum()

    listGoBPFamiliesBarPlot.append(int(sumBP))
    listGoCCFamiliesBarPlot.append(int(sumCC))
    listGoMFFamiliesBarPlot .append(int(sumMF))
    listAllGoFamiliesBarPlot.append(int(sumAll))
    numberProtPerFamily.append(nProt)
    numberProtPerFamily_atR.append(nProt_R)
    numberProtPerFamily_noR.append(nProt_noR)

  dfFamilies = pd.DataFrame(listLabelsFamilyBarPlot, columns=['ProteinFamily'])

  dfFamilies['sumGO_BP_ID'] = listGoBPFamiliesBarPlot
  dfFamilies['sumGO_CC_ID'] = listGoCCFamiliesBarPlot
  dfFamilies['sumGO_MF_ID'] = listGoMFFamiliesBarPlot
  dfFamilies['sumAllGO_ID'] = listAllGoFamiliesBarPlot
  dfFamilies['numberProtPerFamily'] = numberProtPerFamily
  dfFamilies['n_protAtReactome'] = numberProtPerFamily_atR
  dfFamilies['n_protNoReactome'] = numberProtPerFamily_noR

  return (dfFamilies)

#______________________________________________________________________________________________________
