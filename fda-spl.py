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
from spldata import ProductSummary
from spldata import DrugMonograph



drugFiles = ['./SourceProcessFiles/drug-label-0001-of-0006.json',
'./SourceProcessFiles/drug-label-0002-of-0006.json',
'./SourceProcessFiles/drug-label-0003-of-0006.json',
'./SourceProcessFiles/drug-label-0004-of-0006.json',
'./SourceProcessFiles/drug-label-0005-of-0006.json',
'./SourceProcessFiles/drug-label-0006-of-0006.json']


product_data_array = []
unique_keys = {}
med_by_pharma = {}
drug_mono_array = []
drug_mono_dict = {}
drug_mono_rxcui_dict = {}
table_contents_file = open('monographs-toc.html','w')

drugFields = {}

## IDENTIFICATION - SPL, PACKAGE LABELING, ID
drugFields['openfda'] = 'None'			## 114,337
drugFields['id'] = 'None'				## 114,337
drugFields['version'] = 'None'			## 114,337
drugFields['spl_medguide'] = 'None' 			##    9,296
drugFields['spl_product_data_elements'] = 'None'	## 113,811
drugFields['set_id'] = 'None'				## 114,337
drugFields['spl_unclassified_section'] = 'None'	##  48,037
drugFields['spl_unclassified_section_table'] = 'None' ## 2,805
drugFields['spl_patient_package_insert_table'] = 'None' ## 1,505
drugFields['spl_medguide_table'] = 'None'		## 3,952
drugFields['spl_patient_package_insert'] = 'None'	## 1,505
drugFields['spl_indexing_data_elements'] = 'None'	##    10
drugFields['package_label_principal_display_panel_table'] = 'None'	## 401
drugFields['package_label_principal_display_panel'] = 'None' 	##113,723

## INDICATIONS AND DESCRIPTION
drugFields['description_table'] = 'None'		##   2,362
drugFields['indications_and_usage'] = 'None'	## 108,563	
drugFields['indications_and_usage_table'] = 'None'	##    1,017
drugFields['description'] = 'None'			## 47,244
drugFields['purpose_table'] = 'None'			## 2,492
drugFields['purpose'] = 'None'			## 64,685
drugFields['instructions_for_use'] = 'None'		##  1,708

## DOSAGE AND ADMINISTRATION, STORAGE, HANDLING
drugFields['active_ingredient'] = 'None'		## 66,795
drugFields['active_ingredient_table'] = 'None'	##  2,838
drugFields['inactive_ingredient'] = 'None'
drugFields['when_using_table'] = 'None'
drugFields['dosage_forms_and_strengths'] = 'None'		## 14,656
drugFields['dosage_and_administration'] = 'None'		## 108,072
drugFields['dosage_and_administration_table'] = 'None'	##   21,336
drugFields['route'] = 'None'					## 50
drugFields['dosage_forms_and_strengths_table'] = 'None'	## 549
drugFields['storage_and_handling'] = 'None'			## 35,264
drugFields['how_supplied'] = 'None'				## 44,541
drugFields['how_supplied_table'] = 'None'			##  6,856
drugFields['storage_and_handling_table'] = 'None'		## 123
drugFields['safe_handling_warning_table'] = 'None'
drugFields['disposal_and_waste_handling'] = 'None'
drugFields['safe_handling_warning'] = 'None'

## CONTRAINDICATIONS, BOXED WARNING, PRECAUTIONS, RISKS, WARNINGS
## DRUG INTERACTIONS, ADVERSE REACTIONS, FOOD SAFETY, STOP USE
drugFields['contraindications'] = 'None'
drugFields['contraindications_table'] = 'None'
drugFields['summary_of_safety_and_effectiveness'] = 'None'
drugFields['general_precautions'] = 'None'
drugFields['boxed_warning'] = 'None'			## 16,218
drugFields['boxed_warning_table'] = 'None'
drugFields['precautions_table'] = 'None'
drugFields['general_precautions_table'] = 'None'
drugFields['precautions'] = 'None'
drugFields['risks'] = 'None'
drugFields['risks_table'] = 'None'
drugFields['warnings'] = 'None'
drugFields['warnings_and_cautions'] = 'None'
drugFields['warnings_and_cautions_table'] = 'None'
drugFields['warnings_table'] = 'None'
drugFields['drug_interactions'] = 'None'
drugFields['drug_interactions_table'] = 'None'
drugFields['adverse_reactions'] = 'None'			## 45,368
drugFields['adverse_reactions_table'] = 'None'		## 20,495
drugFields['food_safety_warning'] = 'None'			## 1
drugFields['stop_use'] = 'None'
drugFields['stop_use_table'] = 'None'
drugFields['risks'] = 'None'
drugFields['do_not_use'] = 'None'
drugFields['do_not_use_table'] = 'None'
drugFields['other_safety_information'] = 'None'
drugFields['user_safety_warnings'] = 'None'
drugFields['keep_out_of_reach_of_children'] = 'None'
drugFields['keep_out_of_reach_of_children_table'] = 'None'

## ABUSE, CONTROLLED SUBSTANCE
drugFields['abuse'] = 'None'
drugFields['abuse_table'] = 'None'
drugFields['dependence'] = 'None'
drugFields['dependence_table'] = 'None'
drugFields['drug_abuse_and_dependence'] = 'None'		## 9,633
drugFields['drug_abuse_and_dependence_table'] = 'None'		##     36
drugFields['controlled_substance'] = 'None'
drugFields['overdosage'] = 'None'
drugFields['overdosage_table'] = 'None'

## GENERAL INFORMATION
drugFields['ask_doctor_table'] = 'None'
drugFields['ask_doctor_or_pharmacist_table'] = 'None'
drugFields['ask_doctor_or_pharmacist'] = 'None'
drugFields['instructions_for_use_table'] = 'None'
drugFields['ask_doctor'] = 'None'
drugFields['questions'] = 'None'
drugFields['when_using'] = 'None'
drugFields['information_for_owners_or_caregivers'] = 'None'
drugFields['information_for_owners_or_caregivers_table'] = 'None'
drugFields['questions_table'] = 'None'
drugFields['troubleshooting'] = 'None'
drugFields['information_for_patients'] = 'None'
drugFields['information_for_patients_table'] = 'None'
drugFields['patient_medication_information'] = 'None'
drugFields['patient_medication_information_table'] = 'None'

## LIFE STAGE / SPECIAL POPULATIONS
drugFields['pregnancy_or_breast_feeding'] = 'None'		## 19,271
drugFields['pregnancy_or_breast_feeding_table'] = 'None'
drugFields['labor_and_delivery'] = 'None'
drugFields['nursing_mothers'] = 'None'
drugFields['pregnancy'] = 'None'
drugFields['pregnancy_table'] = 'None'
drugFields['pediatric_use'] = 'None'
drugFields['pediatric_use_table'] = 'None'
drugFields['geriatric_use'] = 'None'
drugFields['geriatric_use_table'] = 'None'
drugFields['use_in_specific_populations_table'] = 'None'
drugFields['use_in_specific_populations'] = 'None'

## PHARMACOLOGY
drugFields['pharmacokinetics'] = 'None'
drugFields['pharmacokinetics_table'] = 'None'
drugFields['pharmacodynamics_table'] = 'None'
drugFields['pharmacodynamics'] = 'None'
drugFields['pharmacogenomics'] = 'None'
drugFields['pharmacogenomics_table'] = 'None'
drugFields['mechanism_of_action_table'] = 'None'
drugFields['mechanism_of_action'] = 'None'
drugFields['clinical_pharmacology'] = 'None'
drugFields['clinical_pharmacology_table'] = 'None'
drugFields['clinical_studies'] = 'None'
drugFields['clinical_studies_table'] = 'None'
drugFields['animal_pharmacology_and_or_toxicology'] = 'None'
drugFields['animal_pharmacology_and_or_toxicology_table'] = 'None'
drugFields['nonclinical_toxicology_table'] = 'None'
drugFields['carcinogenesis_and_mutagenesis_and_impairment_of_fertility'] = 'None'

## LABS
drugFields['laboratory_tests'] = 'None'
drugFields['laboratory_tests_table'] = 'None'
drugFields['drug_and_or_laboratory_test_interactions_table'] = 'None'
drugFields['drug_and_or_laboratory_test_interactions'] = 'None'
drugFields['teratogenic_effects'] = 'None'
drugFields['teratogenic_effects_table'] = 'None'
drugFields['nonteratogenic_effects'] = 'None'
drugFields['nonteratogenic_effects_table'] = 'None'
drugFields['carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table'] = 'None'
drugFields['microbiology'] = 'None'
drugFields['microbiology_table'] = 'None'
drugFields['nonclinical_toxicology'] = 'None'

## MAJOR CHANGES, HEALTH CLAIMS, 
drugFields['recent_major_changes'] = 'None'
drugFields['recent_major_changes_table'] = 'None'
drugFields['effective_time'] = 'None'
drugFields['health_claim'] = 'None'
drugFields['health_claim_table'] = 'None'
drugFields['health_care_provider_letter'] = 'None'
drugFields['health_care_provider_letter_table'] = 'None'
drugFields['assembly_or_installation_instructions'] = 'None'
drugFields['other_safety_information_table'] = 'None'


## OTHER
drugFields['accessories'] = 'None'
drugFields['references'] = 'None'
drugFields['references_table'] = 'None'
drugFields['alarms'] = 'None'
drugFields['alarms_table'] = 'None'
drugFields['cleaning'] = 'None'
drugFields['environmental_warning'] = 'None'
drugFields['statement_of_identity_table'] = 'None'
drugFields['inactive_ingredient_table'] = 'None'
drugFields['intended_use_of_the_device'] = 'None'

drugFields['guaranteed_analysis_of_feed'] = 'None'
drugFields['components'] = 'None'
drugFields['statement_of_identity'] = 'None'
drugFields['veterinary_indications'] = 'None'
drugFields['calibration_instructions'] = 'None'
drugFields['residue_warning'] = 'None'

def read_product_data():
	with open('product.txt',encoding='ISO-8859-1') as csvDataFile:
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

def write_html_detail_monograph(generic_med_name, monograph, drugbank_mono):
	if len(monograph.generic_name) < 60:
		generic_name_init = re.sub(r'\s+','',monograph.generic_name)
		generic_name = re.sub(r'\/','',generic_name_init)

		drug_filename = './drugList/'+generic_name + '.html'
		drug_file = open(drug_filename,'w')
		drug_file.write('<html>\n<head>\n</head>\n<body>\n')
		drugName = '\n<h1>Generic med name: ' + generic_med_name + ' (' + monograph.brand_name + ')</h1>\n'
		drugIDinfo = '\n<p>SPL'+monograph.spl_id+'<BR>\nNDC:'+monograph.product_ndc+'<BR>\nRXCUI'+monograph.rxcui+'<BR>'
		drugPharmaClasses = '\n<p>Pharmaceutical Clases: ' + monograph.pharm_class + ', ' + monograph.pharm_class_pe

		drug_file.write(drugName)
		drug_file.write(drugIDinfo)
		drug_file.write(drugPharmaClasses)

		if monograph.boxedWarning != 'No warning':
			drug_file.write('\n<h1 id=\"warning\">BOXED WARNING</h1>\n<p>' + monograph.boxedWarning)


		drug_file.write ('<h2 id=\"drugName\">Generic cleaned name:' + generic_name + '<h2>\n')
		drug_file.write('\n<h3>How supplied</h3>\n' + monograph.how_supplied)
		drug_file.write('\n<h3>Indications and Usage</h3>\n' + monograph.indications_usage)
		drug_file.write('\n<h3>Description</h3>\n' + monograph.description)
		drug_file.write('\n<h3>Contraindications</h3>\n' + monograph.contraindications)
		drug_file.write('\n<h3>Precautions</h3>\n' + monograph.precautions)
		drug_file.write('\n<h3>Warnings</h3>\n' + monograph.warnings)
		drug_file.write('\n<h3>Route: ' + monograph.route + '</h3>')
		if len(monograph.dosage_admin) > 0:
			for dose in monograph.dosage_admin:
				drug_file.write(dose+'<BR>\n')

		drug_file.write('\n<h3>Adverse Reactions</h3>')
		drug_file.write('<p>'+monograph.adverse_reactions)

		if len(monograph.adverse_reactions) > 0:
			for adverse in monograph.adverse_reactions_table:
				drug_file.write(adverse +'<BR>\n')

		drug_file.write('\n<h3>Drug Interactions</h3>')
		drug_file.write('<p>' + monograph.drug_interactions + '</p>')
		for ddi in monograph.ddi_parsed:
			drug_file.write('<p>' + ddi)

		for ddi in monograph.ddi_parsed:
			drug_file.write('<p>' + ddi)

		if drugbank_mono != '':
			##drug_file.write('\n<h3><i>DB-Indications</i>' + drugbank_mono.indication + '\n')
			##drug_file.write('\n<h3><i>DB-Description</i>' + drugbank_mono.description + '\n')

			if len(drugbank_mono.adverse_reactions) > 0:
				drug_file.write('\n\n<h3<i>Adverse Reactions</i></h3>\n')
				for adverse_obj in drugbank_mono.adverse_reactions:
					drug_file.write('<P>' +adverse_obj.r_gene + '\n')
					drug_file.write('<p>' +adverse_obj.r_allele + '\n')
					drug_file.write('<P>' +adverse_obj.r_adverse + '\n')
					drug_file.write('<p> ' +adverse_obj.r_description + '\n')

			if len(drugbank_mono.food_interactions) > 0:
				drug_file.write('\n\n<h3 id=\"foodInteractions\"><i>Food Interactions</i></h3>\n')
				for food_interaction in drugbank_mono.food_interactions:
					drug_file.write('\n<p>' + food_interaction + ', ')
					drug_file.write('\n<h3>Dosage Admin</h3>')

		drug_file.close()
		##table_contents_file.write('<p><a href=\"./drugList/'+drug_filename+'\">Full monograph</a></p>\n')

def write_html(drug_monograph_dict):

	keys = drug_monograph_dict.keys()

	for key in keys:
		monograph = drug_monograph_dict[key][0]
		table_contents_file.write('<p>#######################################</p>\n')
		table_contents_file.write('<h2><a href = \"./drugList/' + monograph.generic_name +'\">' + monograph.generic_name + '</a></h2>')
		table_contents_file.write('<p>--------------------------------------------------</p>\n')
		table_contents_file.write('<p>Num meds: ' + str(len(drug_monograph_dict[key]))+ '\n')
		if key in drug_monograph_dict:
			drug_bank_monograph = drug_monograph_dict[key]
		table_contents_file.write('<h3>' + monograph.pharm_class + '</h3>\n')
		table_contents_file.write('<h3>' + monograph.pharm_class_pe + '</h3>\n')
		table_contents_file.write('<BR><BR>\n')

	table_contents_file.write('</body>\n</html>')

def create_monographs():

	adverse_out = open('adverse.txt','w')
	indications_out = open('indications.txt', 'w')
	warnings_out = open('warnings_precautions.txt','w')
	interactions_out = open('drug_interactions.txt','w')

	counter = 0;
	no_pharm_count = 0

	for drugSource in drugFiles:
		with open(drugSource) as json_file:
			data = json.load(json_file)
			for display_name in data['results']:
				drug_keys = display_name.keys()
				for dkey in drug_keys:
					if drugFields[dkey] == 'None':
						field_count = 1
						drugFields[dkey] = str(field_count)
					else:
						field_count = int(drugFields[dkey])
						field_count = field_count + 1
						drugFields[dkey] = str(field_count)

				drug_mono = DrugMonograph(display_name)

				if drug_mono.drugfields['adverse_reactions'] != None:
					adverse_out.write('-------------------NEW DRUG----------\n')
					adverse_out.write('Drug name: ' + drug_mono.generic_name+'\n')
					adverse_out.write('Brand name: ' + drug_mono.brand_name + '\n')
					if 'brand_name' in drug_mono.drugfields:
						adverse_out.write('Brand array: ' + str(drug_mono.drugfields['brand_name']))

					adverse_out.write('UNII: ' + drug_mono.unii+'\n')
					if 'unii' in drug_mono.drugfields:
						adverse_out.write('UNII array: ' + str(drug_mono.drugfields['unii']) + '\n')

					for adverse_text in drug_mono.drugfields['adverse_reactions']:
						adverse_out.write(adverse_text+ '\n')

				if drug_mono.drugfields['drug_interactions'] != None:
					interactions_out.write('-------------------NEW DRUG----------\n')
					interactions_out.write('Drug name: ' + drug_mono.generic_name+'\n')
					interactions_out.write('Brand name: ' + drug_mono.brand_name + '\n')
					if 'brand_name' in drug_mono.drugfields:
						interactions_out.write('Brand array: ' + str(drug_mono.drugfields['brand_name']))
					interactions_out.write('UNII: ' + drug_mono.unii+'\n')
					if 'unii' in drug_mono.drugfields:
						interactions_out.write('UNII array: ' + str(drug_mono.drugfields['unii']) + '\n')

					for interactions_text in drug_mono.drugfields['drug_interactions']:
						interactions_out.write(interactions_text + '\n')

				if drug_mono.drugfields['indications_and_usage'] != None:
					indications_out.write('-------------------NEW DRUG----------\n')
					indications_out.write('Drug name: ' + drug_mono.generic_name+'\n')
					indications_out.write('Brand name: ' + drug_mono.brand_name + '\n')
					if 'brand_name' in drug_mono.drugfields:
						indications_out.write('Brand array: ' + str(drug_mono.drugfields['brand_name']) + '\n')
					indications_out.write('UNII: ' + drug_mono.unii+'\n')
					if 'unii' in drug_mono.drugfields:
						indications_out.write('UNII array: ' + str(drug_mono.drugfields['unii']) + '\n')

					for indications_text in drug_mono.drugfields['indications_and_usage']:
						indications_out.write(indications_text + '\n')
				

				for prod_obj in product_data_array:
					if prod_obj.productNDC == drug_mono.product_ndc:
						##if  prod_obj.productPharmClasses != None:
						##	drug_mono.pharm_class = prod_obj.productPharmClasses
						if len(prod_obj.pharmEPC) > 0:
							drug_mono.pharm_class = prod_obj.pharmEPC[0]
						if len(prod_obj.pharmPE) > 0:
							drug_mono.pharm_class_pe = prod_obj.pharmPE[0]
						if prod_obj.methodOfAction != 'No method of action':
							drug_mono.method_of_action = prod_obj.methodOfAction

				unii_keys = drug_mono_dict.keys()

				if drug_mono.unii in unii_keys:
					drug_mono_array = drug_mono_dict[drug_mono.unii]
					drug_mono_array.append(drug_mono)
					drug_mono_dict[drug_mono.unii] = drug_mono_array
				else:
					drug_mono_array = []
					drug_mono_array.append(drug_mono)
					drug_mono_dict[drug_mono.unii] = drug_mono_array

				if drug_mono.pharm_class_pe == 'No Pharma PE' and drug_mono.pharm_class == 'No Pharma':
					no_pharm_count = no_pharm_count + 1
				else: 
					if drug_mono.pharm_class_pe in med_by_pharma:
						monographs_by_pharma_array = []
						monographs_by_pharma_array = med_by_pharma[drug_mono.pharm_class_pe]
						monographs_by_pharma_array.append(drug_mono)
						med_by_pharma[drug_mono.pharm_class_pe] = monographs_by_pharma_array
					else:
						monographs_by_pharma_array = []
						monographs_by_pharma_array.append(drug_mono)
						med_by_pharma[drug_mono.pharm_class_pe] = monographs_by_pharma_array

					if drug_mono.pharm_class in med_by_pharma:
						monographs_by_pharma_array = []
						monographs_by_pharma_array = med_by_pharma[drug_mono.pharm_class]
						monographs_by_pharma_array.append(drug_mono)
						med_by_pharma[drug_mono.pharm_class] = monographs_by_pharma_array
					else:
						monographs_by_pharma_array = []
						monographs_by_pharma_array.append(drug_mono)
						med_by_pharma[drug_mono.pharm_class] = monographs_by_pharma_array				

				counter = counter + 1

			print ('Number of monographs in dictionary: ' + str(len(drug_mono_dict)))
			print ('Total counter: '+ str(counter))
			print ('No pharma count: ' + str(no_pharm_count))

			pharma_keys = med_by_pharma.keys()

			for key in pharma_keys:
				
				pharma_array = med_by_pharma[key]
				num_meds = len(pharma_array)
				table_contents_file.write('<h2>' + key +', num Mono: ' + str(num_meds) + ' </h2>\n')
				table_contents_file.write('<p>----------------------\n')
				##if key != 'No Pharma PE':
				##	for med in pharma_array:
				##		table_contents_file.write('<p>' + med.generic_name + ' (' + med.unii + '), Method of Action: ' +med.method_of_action +'\n')


	keysCountFields = drugFields.keys()
	for key in keysCountFields:
		print (key + ': ' + drugFields[key])

	write_html(drug_mono_dict)	
	adverse_out.close()
	indications_out.close()
	warnings_out.close()
	interactions_out.close()

create_monographs()	
