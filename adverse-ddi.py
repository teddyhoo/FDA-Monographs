import json
import csv
import re
import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
from nltk import ngrams

drugFiles = ['drug-label-0001-of-0006.json']##,'drug-label-0002-of-0006.json','drug-label-0002-of-0006.json','drug-label-0003-of-0006.json','drug-label-0004-of-0006.json','drug-label-0005-of-0006.json','drug-label-0006-of-0006.json']
outfile= open('adverse.txt','w')
outfile2 = open('druginteractions.txt','w')

## Ontology
## Central Nervous System
##  Gastrointestinal System
## Cardiovascular System
## Psychiatric and Paradoxical Reactions
## Laboratories
## Renal
## CNS
## Soft Tissues
## Skeletal
## Gastrointestinal
##  Metabolic
## Cardiovascular Hypotension Tachycardia, chest pain, and palpitations
## Urinary System: Renal insufficiency, albuminuria, hematuria
## The following serious adverse reactions are discussed in greater detail in other sections of the labeling: •Thrombotic Thrombocytopenic Purpura/Hemolytic Uremic Syndrome [see Warnings and Precautions 
## The most common adverse reactions reported in at least one indication by > 10% of adult patients treated with valacyclovir hydrochloride tablets and more commonly than in patients treated with placebo are headache, nausea, and abdominal pain
## The adverse reactions reported by ≥ 5% of patients receiving valacyclovir hydrochloride tablets 1 gram twice daily for 10 days (n = 318) or oral acyclovir 200 mg 5 times daily for 10 days (n = 318), respectively, included headache (13%, 10%) and nausea (6%, 6%)
## The following adverse reactions have been associated with cromolyn sodium inhalation solution USP: cough, nasal congestion, nausea, sneezing and wheezing
## Extrapyramidal Symptoms
## Psychiatric Disorders
## The most frequent adverse experiences reported with the use of LIVOSTIN™ 0.05% (levocabastine hydrochloride ophthalmic suspension) were mild, transient stinging and burning (29%) and headache (5%)
## Other adverse experiences reported in approximately 1-3% of patients treated with LIVOSTIN™ were visual disturbances, dry mouth, fatigue, pharyngitis, eye pain/dryness, somnolence, red eyes, lacrimation/discharge, cough, nausea, rash/erythema, eyelid edema, and dyspnea
## Cardiovascular Effects Tachycardia, hypotension, and hypertension have been reported
## CNS Effects Extrapyramidal Symptoms (EPS) EPS during the administration of haloperidol have been reported frequently, often during the first few days of treatment
## Dystonia Class Effect: Symptoms of dystonia, prolonged abnormal contractions of muscle groups, may occur in susceptible individuals during the first few days of treatment
## Endocrine Disorders
##  Gastrointestinal Effects
## Angina pectoris, myocardial infarction, Raynaud syndrome, and congestive heart failure
## Tachycardia, chest pain, and palpitations
## dverse events that are clearly related to Betapace AF are those which are typical of its Class II (beta-blocking) and Class III (cardiac action potential duration prolongation) effects
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 
## 



def ddi_parse(ddi_text, drug_name, filename):

	ddi_re = re.compile(r'(\s[\([0-9]+\.[0-9\)]+\s)')
	ddi_elems = ddi_re.split(ddi_text)

	for elem in ddi_elems:
		find_cyp_marker(elem, drug_name, filename)
		filename.write(elem + '\n')



def find_cyp_marker(cyp_text,drug_name, filename):
	cyp_re_t = re.compile(r'(\w+) (^CYP\s?[A-Za-z0-9\s]{1,5}) (\w+)')
	cyp_re_t2 = re.compile(r'(\w+) (^cyp\s?[A-Za-z0-9\s]{1,5}) (\w+)')
	cyp_re_t3 = re.compile(r'(\w+) (^Cytochrome\s?[A-Za-z0-9\s]{1,5}) (\w+)')
	
	filename.write('---------------CYP DDI------------\n')
	filename.write(cyp_text + '\n')
	filename.write('------------------------------------\n')

	n = 12
	ngram_cyp = ngrams(cyp_text.split(),n)

	for grams in ngram_cyp:
		counter = 0
		word1 = ''
		word2 = ''
		word3 = ''
		word4 = ''
		word5 = ''
		word6 = ''
		word7 = ''
		word8 = ''
		word9 = ''
		word10 = ''
		word11 = ''
		word12 = ''


		for word in grams:
			if counter == 0:
				word1 = str(word)
			elif counter == 1:
				word2 = str(word)
			elif counter == 2:
				word3 = str(word)
			elif counter == 3:
				word4 = str(word)
			elif counter == 4:
				word5 = str(word)
			elif counter == 5:
				word6 = str(word)
			elif counter == 6:
				word7 = str(word)
			elif counter == 7:
				word8 = str(word)
			elif counter == 8:
				word9 = str(word)
			elif counter == 9:
				word10 = str(word)
			elif counter == 10:
				word11 = str(word)
			elif counter == 11:
				word12 = str(word)


			counter  = counter + 1

		
		if word4 == 'P450':
			filename.write(drug_name + ': [1]'  +word1 + '  [2]'  + word2 + ' [3]' + word3 + ' [4]' + word4 + ' [5]' + word5 + ' [6]' + word6 + ' [7]' + word7 + ' [8]' + word8 + ' [9]' + word9+ ' [10]' + word10+ ' [11]' + word11 + ' [12]' + word12 + '\n')

	results = cyp_re_t.match(cyp_text)
	if results != None:
		match_groups = results.groups()
		before = results.group(1)
		after = results.group(2)
		filename.write(drug_name + ': ' + before + '--> ' + after + '\n')

	results = cyp_re_t2.match(cyp_text)
	if results != None:
		match_groups = results.groups()
		before = results.group(1)
		after = results.group(2)
		filename.write(drug_name + ': ' + before + '--> ' + after + '\n')

	results = cyp_re_t3.match(cyp_text)
	if results != None:
		match_groups = results.groups()
		before = results.group(1)
		after = results.group(2)
		filename.write(drug_name + ': ' + before + '--> ' + after + '\n')


def parse_adverse(adverse_text, drug_name, filename):
	adverse = adverse_text

	match_adverse = 0

	adverse_r1 = re.compile(r'(the most frequent adverse reaction to) ([A-Za-z\s\-]+) (was) ([A-Za-z\s\-]+)')
	adverse_r2 = re.compile(r'(Most common adverse reactions \(\>[A-Za-z0-9]+\%\) are) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r3 = re.compile(r'(During or immediately after treatment,) ([A-Za-z0-9]+)')
	adverse_r4 = re.compile(r'(\(incidence \> [0-9\%]+\)) (are) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r5 = re.compile(r'(Most common adverse reactions in adults \(incidence ≥ [0-9\%]+\) are:) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r6 = re.compile(r'(The most frequent complaints reported related to the) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r7 = re.compile(r'(The most frequently reported adverse experiences in approximately [0-9\%]+ to [0-9\%]+ of patients are:) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r8 = re.compile(r'(The following adverse reactions have been reported to occur in more than [0-9\%]+ of patients on therapy with [A-Za-z\s\-]+ in controlled clinical trials, and may be causally related to the drug:) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r9 = re.compile(r'(Most common adverse reactions in adults \(incidence ≥ [0-9\%]+\) are:) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r10 = re.compile(r'(Most common adverse reactions in adults \(incidence ≥ [0-9\%]+\) are:) ([A-Za-z0-9\(\)\%\-\s\,]+)')
	adverse_r11 = re.compile(r'(Most common adverse reactions in adults \(incidence ≥ [0-9\%]+\) are:) ([A-Za-z0-9\(\)\%\-\s\,]+)')

	results = adverse_r1.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(4)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#1 Drug Name: ' + drug_name + ' ' + csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)

	results = adverse_r2.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#2 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r3.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#3 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r4.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(3)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#4 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r5.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#5 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r6.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#6 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r7.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#7 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)	
	results = adverse_r8.search(adverse)
	if results != None:
		match_groups = results.groups()
		csv_list_adverse = results.group(2)
		match_adverse = 1
		match_drugs.append(drug_name)
		print ('#8 Drug Name: ' + drug_name + ' ' +  csv_list_adverse + '\n')
		n = 4
		ngrams_results = ngrams(adverse.split(), n)
		for ngram in ngrams_results:
			print (ngram)
	if match_adverse == 0:
		no_match_drugs.append(drug_name)
		adverse_list = adverse.split('.\s')
		for adverse_item in adverse_list:
			outfile.write('-------ADVERSE' + generic_name + '------------\n')
			outfile.write(adverse_item + '\n')
				

no_match_drugs = []
match_drugs = []

for drugSource in drugFiles:
	with open(drugSource) as json_file:
		print ('OPEN FILE')
		adverse_reactions = ''
		drug_interaction = ''
		data = json.load(json_file)
		for display_name in data['results']:
			drug_keys= display_name.keys()
			drug_fda = display_name['openfda']
			generic_name = ''
			if 'generic_name' in drug_fda:
				generic_name = drug_fda['generic_name'][0]
				outfile.write('\n--------MED: '  + generic_name + ' -------------------------------------\n')

			if 'adverse_reactions' in drug_keys:
				adverse_reactions = display_name['adverse_reactions'][0]
				parse_adverse(adverse_reactions, generic_name, outfile)

			##if 'drug_interactions' in drug_keys:
			##	drug_interactions = display_name['drug_interactions'][0]
			##	outfile2.write('-------INTERACTIONS----------\n' + drug_interactions + '\n')
			##	outfile2.write('------------END----------------\n')
			##	ddi_parse(drug_interactions, generic_name, outfile2)

		print ('No match Adverse count: ' + str(len(no_match_drugs)))
		print ('Match adverse count: ' + str(len(match_drugs)))

