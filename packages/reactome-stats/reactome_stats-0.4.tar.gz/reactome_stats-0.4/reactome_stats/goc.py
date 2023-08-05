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
FUNCTION goc.get_gocOntology()
'''
def get_gocOntology(loadCopyNovember2017 = False):

	if loadCopyNovember2017 == True:

		#print ("Loading GO Ontologies from November 2017 at "+time.strftime("%H:%M:%S"))

		df_GOContologies = pd.read_csv("https://raw.githubusercontent.com/corinabioinformatic/Neo4J_at_Reactome/Analysis_2/output_a2_allGOfromOWLfile.csv",sep ="\t")

		#print ("\nFinished succesfully at "+time.strftime("%H:%M:%S")+ "!")

		return(df_GOContologies)

	elif loadCopyNovember2017 == False:

		#print ("Loading the up-to-date GO ontologies file at "+time.strftime("%H:%M:%S"))

		target_url = urlopen("http://purl.obolibrary.org/obo/go.owl")
		zipfile  = ZipFile(StringIO(target_url.read()))
		data = zipfile.open('go.owl_2017-10-31.rdf').readlines()
		listClassesGO = []
		listAspectGO = []
		counter = 0

		for line in data: # files are iterable

		  matchObj =re.search(r'<owl:Class rdf:about="http://purl.obolibrary.org/obo/GO_(.*)">' ,line)
		  matchObj2 =re.search(r'<oboInOwl:hasOBONamespace rdf:datatype="http://www.w3.org/2001/XMLSchema#string">(molecular_function|biological_process|cellular_component)</oboInOwl:hasOBONamespace>' ,line)
		  matchObj3 =re.search(r'<owl:deprecated rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</owl:deprecated>' ,line)  

		  if (matchObj) and (counter ==0):

		    goToAppend = ("GO:"+str(matchObj.group(1)))
		    listClassesGO.append(goToAppend)
		    counter = counter + 1

		  elif (matchObj2) and (counter ==1):

		    goToAppend2 = str(matchObj2.group(1))
		    listAspectGO.append(goToAppend2)
		    counter = counter - 1

		  elif (matchObj) and (counter ==1):
		    
		    listAspectGO.append("")
		    goToAppend = ("GO:"+str(matchObj.group(1)))
		    listClassesGO.append(goToAppend)

		df_GOContologies = pd.DataFrame({'GO_ID':listClassesGO,'Aspect':listAspectGO})
		#print ("\nFinished succesfully at "+time.strftime("%H:%M:%S")+ "!")

		return(df_GOContologies)  #at goc

'''
FUNCTION goc.get_gocAnnotation()
From here it is interesting to see if in the new version is it any deprecated value. Check by typeSet 'deprecated' if it is any deprecated GO
'''
def get_gocAnnotation(loadCopyNovember2017 = False, typeSet = 'all'):

	if loadCopyNovember2017 == True:

		df_GOC_prot = pd.read_csv("https://github.com/corinabioinformatic/Neo4J_at_Reactome/raw/Analysis_2/input_a2_goa_human_1.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.2
		df_GOC_cplx = pd.read_csv("https://github.com/corinabioinformatic/Neo4J_at_Reactome/raw/Analysis_2/input_a2_goa_human_2complex.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.3
		df_GOC_rna = pd.read_csv("https://github.com/corinabioinformatic/Neo4J_at_Reactome/raw/Analysis_2/input_a2_goa_human_3rna.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.4
		df_GOC_isof = pd.read_csv("https://github.com/corinabioinformatic/Neo4J_at_Reactome/raw/Analysis_2/input_a2_goa_human_4isoform.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])

		df_gocAnnotation = pd.concat([df_GOC_prot,df_GOC_cplx, df_GOC_rna,df_GOC_isof])

	elif loadCopyNovember2017 == False:

		df_GOC_prot = pd.read_csv("http://geneontology.org/gene-associations/goa_human.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.2
		df_GOC_cplx = pd.read_csv("http://geneontology.org/gene-associations/goa_human_complex.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.3
		df_GOC_rna = pd.read_csv("http://geneontology.org/gene-associations/goa_human_rna.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])
		#Table 1.B.4 from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/
		df_GOC_isof = pd.read_csv("ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human_isoform.gaf.gz", compression='gzip', sep='\t', comment='!', names = ["DB","DB_Object_ID","DB_Object_Symbol","Qualifier","GO_ID","DB:Reference","EvidenceCode","With(or)From","Aspect","DB_Object_Name","DB_Object_Synonym","DB_Object_Type","Taxon","Date","Assigned_By","Annotation_Extension","Gene_Product_Form_ID"])

		df_gocAnnotation = pd.concat([df_GOC_prot,df_GOC_cplx, df_GOC_rna,df_GOC_isof])


	#print ("\nRetrieving GOC annotation filtered by "+ typeSet +"at "+time.strftime("%H:%M:%S")+ "!")

	if typeSet == 'all' :

		df_GOC_Uniprot  = df_gocAnnotation

		return(df_GOC_Uniprot)

	elif typeSet == 'uniprot' :

		df_GOC_Uniprot  = df_gocAnnotation[df_gocAnnotation['DB'].isin(['UniProtKB'])]

		return(df_GOC_Uniprot)

	elif typeSet == 'curated' :

		df_GOC_Uniprot  = df_gocAnnotation[df_gocAnnotation['DB'].isin(['UniProtKB'])]  
		df_GOC_UniProt_curated = df_GOC_Uniprot[~df_GOC_Uniprot['EvidenceCode'].isin(['IEA'])]

		return(df_GOC_UniProt_curated)

	elif typeSet == 'iea' :

		df_GOC_Uniprot  = df_gocAnnotation[df_gocAnnotation['DB'].isin(['UniProtKB'])]
		df_GOC_UniProt_iea = df_GOC_Uniprot[df_GOC_Uniprot['EvidenceCode'].isin(['IEA'])]

		return(df_GOC_UniProt_iea)

	elif typeSet == 'deprecated' :

		df_GOC_Uniprot  = df_gocAnnotation[df_gocAnnotation['DB'].isin(['UniProtKB'])]
		df_GOC_UniProt_deprec = df_GOC_Uniprot[df_GOC_Uniprot['Aspect'].isnull()]

		return(df_GOC_UniProt_deprec)

	else:

		print("'typeSet' introduced no valid.\n Please introduce one of the next options: \n\t0) 'all'\n\t1) 'curated' \n\t2) 'uniprot' \n\t3) 'iea'")