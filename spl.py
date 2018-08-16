import json
import csv
import re
from bs4 import BeautifulSoup
from nltk import ngrams
import lxml.html
from lxml import etree
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom

from Monograph import ProductSummary
from Monograph import DrugMonograph

from spldataNDF import  NDFElement
from spldataNDF import SNOMED
from spldataNDF import SNOMED_MAP
from spldataNDF import  RXNNORM
from spldataNDF import  RXNREL

from spldata import SIDER
from spldata import AdverseReactionReport

from drug_api import DrugAPI


drugFiles = ['../spl/drug-label-0001-of-0007.json']##,
##'../spl/drug-label-0002-of-0007.json',
##'../spl/drug-label-0003-of-0007.json',
##'../spl/drug-label-0004-of-0007.json',
##'../spl/drug-label-0005-of-0007.json',
##'../spl/drug-label-0006-of-0007.json',
##'../spl/drug-label-0007-of-0007.json']

sider_indications = []
sider_se = []
snomed_terms = []
snomed_map_terms = []
rx_cui_dict = {}
rx_aui_dict = {}

## SPL DATA
product_data_array = []
unique_keys = {}
med_by_pharma = {}
drug_mono_array = []
drug_mono_dict = {}
drug_mono_rxcui_dict = {}
table_contents_file = open('../../PetOwnerPortal/DrugMonograph/monographs-toc.html','w')
table_contents_file_2 = open('../../PetOwnerPortal/DrugMonograph/monographs-toc-2.html','w')
table_contents_file_3 = open('../../PetOwnerPortal/DrugMonograph/monographs-toc-3.html','w')
table_contents_file_4 = open('../../PetOwnerPortal/DrugMonograph/monographs-toc-4.html','w')
table_contents_file_otc = open('../../PetOwnerPortal/DrugMonograph/monographs-otc.html','w')

cyp_adverse = open('adverse_interactions.txt','w')

## ONTOLOGIES
symptom_ontology = {}
med_by_pharma = {}
corpus_multi = {}
corpus_indications = {}
corpus_meddra = {}
drug_api_handle = DrugAPI('rxnorm')


def read_product_data():
	with open('../FDA-Monographs/SPL/SourceProcessFiles/product.txt',encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
		rowCount = 0
		for row in csvReader:
			rowCount = rowCount + 1
			if len(row) < 16:
				print('Less than 16')
				print(str(rowCount))
			elif len(row) < 15:
				print('Less than 15')
				print(str(rowCount))
			product_info = ProductSummary(row)
			if product_info.isValid == 'YES':
				product_data_array.append(product_info)
def write_html(drug_monograph, fileout):
	fileout.write('<div><table width=\"100%\">\n<tr>\n<th></th><th></th><th></th></tr>\n')
	fileout.write('<tr>\n<td>Generic Name</td><td><a href=\"./' + drug_monograph.monograph_id + '.html\">' + drug_monograph.generic_name + '</a></td></tr>')
	for brand in drug_monograph.brand_name:
		fileout.write('<tr><td>Brand Name</td><a href=\"./' + drug_monograph.monograph_id + '.html\">' + str(brand) + '</a>')
	fileout.write('<tr>\n<td>\n')
	for pharm_class in drug_monograph.pharm_class_epc:
		fileout.write(pharm_class + '<br>\n')
	for pharm_class_pe in drug_monograph.pharm_class_pe:
		fileout.write(pharm_class_pe + '<br>\n')
	for pharm_class_pe in drug_monograph.pharm_class_cs:
		fileout.write(pharm_class_pe + '<br>\n')
	for pharm_class_pe in drug_monograph.pharm_class_moa:
		fileout.write(pharm_class_pe + '<br>\n</td>\n')
	for rxcui_id in drug_monograph.rxcui:
		fileout.write('<td id="getRXCUI" onClick=\"getRXCUI(' + rxcui_id + ')\">RXCUI</td><td><a href=\"https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=' + rxcui_id + '&sources=ONCHigh\">' + rxcui_id + '</a></br>')

	fileout.write('</td>\n</tr>\n</table>\n</div>\n')
	fileout.write('<BR>\n')
def writeTOCheadersHMTL(fileout):
	fileout.write('<HTML>\n')
	fileout.write('<HEAD>\n')
	fileout.write('<script type=\"text/javascript\">\n')
	fileout.write('const request = new XMLHttpRequest();\n')
	fileout.write('function getRXCUI (rxid) {\n')
	fileout.write('		request.open(\'GET\', \'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=rxid&sources=ONCHigh\')\n')
	fileout.write('   		alert(\"rxcui alert called\")\n')
	fileout.write('   		request.onload = function() {\n')
	fileout.write('                		if (request.status == 200) {\n')
	fileout.write('                          		var info = JSON.parse(request.responseText);')
	fileout.write('			console.log(info);')		
	fileout.write('\n             }\n};\n}')
	fileout.write('</script>\n\n')
	fileout.write('<link rel=\"stylesheet\" type=\"text/css\" href=\"../style_sheets/monograph.css\">\n</head>')	
	fileout.write('<BODY>\n')
	fileout.write('<h1>FDA SPL Raw</h1>\n')
def writeTOCclosingHTML(fileout):

	fileout.write('</HTML>')	
def Rxcui_table_out(rxcui_dict):
	##print ('Called RXCui Table Out')
	wrote_drug_names_dic = {}
	drug_count = 0
	unique_rxcui_count = 0
	fileout_handle = table_contents_file
	fileout_handle.write('<HTML>\n')
	fileout_handle.write('<HEAD>\n')
	fileout_handle.write('<script type=\"text/javascript\">\n')
	fileout_handle.write('const request = new XMLHttpRequest();\n')
	fileout_handle.write('function getRXCUI (rxid) {\n')
	fileout_handle.write('		request.open(\'GET\', \'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=rxid&sources=ONCHigh\');\n')
	fileout_handle.write('   	alert(\"rxcui alert called\")\n')
	fileout_handle.write('   	request.onload = function() {\n')
	fileout_handle.write('                if (request.status == 200) {\n')
	fileout_handle.write('                          	var info = JSON.parse(request.responseText);')
	fileout_handle.write('			console.log(info);')		
	fileout_handle.write('\n             }\n};\n}')
	fileout_handle.write('</script>\n\n')
	fileout_handle.write('<link rel=\"stylesheet\" type=\"text/css\" href=\"../style_sheets/monograph.css\">\n</head>')
	fileout_handle.write('<BODY>')
	fileout_handle.write('<h1>FDA SPL Raw</h1>\n')
	##fileout_handle.write('<div><table width=\"100%\"><tr><th></th><th></th></tr>\n')

	for rxcuis in rxcui_dict:
		mono_array = []
		mono_array = rxcui_dict[rxcuis]

		best_drug_mono = mono_array[0]
		if best_drug_mono.product_type == 'HUMAN PRESCRIPTION DRUG':

			for mono in mono_array:
				drug_count = drug_count + 1
				keys_drugfields = mono.drugfields.keys()
				if mono.num_drug_keys > best_drug_mono.num_drug_keys:
					best_drug_mono = mono


			unique_rxcui_count = unique_rxcui_count + 1

			if unique_rxcui_count == 1000:
				writeTOCclosingHTML(fileout_handle)
				fileout_handle = table_contents_file_2
				writeTOCheadersHMTL(fileout_handle)

			elif unique_rxcui_count == 2000:
				writeTOCclosingHTML(fileout_handle)
				fileout_handle = table_contents_file_3
				writeTOCheadersHMTL(fileout_handle)

			elif unique_rxcui_count == 3000:
				writeTOCclosingHTML(fileout_handle)
				fileout_handle = table_contents_file_4
				writeTOCheadersHMTL(fileout_handle)


			write_html(best_drug_mono,fileout_handle)
		else: 
			for mono in mono_array:
				drug_count = drug_count + 1
				keys_drugfields = mono.drugfields.keys()
				if mono.num_drug_keys > best_drug_mono.num_drug_keys:
					best_drug_mono = mono

			write_html(best_drug_mono, table_contents_file_otc)

		best_drug_mono = None

	table_contents_file.close()
	table_contents_file_2.close()
	table_contents_file_3.close()
	table_contents_file_4.close()
	fileout_handle.close()

def ngram_analyze():

	loadCorpus()
	loadIndicationsCorpus()
	loadCorpusMEDDRA()

	ngram_data = {}
	drugs_by_id = {}
	counter = 0;
	no_pharm_count = 0
	rxcui_table = {}
	set_id_table = {}

	for drugSource in drugFiles:
		with open(drugSource) as json_file:
			data = json.load(json_file)
			for display_name in data['results']:
				drug_mono = DrugMonograph(display_name, corpus_multi, corpus_indications,corpus_meddra)
				drugs_by_id[drug_mono.set_id] = drug_mono
				if len(drug_mono.rxcui) > 0: 


					if drug_mono.rxcui in rxcui_table:

						mono_array = []
						mono_array = rxcui_table[rxcui_num]
						mono_array.append(drug_mono)
						rxcui_table[rxcui_num] = mono_array
					else:
						new_mono_array = []
						new_mono_array.append(drug_mono)
						rxcui_table[rxcui_num]= new_mono_array

				if drug_mono.adverse_reactions != None and len(drug_mono.adverse_reactions) > 0:
					for adverse in drug_mono.adverse_reactions:
						ngramresults = ngrams(adverse.split(),16)
						for words in ngramresults:
							if words in ngram_data:
								counter = int(ngram_data[words])
								counter = counter + 1
								ngram_data[words] = str(counter)
								if counter > 36:
									print (str(words) + ' adding another ngram list')
							else:
								ngram_data[words] = '1'


	for rxcui_elem in rxcui_table:
		mono_array  = rxcui_table[rxcui_elem]
		print ('RXCUI element:  ' + str(rxcui_elem))
		for mono in mono_array:
			print (mono.generic_name)

	for ngram_count_term in ngram_data:
		count = int(ngram_data[ngram_count_term])
		if count > 36:
			print (str(ngram_count_term) + ' -->  ' + str(ngram_data[ngram_count_term]))

def create_monographs():

	drugs_by_id = {}
	counter = 0;
	no_pharm_count = 0
	rxcui_table = {}
	set_id_table = {}

	loadCorpus()
	loadIndicationsCorpus()
	loadCorpusMEDDRA()

	for drugSource in drugFiles:
		with open(drugSource) as json_file:
			data = json.load(json_file)
			for display_name in data['results']:
				drug_mono = DrugMonograph(display_name, corpus_multi, corpus_indications,corpus_meddra)
				drugs_id = drug_mono.set_id
				drugs_by_id[drugs_id] = drug_mono

				if len(drug_mono.rxcui) > 0: 
					rxcui_compare =''
					for rxcui_num in drug_mono.rxcui:
						rxcui_compare = rxcui_compare + rxcui_num
						print('RXCUI: ' + str(rxcui_compare))

					if rxcui_compare in rxcui_table:
						mono_array = []
						mono_array = rxcui_table[rxcui_compare]
						mono_array.append(drug_mono)
						rxcui_table[rxcui_compare] = mono_array
					else:
						new_mono_array = []
						new_mono_array.append(drug_mono)
						rxcui_table[rxcui_compare]= new_mono_array

				if drug_mono.product_type == 'HUMAN PRESCRIPTION DRUG':
					print ('\n\n-------------------------------- ' + drug_mono.generic_name + '-----------------------------------------')
					print ('-----BRAND: ' + str(drug_mono.brand_name) + ' ---------')

					if len(drug_mono.cyp_text_raw) > 0:
						print ('-------CYP RAW TEXT--------')
						for text in drug_mono.cyp_text_raw:
							cyp_adverse.write(text + '\n')
					##else:
					##	print ('No cyp raw text')

					if len(drug_mono.regex_adverse_match_table_terms) > 0:
						print ('--ADVERSE MATCH TABLE---')
						for text in drug_mono.regex_adverse_match_table_terms:
							cyp_adverse.write(text + '\n')
					##else:
					##	print ('No adverse match table terms')

					if len(drug_mono.regex_adverse_analysis) > 0:
						print ('-------ADVERSE ANALYSIS--------')
						for text in drug_mono.regex_adverse_analysis:
							cyp_adverse.write(text + '\n')
					#3else:
					##	print ('No adverse analysis')


					if len(drug_mono.ddi_parsed) > 0:
						print ('------DDI PARSED--------')
						for text in drug_mono.ddi_parsed:
							cyp_adverse.write(text + '\n')
					##else:
					##	print ('No ddi')


	cyp_adverse.close()
	Rxcui_table_out(rxcui_table)

def loadIndicationsCorpus():

	strip_2_re = re.compile(r'([A-Za-z0-9\'\,\-\s\+]+)(\s?\r?\n?)')
	indication_re = re.compile(r'NLP_([A-Za-z0-9\s\-\']+)')

	with open('../FDA-Monographs/SPL/SourceProcessFiles/SIDER/meddra_all_label_indications.tsv') as corp:
		for line in corp:
			words = line.split('\t')
			results = strip_2_re.match(words[8])
			if results != None:
				match_term_groups = results.groups()
				term = results.group(1)
				stripterm = term.replace('\n','')
				dict_term = stripterm.lower()
				corp_indications_array = dict_term.split()
				if len(corp_indications_array) > 1:
					corpus_indications[dict_term] = corp_indications_array
				else:
					corpus_indications[dict_term] = 'meddra'
def loadCorpusMEDDRA():
	disease_find_re = re.compile(r'^([A-Za-z0-9\-\,\s]+)\s?\[Disease\/Finding\]')
	physio_effect_re = re.compile(r'^([A-Za-z0-9\-\,\s]+)\s?\[PE\]')
	strip_2_re = re.compile(r'([A-Za-z0-9\'\,\-\s\+]+)(\s?\r?\n?)')
	indication_re = re.compile(r'NLP_([A-Za-z0-9\s\-\']+)')

	with open('../FDA-Monographs/SPL/SourceProcessFiles/SIDER/meddra.tsv') as corp:
		line_count = 0
		for line in corp:
			line_count = line_count + 1
			words  = line.split('\t')
			results = strip_2_re.match(words[3])
			if results != None:
				match_groups = results.groups()
				term = results.group(1)
				stripterm = term.replace('\n', '')
				dict_term = stripterm.lower()
				corp_term_array = dict_term.split()
				if len(corp_term_array) > 1:
					corpus_meddra[dict_term] = corp_term_array
				else:
					corpus_meddra[dict_term] = 'basic-meddra'

		meddra_keys = corpus_meddra.keys()

		for key in corpus_meddra:
			term = key.split()
			if len(term) > 1:
				meddra_array_words = ''
				for word in term:
					if meddra_array_words != '':
						meddra_array_words = word
					else:
						meddra_array_words = meddra_array_words + ' '  + word
				##if meddra_array_words in corpus_multi:
				##	print ('Already in multi corpus: ' + meddra_array_words)
def loadCorpus():
	disease_find_re = re.compile(r'^([A-Za-z0-9\-\,\s]+)\s?\[Disease\/Finding\]')
	physio_effect_re = re.compile(r'^([A-Za-z0-9\-\,\s]+)\s?\[PE\]')
	strip_2_re = re.compile(r'([A-Za-z0-9\'\,\-\s\+]+)(\s?\r?\n?)')
	indication_re = re.compile(r'NLP_([A-Za-z0-9\s\-\']+)')

	with open('../FDA-Monographs/SPL/SourceProcessFiles/SIDER/meddra_all_label_se.tsv') as corp:
		line_count = 0
		for line in corp:
			line_count = line_count + 1
			words = line.split('\t')
			results = strip_2_re.match(words[6])
			if results != None:
				match_groups = results.groups()
				term = results.group(1)
				stripterm = term.replace('\n','')
				dict_term = stripterm.lower()
				corp_term_array = dict_term.split()
				if len(corp_term_array )> 1:
					corpus_multi[dict_term] = corp_term_array
				else:	
					corpus_multi[dict_term] = 'meddra'


	##with open('../FDA-Monographs/SPL/SourceProcessFiles/NDFRT_Public_2017.11.06/NDFRT_Public_2017.11.06_NUI.txt') as ndf_corp:
	##with open('../FDA-Monographs/SPL/SourceProcessFiles/normInflvarCorpus.data.2017','r') as corp:
def analyze_set_id(dict_drug):
	for set_id_num in dict_drug:
		print (dict_drug[set_id_num] + '--> ' + set_id_num)
def writeDefinitions():
	ndfrt_meta.write('Property Definitions\n\n')
	for pDef in ndf_property_definition:
		ndfrt_meta.write(pDef + ': ' + ndf_property_definition[pDef] + '\n')
	
	ndfrt_meta.write('\nRole Definitions\n\n')
	for rDef in ndf_role_definition:
		ndfrt_meta.write(rDef + ': ' + ndf_role_definition[rDef] + '\n')

	ndfrt_meta.write('\nKind Definitions\n\n')
	for kDef in ndf_kind_definition:
		ndfrt_meta.write(kDef + ': ' + ndf_kind_definition[kDef] + '\n')

	ndfrt_meta.write('\nAssociation Definitions\n\n')
	for assocDef in ndf_association_definition:
		ndfrt_meta.write(assocDef + ': ' + ndf_association_definition[assocDef]+'\n')

	ndfrt_meta.write('\nQualifier Definitions\n\n')
	for qualDef in ndf_qualifier_definition:
		ndfrt_meta.write(qualDef + ': ' + ndf_qualifier_definition[qualDef] + '\n')
def convertPropCodeToText(code_number):
	if code_number in ndf_property_definition:
		code_text = ndf_property_definition[code_number]
		return code_text
	elif code_number in ndf_role_definition:
		code_text = ndf_role_definition[code_number]
		return code_text
	elif code_number in ndf_association_definition:
		code_text = ndf_association_definition[code_number]
		code_text = code_text
		return code_text
	elif code_number in ndf_qualifier_definition:
		code_text = ndf_qualifier_definition[code_number]
		code_text = code_text 
		return code_text		
	elif code_number in ndf_kind_definition:
		code_text = ndf_kind_definition[code_number]
	else:
		return code_number
def parse_out_ndf_global_property_def(root):
	for child in root:
		if child.tag == 'propertyDef' or child.tag == 'roleDef' or child.tag == 'kindDef' or child.tag == 'associationDef' or child.tag == 'qualifierDef':
			meta = child.getchildren()
			code_key = ''
			name_key = ''
			for meta_item in meta:
				if meta_item.tag == 'name':
					name_key = meta_item.text
				elif meta_item.tag == 'code':
					code_key = meta_item.text
			if child.tag == 'propertyDef':
				ndf_property_definition[code_key] = name_key
			elif child.tag == 'roleDef':
				ndf_role_definition[code_key] = name_key
			elif child.tag == 'kindDef':
				ndf_kind_definition[code_key] = name_key
			elif child.tag == 'associationDef':
				ndf_association_definition[code_key] = name_key
			elif child.tag  == 'qualifierDef':
				ndf_qualifier_definition[code_key] = name_key
	writeDefinitions()
def write_ndf_concept(ndf_obj):
	ndfrt_file.write('\n\n---------------------------------------------------------------')
	ndfrt_file.write ('\nName: ' + ndf_obj.name + ' ---> ' + ndf_obj.code + ' [Kind:' +ndf_obj.kind+']\n')
	ndfrt_file.write('-----------------------------------------------------------------\n')
	ndfrt_file.write('May treat: ' + ndf_obj.treat_mesh_def + '\n')
	ndfrt_file.write('Effect: ' + ndf_obj.physiological_mesh_def + '\n')
	ndfrt_file.write('--------item properties------------\n')
	for item in ndf_obj.properties:
		ndfrt_file.write(item + ',  ' + ndf_obj.properties[item] + '\n')
	for mProp in ndf_obj.med_properties:
		ndfrt_file.write(mProp + ': ' + ndf_obj.med_properties[mProp])
	for r in ndf_obj.roles:
		ndfrt_file.write(r + ',  ' + ndf_obj.roles[r] + '\n')
	for concept in ndf_obj.concepts:
		ndfrt_file.write('CONCEPT: ' + concept + ',  ' + ndf_obj.concepts[concept] + '\n')
def write_RXCUI_batch():

	rx_keys = NDF_rxcui_dict.keys()

	for key in rx_keys:

		ndf_array = NDF_rxcui_dict[key]
		if len(ndf_array) > 5:
			ndfrt_file.write('RXCUI: ' + key)
			ndfrt_file.write('\n---------------------------')
			for ndf in ndf_array:
				for role in ndf.roles:

					if re.findall('may_treat',role) :
						code = ndf.roles[role]
						if code in disease_kinds:
							ndf_match_code = disease_kinds[code]
							ndf.roles[role] = ndf_match_code.name
							if ndf_match_code.mdef != 'None':
								ndf.treat_mesh_def = ndf_match_code.mdef

					elif re.findall('PE',role):
						code = ndf.roles[role]
						if code in physiological_kinds:
							print (ndf_match_code.name)
							##ndf = physiological_kinds[code]
							##ndf.roles[role] = ndf_match_code.name
						##	if ndf_match_code.mdef != 'None':
						##		ndf.physiological_mesh_def = ndf_match_code.mdef

					elif re.findall('effect_may_be_inhibited_by',role):
						code = ndf.roles[role]
						if code in drug_kinds:
							ndf_match_code = drug_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('has_MoA',role):
						code = ndf.roles[role]
						if code in mechanism_of_action_kinds:
							ndf_match_code = mechanism_of_action_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('CI_MoA',role):
						code = ndf.roles[role]
						if code in mechanism_of_action_kinds:
							ndf_match_code = mechanism_of_action_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('CI_with',role):
						code = ndf.roles[role]
						if code in disease_kinds:
							ndf_match_code = disease_kinds[code]
							ndf.roles[role] = ndf_match_code.name	

					elif re.findall('has_Ingredient',role):
						code = ndf.roles[role]
						if code in ingredient_kinds:
							ndf_match_code = ingredient_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('may_prevent',role):
						code = ndf.roles[role]
						if code in disease_kinds:
							ndf_match_code = disease_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('has_DoseForm ',role):
						code = ndf.roles[role]
						if code in dose_kinds:
							ndf_match_code = dose_kinds[code]
							ndf.roles[role] = ndf_match_code.name

					elif re.findall('induces ',role):
						code = ndf.roles[role]
						if code in disease_kinds:
							ndf_match_code = disease_kinds[code]
							ndf.roles[role] = ndf_match_code.name	
				write_ndf_concept(ndf)
				ndfrt_file.write ('\n')
def read_ndfrt():
	ndf_code_dict_count = {}
	tree = etree.parse('../NDFRT_Public_2017.11.06/NDFRT_Public_2017.11.06_TDE.xml') 
	root = tree.getroot()
	parse_out_ndf_global_property_def(root)

	for child in root:
		if child.tag != 'propertyDef' and child.tag != 'roleDef' and child.tag != 'kindDef' and child.tag != 'associationDef' and child.tag != 'qualifierDef':

			name = ''
			code = ''
			id = ''
			namespace = ''
			primitive = ''
			kind = ''
			role_properties = {}
			concept_properties = {}
			item_properties = {}
			association_properties = {}
			qualifier_properties = {}
		
			for elem in child:
				if elem.tag == 'name':
					name = elem.text
				elif elem.tag == 'code':
					code = elem.text
				elif elem.tag == 'id':
					id = elem.text
				elif elem.tag == 'namespace':
					namespace = elem.text
				elif elem.tag == 'primitive':
					primitive = elem.text
				elif elem.tag == 'kind':
					kind = elem.text
				elif elem.tag == 'definingConcepts':
					concepts = elem.getchildren()
					for concept in concepts:
						##print ('concept: ' + concept.text)
						if concept.tag == 'concept':
							final_name = convertPropCodeToText(concept.text)
							##print ('final name: ' + final_name)
							concept_properties[final_name] = concept.text

				elif elem.tag == 'definingRoles':
					defining_roles= elem.getchildren()

					for role in defining_roles:

						role_list = role.getchildren()
						defining_name = ''
						defining_val = ''

						for role_item in role_list: 
							if role_item.tag == 'name':
								defining_name = role_item.text
							elif role_item.tag == 'value':
								defining_val = role_item.text
							if defining_name != '' and defining_val != '':
								final_name = convertPropCodeToText(defining_name)
								role_properties[final_name] = defining_val

				elif elem.tag == 'properties':
					properties = elem.getchildren()
					for props in properties:
						if props.tag == 'property':
							theProps = props.getchildren()
							propName = 'NV'
							val = 'NV'
							for prop in theProps:
								if prop.tag == 'name':
									propName = prop.text
								elif prop.tag == 'value':
									val = prop.text
								if propName != '' and val != '':
									final_name = convertPropCodeToText(propName)
									item_properties[final_name] = val

			propObj = NDFElement(name,code,id,kind,item_properties)
			propObj.add_roles_concepts(role_properties, concept_properties)
			drug_kinds[propObj.code] = propObj
			NDF_term_objects.append(propObj)
			
			if propObj.rxcui != None and propObj.level != None and propObj.level  != 'VA Class':
				if propObj.rxcui in NDF_rxcui_dict:
					ndf_array = NDF_rxcui_dict[propObj.rxcui]
					ndf_array.append(propObj)
					NDF_rxcui_dict[propObj.rxcui] = ndf_array
				else:
					ndf_array = []
					ndf_array.append(propObj)
					NDF_rxcui_dict[propObj.rxcui] = ndf_array

			if propObj.level == 'None':
				if propObj.kind == 'DISEASE':
					disease_kinds[propObj.code] = propObj
				elif propObj.kind == 'PHYSIOLOGICAL_EFFECT':
					physiological_kinds[propObj.code] = propObj
				elif propObj.kind == 'THERAPEUTIC':
					therapeutic_kinds[propObj.code] = propObj
				elif propObj.kind == 'DOSE':
					dose_kinds[propObj.code] = propObj
				elif propObj.kind == 'MECHANISM_OF_ACTION':
					mechanism_of_action_kinds[propObj.code] = propObj
				elif propObj.kind == 'PHARMACOKINETICS':
					pharmacokinetics_kinds[propObj.code] = propObj
				elif propObj.kind == 'INGREDIENT':
					ingredient_kinds[propObj.code]= propObj

			elif propObj.level  == 'VA Class':
				ndf_va_class[propObj.code] = propObj

	rx_cui_ndf_keys = NDF_rxcui_dict.keys()

	for key in rx_cui_ndf_keys:
		ndf_elem_array = NDF_rxcui_dict[key]
		ndf_array_copy = []
		for NDF_element in ndf_elem_array:
			for concept in NDF_element.concepts:
				if concept in ndf_va_class:
					ndf_concept_match = ndf_va_class[concept]
					NDF_element.concepts[concept] = ndf_concept_match.name
			ndf_array_copy.append(NDF_element)
		NDF_rxcui_dict[key] = ndf_array_copy
def connect_DB():
	connection = pymysql.connect(host='localhost:3306',
                             user='root',
                             password='root',                             
                             db='simplehr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

read_product_data()
##create_monographs()	
ngram_analyze()
##drug_mono_rxcui_keys = drug_mono_rxcui_dict.keys()
##for rxcui_array_key in drug_mono_rxcui_keys:
##	monographs_array = drug_mono_rxcui_dict[rxcui_array_key]
##	num_rx = len(monographs_array)
##	monograph = monographs_array[0]
##	if num_rx > 5:
##		num_rx_str = str(num_rx)
##		print(num_rx_str)


## NDF Files
##ndfrt_file = open('ndfrt-format.txt','w')
##ndfrt_meta = open('NDFRT-Therapeutic-Class','w')
##NDF_term_objects = []
##ndc_keys = []
##ndf_objects = {}
##NDF_rxcui_dict = {}
##ndf_kind_definition = {}
##ndf_role_definition = {}
##ndf_property_definition = {}
##ndf_association_definition = {}
##ndf_qualifier_definition = {}
##disease_kinds = {}
##physiological_kinds = {}
##therapeutic_kinds = {}
##dose_kinds = {}
##mechanism_of_action_kinds = {}
##pharmacokinetics_kinds = {}
##ingredient_kinds = {}
##drug_kinds = {}
##ndf_va_class = {}



##spl_unclassified_section
##spl_product_data_elements
##set_id
##overdosage
##laboratory_tests
##effective_time
##clinical_studies
##do_not_use
##active_ingredient
##inactive_ingredient
##keep_out_of_reach_of_children


##version: 						33004		added
##effective_time: 					33004		added
##id: 							33004		added
##set_id: 						33004		added
##openfda: 						33004		OK
##spl_product_data_elements: 			33004		added
##package_label_principal_display_panel: 		32971			added
##description: 					30376			added
##dosage_and_administration: 			30772			added
##indications_and_usage: 				30878			added
##adverse_reactions: 					30060		added
##information_for_patients: 				21655			added
##contraindications: 					29997			added

##clinical_pharmacology: 				29625			added
##how_supplied: 					29644			added
##overdosage: 					27385			added
##pregnancy: 						23114			added
##pediatric_use: 					23293			added
##drug_interactions: 					22222			added
##nursing_mothers: 					21985			added



##carcinogenesis_and_mutagenesis_
	##and_impairment_of_fertility:		21224
##geriatric_use: 					19256
##precautions: 					19614
##warnings:						18855
##spl_unclassified_section: 				16868
##pharmacokinetics: 					15952
##adverse_reactions_table: 				14267
##mechanism_of_action: 				12164
##general_precautions: 				11385
##boxed_warning: 					11231
##use_in_specific_populations: 			10744
##nonclinical_toxicology: 				10128
##dosage_forms_and_strengths: 			10256
##clinical_pharmacology_table: 			10056
##warnings_and_cautions: 				10801
##clinical_studies_table: 				8497
##pharmacodynamics: 				9317
##storage_and_handling: 				8699
##dosage_and_administration_table: 			8620
##teratogenic_effects: 				8084
##laboratory_tests: 					6942
##drug_abuse_and_dependence: 			6601
##labor_and_delivery: 				6645
##spl_medguide: 					6598
##recent_major_changes: 				5524
##references: 						5677
##how_supplied_table:				5206
##pharmacokinetics_table: 				5355
##spl_patient_package_insert: 			3919
##drug_and_or_laboratory_test_interactions: 	3823
##animal_pharmacology_and_or_toxicology: 	3969
##nonteratogenic_effects: 				3208
##abuse: 						2335
##spl_medguide_table: 				2852
##controlled_substance: 				2581
##warnings_and_cautions_table: 			2190
##drug_interactions_table: 				2147		OK
##dependence: 				2174
##warnings_table: 				2098
##microbiology: 				2051
##spl_unclassified_section_table: 		1562
##recent_major_changes_table: 		1468
##description_table: 				1496
##inactive_ingredient: 			1149
##spl_patient_package_insert_table: 		1107
##microbiology_table: 			887
##pharmacodynamics_table: 			858
##precautions_table: 				797
##indications_and_usage_table:		725
##instructions_for_use: 			609
##use_in_specific_populations_table: 	600
##active_ingredient: 				551
##keep_out_of_reach_of_children: 		503
##information_for_patients_table: 		455
##pediatric_use_table: 			413
##dosage_forms_and_strengths_table: 	380
##patient_medication_information: 		366
##questions: 					363
##purpose: 					314
##pregnancy_or_breast_feeding: 		258
##instructions_for_use_table: 		234
##general_precautions_table: 		172
##geriatric_use_table: 			161
##other_safety_information: 			123
##stop_use: 					123
##do_not_use: 				120
##nonclinical_toxicology_table: 		117
##risks: 					102

##package_label_principal_display_panel_table: 				96
##contraindications_table: 							95
##carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table: 	85
##when_using: 								82
##ask_doctor: 									71
##overdosage_table: 								70
##storage_and_handling_table: 						64
##patient_medication_information_table: 					63
##pharmacogenomics: 57
##safe_handling_warning: 47
##boxed_warning_table: 41
##mechanism_of_action_table: 35
##laboratory_tests_table: 27
##components: 25
##references_table: 23
##disposal_and_waste_handling: 19
##information_for_owners_or_caregivers: 19
##drug_abuse_and_dependence_table: 18
##health_care_provider_letter: 17
##active_ingredient_table: 17
##pregnancy_table: 16
##ask_doctor_or_pharmacist: 15
##troubleshooting: 14
##purpose_table: 12
##user_safety_warnings: 12
##health_care_provider_letter_table: 12
##drug_and_or_laboratory_test_interactions_table: 12
##nonteratogenic_effects_table: 10
##abuse_table: 8
##veterinary_indications: 8
##inactive_ingredient_table: 8
##animal_pharmacology_and_or_toxicology_table: 7
##statement_of_identity: 6
##spl_indexing_data_elements: 3
##information_for_owners_or_caregivers_table: 3
##cleaning: 2
##when_using_table: 2
##intended_use_of_the_device: 2
##teratogenic_effects_table: 1
##statement_of_identity_table: 1
##safe_handling_warning_table: 1
##health_claim: 1
##risks_table: 1
##summary_of_safety_and_effectiveness: 1
##other_safety_information_table: 1
##calibration_instructions: 1
##dependence_table: 1
##environmental_warning: 1

class ADR_element:
	def __init__ (self,adr_term, adr_id, frequency):
		self.adr_term = adr_term
		self.adr_id = adr_id
		self.frequency = frequency
def parse_ADReCS():
	tree = etree.parse('./ADReCS_Drug_info.xml') 
	root = tree.getroot()

	for child in root:
		for elem in child:
			drug_name = ''
			drug_id = ''
			drug_description = ''
			drug_atc = ''
			drug_cas = ''
			drug_indications= ''
			drug_synonyms = []
			drug_adrs = [] 

			if elem.tag == 'DRUG_ID':
				drug_id = elem.text
			elif elem.tag == 'DRUG_NAME':
				drug_name = elem.text
				print ('-----------------------------------------')
				print('DRUG NAME: ' + drug_name)
				print ('-----------------------------------------\n')
			elif elem.tag == 'DESCRIPTION':
				drug_description = elem.text
				print('DESCRIPTION: ' + drug_description)
			elif elem.tag == 'ATC':
				drug_atc = elem.text
			elif elem.tag == 'INDICATIONS':
				drug_indications = elem.text
				print('\nINDICATIONS: ' + drug_indications)
			elif elem.tag == 'ADRs':
				adrs = elem.getchildren()
				adr_items = []
				for adr in adrs:
					if adr.tag == 'ADR':
						term = ''
						adr_id = ''
						adr_freq = '0'
						adr_item = adr.getchildren()
						for adr_detail in adr_item:
							if adr_detail.tag == 'ADR_TERM':
								term = adr_detail.text
							elif adr_detail.tag == 'ADRECS_ID':
								adr_id = adr_detail.text
							elif adr_detail.tag == 'FREQUENCY':
								adr_freq = adr_detail.text
						adr_term_obj = ADR_element(term,adr_id,adr_freq)
						adr_items.append(adr_term_obj)

				for adr_obj in adr_items:
					print ('-----------------------------------------')
					print (adr_obj.adr_term + ': ' + adr_obj.frequency)		
def readRXNCONSO():
	root_directory = '../UMSL/RxNorm_full_12042017/prescribe/rrf/'

	with open(root_directory+'RXNCONSO.RRF',encoding='ISO-8859-1') as csvDataFile:

		csvReader = csv.reader(csvDataFile,delimiter='|')

		for row in csvReader:

			rxn_concept = RXNNORM(row)
			rx_cui_dict[rxn_concept.rxn_cui] = rxn_concept

	with open(root_directory+'RXNREL.RRF',encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='|')
		for row in csvReader:
			rxn_rel = RXNREL(row)
			if rxn_rel.relation_type == 'CUI':
				cui_1 = rx_cui_dict[rxn_rel.rxn_cui_1 ]
				cui_2 = rx_cui_dict[rxn_rel.rxn_cui_2]
				print (cui_1.drug_name )
				print (rxn_rel.relation_text )
				print (cui_2.drug_name)
				print ('----------------')
def readSNOMED():

	snomed_file = open('./snomed-file.txt','w')

	root_directory = '../UMSL/SnomedCT_USEditionRF2_PRODUCTION_20170901T120000Z/'

	with open(root_directory+'/Documentation/tls_Icd10cmHumanReadableMap_US1000124_20170901.tsv',
		encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
		for row in csvReader:

			conc_id = row[0]
			module_id = row[3]
			ref_set_id = row[4]
			ref_comp_id = row[5]
			sct_name = row[6]
			map_group = row[7]
			map_priority = row[8]
			map_rule = row[9]
			map_advice = row[10]
			map_target = row[11]
			icd_name = row[12]
			map_cat_id = row[13]
			map_cat_Val = row[14]
			snomed_term = SNOMED(conc_id,module_id,ref_comp_id, sct_name, icd_name)
			snomed_terms.append(snomed_term)

	with open(root_directory +'Full/Refset/Map/der2_iisssccRefset_ExtendedMapFull_US1000124_20170901.txt',
		encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
		for row in csvReader:
			conc_id_2 = row[0]
			module_id_2 = row[3]
			refset_id_2 = row[4]
			referencedComponent_id = row[5]
			map_group_2 = row[6]
			map_priority_2 = row[7]
			map_rule_2 = row[8]
			map_advice_2 = row[9]
			map_target_2 = row[10]
			correlation_id_2 = row[11]
			map_category_id_2 = row[12]
			snomed_map = SNOMED_MAP(conc_id_2, module_id_2, refset_id_2,referencedComponent_id)
			snomed_map_terms.append(snomed_map)

	with open(root_directory+'Full/Refset/Metadata/der2_sssssssRefSet_MRCMDomainFull_US1000124_20170901.txt', 
		encoding ='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
		for row in csvReader:
			print ('---------------------------FULL DOMAIN---------------------')
			print ('ID: ' + row[0])
			print ('Module ID: ' + row[3])
			print ('Domain Constraint: ' + row[6])
			print ('Parent Domain: ' + row[7])
			print ('Proximal Primitive Constraint: ' + row[8])
			print ('Proximal Primitive Refinement: ' + row[9])
			pre_constraint = row[10]
			##split_pre_constrait = pre_constraint.split(',')
			re_pre_constraint = re.findall(r'\[\[.*?\]\]',pre_constraint)
			print ('Domain Template Pre-coordination')
			for constraint in re_pre_constraint:
				print ('C: ' + constraint)

			post_constraint = row[11]
			re_post_constraint = re.findall(r'\[\[.*?\]\]',post_constraint)
			print ('Domain template post-condition: ')
			print ('URL: ' + row[12])
			print ('\n\n')

	for snocone in snomed_terms:
		for snomed_map in snomed_map_terms:
			##print(snocone.conceptID + '  '  + snomed_map.conceptID_map)
			if snocone.conceptID == snomed_map.conceptID_map:
				##print ('Match map id to concept id')
				snomed_file.write ('\nRef Component Snomed: ' + snocone.refCompId + ' --> ' + snomed_map.refComponentID)
				snomed_file.write ('\nConcept ID Snomed: ' + snocone.conceptID + ' --> ' + snomed_map.conceptID_map)
				snomed_file.write ('\nModule Snomed: ' + snocone.moduleID+ ' --> ' + snomed_map.moduleID_map+'\n')
				snomed_file.write (snocone.sctName + '\n')
				snomed_file.write (snocone.icdName + '\n')
				snomed_file.write ('\n-------------------------------------------------\n')

	snomed_file.close()
def read_sider():
	with open('../SIDER/meddra_all_label_indications.tsv',encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
		for row in csvReader:
			indication =  SIDER(row)
			sider_indications.append(indication)			
def read_se():
	with open('../SIDER/meddra_all_label_se.tsv',encoding='ISO-8859-1') as csvDataFile:
		csvReader = csv.reader(csvDataFile,delimiter='\t')
def merge_spl_ndfrt():
	for med in drug_mono_array:
		if med.UMLS_CUI in ndf_objects:
			ndf_element = ndf_objects[med.UMLS_CUI]
			for ndf_prop in ndf_element.med_properties:
				print (ndf_prop + ' ' + ndf_element.med_properties[ndf_prop])
			for ndf_concept in ndf_element.concepts:
				print (ndf_concept + ' ' + ndf_element.concepts[ndf_concept])
def merge_indications_side():
	for med in drug_mono_array:
		print ('----------MEDICATION: ' + med.generic_name + '---------------------------\n')
		for se in sider_se:
			if se.cid_prim == med.UMLS_CUI:
				print ('Match UMLS from Drug Monograph to cid_prim ' + se.side_effect)
			elif se.cid_sec == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to cid_sec' + se.side_effect)
			elif se.concept_prim == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to concept_prim' + se.side_effect)
			elif se.concept_sec == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to concept_sec' + se.side_effect)
		for indication in sider_indications:
			if indication.cid_prim == med.UMLS_CUI:
				print ('Match UMLS from Drug Monograph to cid_prim' + indication.term_name_general)
			elif indication.cid_sec == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to cid_sec' + indication.term_name_general)
			elif indication.concept_prim == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to concept_prim' + indication.term_name_general)
			elif indication.concept_sec == med.UMLS_CUI:
				print('Match UMLS from Drug Monograph to concept_sec' + indication.term_name_general)
def printProperties():
	print('-------------------------------------------------------------------')
	print('PROPERTIES')
	print('-------------------------------------------------------------------')
	for property in property_definition:
		print (property + ' --> ' + property_definition[property])

	print('-------------------------------------------------------------------')
	print('ROLES')
	print('-------------------------------------------------------------------')
	for property in role_definition:
		print (property + ' --> ' + role_definition[property])

	print('-------------------------------------------------------------------')
	print('KIND')
	print('-------------------------------------------------------------------')
	for property in kind_definition:
		print (property + ' --> ' + kind_definition[property])
def regexTableData(parse_text):
	for text_parse in parse_text:
		text_clean_1 = re.sub(r'<[A-Z,a-z,0-9\s]+\/>','####\n',text_parse)
		text_clean_2 = re.sub(r'<[A-Z,a-z,0-9\s]+ \= [A-Z,a-z,0-9\"]+>','####\n',text_clean_1)
		text_clean_3 = re.sub(r'<[A-Z,a-z,0-9\s\=]+>','####\n',text_clean_2)

		return text_clean_3
def parse_adverse(adverse_text,outfile):

	multi_line_buffer = []

	for adverse_lines in adverse_text:
		adverse_terms = adverse_lines.split(',')
		for adverse in adverse_terms:
			text_adverse = adverse.split(' ')
			if len(text_adverse) > 3:
				multi_line_buffer.append(adverse)
			else:
				outfile.write(adverse + ' \n')

	for line in multi_line_buffer:
		line_elem = line.split(',')
		outfile.write(line + '\n')
		##for word in line_elem:
		##	print (word)
def parse_indications(indications_text,outfile):

	multi_line_buffer = []
	##print (indications_text)
	##for indication_lines in indications_text:
	##	indication_terms = indications_lines.split(',')

	##	for indication in indication_terms:
			##text_indication = indication.split(' ')
			##if len(text_indication) > 3:
			##	multi_line_buffer.append(indication)
			##else:
	##		outfile.write(indication + '\n')
def drug_mono_rxcui(drug_monograph):
	if drug_monograph.product_type == 'HUMAN PRESCRIPTION DRUG':
		rxcui_mono = drug_monograph.rxcui

		if rxcui_mono in drug_mono_rxcui_dict:
			rxcui_array = drug_mono_rxcui_dict[rxcui_mono]
			rxcui_array.append(drug_monograph)
			drug_mono_rxcui_dict[rxcui_mono] = rxcui_array
		else:
			rxcui_array = []
			rxcui_array.append(drug_monograph)
			drug_mono_rxcui_dict[rxcui_mono] = rxcui_array
def parse_faers():
	with open('drug-event-0001-of-0023.json') as json_file:
		data = json.load(json_file)
		for item in data['results']:
			adverse_keys = item.keys()
			adverse_report = AdverseReactionReport(item)
			##print ('------ADVERSE-------')
			for key in adverse_keys:
				if key == 'patient':
					patient_dict = item[key]
					if len(patient_dict['drug']) == 1:
						drug_indication = ''
						drug_admin = ''
						drug_dose_text = ''
						drug = patient_dict['drug'][0]
						medicinal_product = drug['medicinalproduct']
						if 'drugindication' in drug:
							drug_indication = drug['drugindication']
						if 'drugadministrationroute' in drug:
							drug_admin = drug['drugadministrationroute']
						if 'drugdosagetext' in drug:
							drug_dose_text = drug['drugdosagetext']
				
	
