import json
import csv
import re
from bs4 import BeautifulSoup
import lxml.html
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


drugFiles = ['drug-label-0001-of-0006.json']##,'drug-label-0002-of-0006.json','drug-label-0002-of-0006.json','drug-label-0004-of-0006.json','drug-label-0005-of-0006.json','drug-label-0006-of-0006.json',]
		
body_system = ['Gastrointestinal','Central Nervous System', 'Gastrointestinal System','Cardiovascular System','Psychiatric and Paradoxical Reactions','Urogenital System','Skin and Appendages']
product_data_array = []
prod_dic_by_company = {}
company_keys = prod_dic_by_company.keys()
ndc_keys = []
unique_keys = {}
med_by_pharma = {}
drug_mono_array = []
drug_mono_dict = {}

html_template_string = '<html>\n<title>FDA Monographs</title>\n<head>\n<body>\n<h1>FDA Monograph list</h1>'

class ProductSummary:
	def __init__(self,prod_items):
		self.product_items = prod_items
		self.isValid = 'NO'
		if(len(self.product_items) > 0):
			self.isValid = 'YES'
			self.productID = self.product_items[0]
			self.companyID = self.productID.split('_')[1]
			self.productNDC = self.product_items[1]
			self.productTypeName = self.product_items[2]
			self.productProprietary = self.product_items[3]
			self.productProprietarySuffix =  self.product_items[4]
			self.productNonProprietaryName = self.product_items[5]
			##added
			self.productDosageFormName = self.product_items[6]
			##added
			self.productRouteName =  self.product_items[7]
			##added
			self.productLabelerName= self.product_items[12]
			self.productStartMarketingDate = self.product_items[8]
			self.productEndMarketingDate = self.product_items[9]
			self.productMarketingCategoryName= self.product_items[10]
			self.productApplicationNumber = self.product_items[11]
			self.productSubstanceName = self.product_items[13]
			self.productActiveNumeratorStrength = self.product_items[14]
			self.productActiveIngredientUnit = self.product_items[15]
			self.productPharmClasses = self.product_items[16]

		##DEASCHEDULE
		
class DrugMonograph:
	def  __init__(self,drug_info):
		
		
		drug_keys= drug_info.keys()
		drug_fda = drug_info['openfda']
		self.id = drug_info['id']

		drug_monograph = drug_fda
		if len(drug_keys) < 5:
			print(str(drug_monograph))

		self.product_ndc = 'No PRODUCT NDC'
		self.rxcui = 'No RXCUI'
		self.spl_id = 'No SPL id'
		self.spl_set_id = 'No SPL set id'		
		self.product_id = 'No product_id'
		self.generic_name = 'No generic'
		self.brand_name = 'No brand name'
		self.pharm_class = 'No Pharma' 
		self.pharm_class_pe = 'No Pharma PE'
		self.product_type = 'No Product Type'
		self.manufacturer_name = 'No Mfr'
		self.brand_name = 'No Brand Name'
		self.route = 'No Route'
		self.precautions = 'No Precautions'
		self.how_supplied = 'No supplied'
		self.contraindications = 'No contraindications'
		self.description = 'No description'
		self.indications_usage  = 'No indications usage'
		self.patientInfo = 'No patient info'
		self.warnings = 'No warnings'
		self.mechanism  = 'No mechanism'
		self.pharmacology  = 'No pharmacology'
		self.boxedWarning = 'No warning'
		self.pharmacokinetics = 'No pharmacokinetics'
		self.pregnancy = 'No preggers'
		self.labor_delivery = 'No labor delivery'
		self.fertility = 'No fertility'
		self.adverse_reactions = 'No adverse'

		self.dosage_admin = []
		self.adverse_reactions_table = []
		self.drug_interactions = []
		self.pharmacokinetics_table = []
		self.manufacturers = []
		self.routes = []

		if 'product_ndc' in drug_fda:
			self.product_ndc = drug_fda['product_ndc'][0]
		if 'rxcui' in drug_fda:
			self.rxcui = drug_fda['rxcui'][0]
		if 'spl_id' in drug_fda:
			self.spl_id = drug_fda['spl_id'][0]
		if 'spl_set_id' in drug_fda:
			self.spl_set_id = drug_fda['spl_set_id'][0]


		if 'generic_name' in drug_fda or 'brand_name' in drug_fda:
			if 'generic_name' in drug_fda:
				generic_string = drug_monograph['generic_name'][0]
				self.generic_name = generic_string
			else: 
				self.generic_name = 'No Generic Name'

			if 'brand_name' in drug_fda:
				self.brand_name = drug_fda['brand_name'][0]

			if 'pharm_class_epc' in drug_fda:
				self.pharm_class = drug_fda['pharm_class_epc'][0]
			if 'pharm_class_pe' in drug_fda:
				self.pharm_class_pe = drug_fda['pharm_class_pe'][0]	
			if 'manufacturer_name' in drug_fda:
				self.manufacturer_name = drug_fda['manufacturer_name'][0]	
			if 'product_type' in drug_fda:
				self.product_type = drug_fda['product_type'][0]
			if 'indications_and_usage' in drug_keys:
				self.indications_usage = drug_info['indications_and_usage'][0]
			if 'contraindications' in drug_keys:
				self.contraindications = drug_info['contraindications'][0]
			if 'precautions' in drug_keys:
				self.precautions = drug_info['precautions'][0]
			if 'description' in drug_keys:
				self.description = drug_info['description'][0]
			if 'how_supplied' in drug_keys:
				self.how_supplied = drug_info['how_supplied'][0]


			if 'information_for_patients' in drug_keys:
				self.patientInfo = drug_info['information_for_patients'][0]
			if 'warnings' in drug_keys:
				self.warnings = drug_info['warnings'][0]
			if 'pregnancy' in drug_keys:
				self.pregnancy = drug_info['pregnancy'][0]
			if 'labor_and_delivery' in drug_keys:
				self.labor_delivery =   drug_info['labor_and_delivery'][0]
			if 'carcinogenesis_and_mutagenesis_and_impairment_of_fertility' in drug_keys:
				self.fertility =   drug_info['carcinogenesis_and_mutagenesis_and_impairment_of_fertility'][0]
			if 'boxed_warning' in drug_keys:
				self.boxedWarning = drug_info['boxed_warning'][0]	
			if 'route' in drug_fda:
				self.route = drug_fda['route'][0]

			if 'package_label_principal_display_panel' in drug_keys:
				self.package_label_display = drug_info['package_label_principal_display_panel'][0]
			if 'mechanism_of_action' in drug_keys:
				self.mechanism = drug_info['mechanism_of_action'][0]
			if 'clinical_pharmacology' in drug_keys:
				self.pharmacology = drug_info['clinical_pharmacology'][0]
			if 'pharmacokinetics' in drug_keys:
				self.pharmacokinetics = drug_info['pharmacokinetics'][0]

			if 'adverse_reactions' in drug_keys:
				self.adverse_reactions = drug_info['adverse_reactions'][0]

			## Arrays
			##-----------------------------------
			if 'dosage_and_administration_table' in drug_keys:
				self.dosage_admin = drug_info['dosage_and_administration_table']
			if 'adverse_reactions_table' in drug_keys:
				self.adverse_reactions_table = drug_info['adverse_reactions_table']
			if 'drug_interactions' in drug_keys:
				self.drug_interactions = drug_info['drug_interactions']
			if 'pharmacokinetic_table' in drug_keys:
				self.pharmacokinetics_table = drug_info['pharmacokinetics_table']

def checkMultipleArrayVal(drug_dic):
	dict_keys = drug_dic.keys()
	for key in dict_keys:
		if type(drug_dic[key]) is list:
			if len(drug_dic[key]) > 1:
				print('List contains multiple items')

def regexTableData(parse_text):
	for text_parse in parse_text:
		text_clean_1 = re.sub(r'<[A-Z,a-z,0-9\s]+\/>','####\n',text_parse)
		text_clean_2 = re.sub(r'<[A-Z,a-z,0-9\s]+ \= [A-Z,a-z,0-9\"]+>','####\n',text_clean_1)
		text_clean_3 = re.sub(r'<[A-Z,a-z,0-9\s\=]+>','####\n',text_clean_2)

		return text_clean_3

def write_med_mono(outfile, drug_mono, product):
	outfile.write('--------------------------------------------------------------\n')
	outfile.write('******' + drug_mono.boxedWarning+'\n')
	outfile.write('Drug ID: ' + drug_mono.id+ ', NDC: ' + drug_mono.product_ndc + '\n')
	outfile.write(drug_mono.generic_name + '(' + drug_mono.brand_name + ')' '\n' + 'Pharm class: ' + drug_mono.pharm_class + '\n')
	outfile.write(product.productLabelerName + '(' + drug_mono.manufacturer_name + ')\n')
	outfile.write(product.productDosageFormName + '\nActive: ' + product.productActiveNumeratorStrength + '(' + product.productActiveIngredientUnit + ')\n' + 'Route: ' + product.productRouteName + '\n')
	outfile.write(drug_mono.how_supplied + '\n')
	outfile.write(drug_mono.description + '\n')

	indications = drug_mono.indications_usage.split('.')
	for indication in indications:
		outfile.write(indication+'**')
	outfile.write(drug_mono.indications_usage + '\n')
	precautions = drug_mono.precautions.split(',')
	for precaution in precautions:
		outfile.write(precaution+'**')

	outfile.write(drug_mono.precautions+'\n')
	outfile.write(drug_mono.contraindications+'\n')
	outfile.write(drug_mono.warnings+'\n')
	outfile.write(drug_mono.patientInfo+'\n')
	outfile.write(drug_mono.pregnancy+'\n')
	outfile.write(drug_mono.labor_delivery+'\n')
	
	if len(drug_mono.adverse_reactions) == 0:
		outfile.write('ADVERSE: 0\n')
	else:
		for reaction in drug_mono.adverse_reactions:
			reaction_clean = re.sub(r'<[A-Z,a-z,0-9\s]+\/>','####\n',reaction)
			reaction_clean2 = re.sub(r'<[A-Z,a-z,0-9\s\"]+ \= [A-Z,a-z,0-9\"\/]*>','####\n',reaction_clean)
			reaction_clean3 = re.sub(r'<[A-Z,a-z,0-9\s\=]+>', '####\n', reaction)
			reaction_clean4 = re.sub(r'<\/[A-Z,a-z,0-9]>','****\n',reaction_clean3)
			reaction_clean5 = re.sub(r'<[A-Z,a-z,0-9\s]+[A-Z,a-z,0-9]+\=\"[A-Z,a-z,0-9]+\">','#*#*#*',reaction_clean4)
			outfile.write('ADVERSE:\n ' + soup.prettify())

			soup = BeautifulSoup(reaction,'xml')
			table_tags = soup.find('table')
			table_caption = table_tags.find('caption')
			if table_caption != None:
				print (table_caption[0])
			table_rows  = table_tags.find_all('tr')
			print('rows: ' + str(len(table_rows)))

			for tableRow in table_rows:
				tableItem = tableRow.find_all('td')
				for element in tableItem:
					if  len(element) > 0:
						item = element.contents[0]
						##print (item)

			table_items = table_row.find_all('td')
			print('table items: ' + str(len(table_items)))

	if len(drug_mono.dosage_admin) == 0:
		outfile.write('DOSE ADMIN: 0\n')
	else:
		for doseAdmin in drug_mono.dosage_admin:
			cleanDose = regexTableData(doseAdmin)
			##outfile.write('DOSE: \n' + cleanDose+'\n')

	if len(drug_mono.drug_interactions) == 0:
		outfile.write('INTERACTIONS : 0 \n')
	else:
		for interactions in drug_mono.drug_interactions:
			re.sub('<[a-z, A-Z, 0-9]+>', '!!\n!!', interactions)
			outfile.write('INTERACTIONS: \n' +interactions+'\n')
		
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

def write_html_detail_monograph(generic_med_name, monograph, toc_file):
	if len(monograph.generic_name) < 60:
			generic_name_init = re.sub(r'\s+','',monograph.generic_name)
			generic_name = re.sub(r'\/','',generic_name_init)
			drug_filename = generic_name + '.html'
			toc_file.write('<p><a href=\"./drugList/'+drug_filename+'\">Full monograph</a></p>\n')

			drug_file = open('./drugList/'+drug_filename,'w')
			if monograph.boxedWarning != 'No warning':
				drug_file.write('<h1 id=\"warning\">BOXED WARNING</h1>\n<p>' + monograph.boxedWarning)
			
			drugName = '<h2>' + generic_med_name + ' (' + monograph.brand_name + ')</h2>'
			drugIDinfo = '<p>SPL'+monograph.spl_id+'<BR>\nNDC:'+monograph.product_ndc+'<BR>\nRXCUI'+monograph.rxcui+'<BR>'
			drugPharma = '<h3>' + monograph.pharm_class + ' -- ' + monograph.pharm_class_pe +'</h3>\n'
			drug_file.write('<h3>Route: ' + monograph.route + '</h3>')
			drug_file.write(drugName)
			drug_file.write(drugIDinfo)
			drug_file.write(drugPharma)
			drug_file.write('<h3>How supplied</h3>\n' + monograph.how_supplied)
			drug_file.write('<h3>Indications and Usage</h3>\n' + monograph.indications_usage)
			drug_file.write('<h3>Description</h3>\n' + monograph.description)
			drug_file.write('<h3>Contraindications</h3>\n' + monograph.contraindications)
			drug_file.write('<h3>Precautions</h3>\n' + monograph.precautions)
			drug_file.write('<h3>Warnings</h3>\n' + monograph.warnings)

			drug_file.write('<h3>Dosage Admin</h3>')
			if len(monograph.dosage_admin) > 0:
				for dose in monograph.dosage_admin:
					drug_file.write(dose+'<BR>\n')

			drug_file.write('<h3>Adverse Reactions</h3>')
			drug_file.write(monograph.adverse_reactions)
			if len(monograph.adverse_reactions) > 0:


				gastrointestinal_re = re.compile(r'Gastrointestinal (:)*', re.UNICODE)

				for adverse in monograph.adverse_reactions_table:
					match = re.search('Gastrointestinal (:)*',adverse)
					if match != None:
						print  (generic_name + ' ' + str(match) + "-->" + adverse)
					gastrointestinal_re.sub(r'<P>Gastrointestinal: <BR>',adverse)
					re.sub(r'Central Nervous System:','<P>Central Nervous System: <BR>',adverse)
					re.sub(r'Cardiovascular:','<P>Cardiovascular: <BR>',adverse)
					re.sub(r'Skin:','<P>Skin: <BR>',adverse)
					subpoints = re.split(r'(\d+\.\d+)',adverse)
					if subpoints != None:
						drug_file.write('<P>\n<ol>\n')
						for point in subpoints:
							drug_file.write('<li>' + point + '</li>')
						drug_file.write('</ol></p')
					else:
						re.sub(r'Gastrointestinal:','<P>Gastrointestinal: <BR>',adverse)
						re.sub(r'Central Nervous System:','<P>Central Nervous System: <BR>',adverse)
						re.sub(r'Cardiovascular:','<P>Cardiovascular: <BR>',adverse)
						re.sub(r'Skin:','<P>Skin: <BR>',adverse)
						drug_file.write(adverse +'<BR>\n')

			drug_file.write('<h3>Drug Interactions</h3>')
			if len(monograph.drug_interactions) > 0:
				for interaction in monograph.drug_interactions:
					subpoints = re.split(r'(\d+\.\d+\s)',interaction)
					if subpoints != None:
						drug_file.write('<P>\n<ul>\n')
						for point in subpoints:
							drug_file.write('<li>' + point + '</li>')
					else:
						drug_file.write(interaction+'<BR>\n')
			drug_file.close()
					
def write_html(drug_monograph_dict):

	keys = drug_monograph_dict.keys()
	table_contents_file = open('monographs-toc.html','w')
	table_contents_file.write(html_template_string)


	for key in keys:
		drug_array = drug_monograph_dict[key]
		table_contents_file.write('<h2>' + key + '</h2>\n')
		table_contents_file.write('<p>-------------------------------------------------</p>\n')
		monograph = drug_monograph_dict[key][0]
		table_contents_file.write('<h3>' + monograph.pharm_class + '</h3>\n')
		write_html_detail_monograph(key, monograph, table_contents_file)

		if monograph.pharm_class_pe in med_by_pharma:
			monographs_by_pharma_array = med_by_pharma[monograph.pharm_class]
			monographs_by_pharma_array.append(monograph)
		else:
			monographs_by_pharma_array = []
			monographs_by_pharma_array.append(monograph)
			med_by_pharma[monograph.pharm_class] = monographs_by_pharma_array

	table_contents_file.write('</body>\n</html>')
	table_contents_file.close()

def write_html_by_pharma_class(medication_by_pharmaceutical_class_dict):
	pharmaMedOutfile = open('MonographsByPharma.html','w')
	pharmaMedOutfile.write(html_template_string)

	med_by_pharma_keys = medication_by_pharmaceutical_class_dict.keys()

	for pharma_key in med_by_pharma_keys:
		med_array = med_by_pharma[pharma_key]
		pharmaMedOutfile.write('<h2>'+ pharma_key + '</h2>\n')
		for med in med_array:
			pharmaMedOutfile.write('<h3>' + med.generic_name + '  (' + med.brand_name + ') </h3>\n')

	pharmaMedOutfile.write('</body>\n</html>')
	pharmaMedOutfile.close()

def create_monographs():
	outfile= open('monographs.txt','w')
	outfile2 = open('monographs2.txt','w')
	outfile3 = open('monographs3.txt','w')
	outfile4 = open('monographs4.txt','w')
	outfile5 = open('monographs5.txt','w')
	outfile6 = open('monographs6.txt','w')

	for drugSource in drugFiles:
		with open(drugSource) as json_file:
			print ('OPEN FILE')
			data = json.load(json_file)
			counter = 0;
			
			for display_name in data['results']:
				drug_mono = DrugMonograph(display_name)
				generic = drug_mono.generic_name
				counter = counter + 1
				if counter > 3000 and counter < 6000:
					outfile = outfile2
				elif counter > 5999 and counter < 9000:
					outfile = outfile3
				elif counter > 8999 and counter < 12000:
					outfile = outfile4
				elif counter > 11999 and counter < 15000:
					outfile = outfile5
				elif counter > 15000:
					outfile = outfile6
				
				if drug_mono.product_type == 'HUMAN PRESCRIPTION DRUG':

					drug_keys = display_name.keys()
					for drug_key in drug_keys:
						if drug_key in unique_keys:
							drug_key_count = int(unique_keys[drug_key])
							drug_key_count = drug_key_count + 1
							unique_keys[drug_key] = str(drug_key_count)
						else:
							unique_keys[drug_key] = 1


					if generic in drug_mono_dict:
						drug_array = drug_mono_dict[generic]
						drug_array.append(drug_mono)
						for product in product_data_array:
							if product.companyID == drug_mono_id:
								drug_mono.productID= product.productID
					else:
						counter = counter + 1
						drug_array = []
						drug_array.append(drug_mono)
						drug_mono_dict[generic] = drug_array
						if drug_mono.pharm_class  =='No Pharma'  and drug_mono.pharm_class_pe == 'No Pharma PE':
							drug_mono_id = drug_mono.id
							for product in product_data_array:
								if product.companyID == drug_mono_id:
									drug_mono.productID= product.productID
									drug_mono.pharm_class = product.productPharmClasses
									##write_med_mono(outfile,drug_mono, product)
									drug_mono_array.append(drug_mono)
									break
					
			


			write_html(drug_mono_dict)
			
	outfile.close()
	outfile2.close()
	outfile3.close()
	outfile4.close()
	outfile5.close()
	outfile6.close()

	##write_html_by_pharma_class(med_by_pharma)

read_product_data()
create_monographs()	



	##for product in product_data_array:
	##	ndc = product.productNDC
	##	ndc_list = ndc.split('-')
	##	ndc_company = ndc_list[0]
	##	if ndc_company in prod_dic_by_company:
	##		company_drug_array = prod_dic_by_company[ndc_company]
	##		company_drug_array.append(product)
	##	else:
	##		new_array = []
	##		new_array.append(product)
	##		prod_dic_by_company[ndc_company] = new_array
	
	##for key in company_keys:
	##	print(key)
	##	productInfoList = prod_dic_by_company[key]
		##for product in productInfoList:
		##	print (product.productProprietary + ', ' + product.productLabelerName + ', '+ product.productDosageFormName + ', ' + product.productRouteName)
		
##spl_unclassified_section
##spl_product_data_elements
##set_id
##overdosage
##laboratory_tests
##effective_time
##clinical_studies
##geriatric_use
##nursing_mothers
##do_not_use
##active_ingredient
##inactive_ingredient
##keep_out_of_reach_of_children


##id: 						33004		added
##set_id: 					33004
##version: 					33004
##effective_time: 				33004
##openfda: 					33004
##spl_product_data_elements: 		33004

##package_label_principal_display_panel: 	32971		added
##adverse_reactions: 			30060		added
##description: 				30376		added
##dosage_and_administration: 		30772		added
##indications_and_usage: 			30878		added
##information_for_patients: 			21655		added
##clinical_pharmacology: 			29625
##contraindications: 				29997		added
##how_supplied: 				29644

##overdosage: 				27385
##pregnancy: 				23114
##pediatric_use: 				23293
##drug_interactions: 				22222
##nursing_mothers: 				21985
##carcinogenesis_and_mutagenesis_and_impairment_of_fertility: 21224
##geriatric_use: 				19256
##precautions: 				19614
##warnings:					18855
##spl_unclassified_section: 			16868
##pharmacokinetics: 				15952
##adverse_reactions_table: 			14267
##mechanism_of_action: 			12164
##general_precautions: 			11385
##boxed_warning: 				11231
##use_in_specific_populations: 		10744
##nonclinical_toxicology: 			10128
##dosage_forms_and_strengths: 		10256
##clinical_pharmacology_table: 		10056
##warnings_and_cautions: 			10801
##clinical_studies_table: 			8497
##pharmacodynamics: 			9317
##storage_and_handling: 			8699
##dosage_and_administration_table: 	8620
##teratogenic_effects: 			8084
##laboratory_tests: 				6942
##drug_abuse_and_dependence: 		6601
##labor_and_delivery: 			6645
##spl_medguide: 				6598
##recent_major_changes: 			5524
##references: 				5677
##how_supplied_table:			5206
##pharmacokinetics_table: 			5355
##spl_patient_package_insert: 		3919
##drug_and_or_laboratory_test_interactions: 3823
##animal_pharmacology_and_or_toxicology: 3969
##nonteratogenic_effects: 			3208
##abuse: 					2335
##spl_medguide_table: 			2852
##controlled_substance: 			2581
##warnings_and_cautions_table: 		2190
##drug_interactions_table: 			2147
##dependence: 				2174
##warnings_table: 				2098
##microbiology: 				2051
##spl_unclassified_section_table: 		1562
##recent_major_changes_table: 		1468
##description_table: 				1496
##inactive_ingredient: 			1149
##spl_patient_package_insert_table: 	1107
##microbiology_table: 			887
##pharmacodynamics_table: 		858
##precautions_table: 				797
##indications_and_usage_table:		725
##instructions_for_use: 			609
##use_in_specific_populations_table: 	600
##active_ingredient: 551
##	keep_out_of_reach_of_children: 	503
##	information_for_patients_table: 	455
##	pediatric_use_table: 			413
##	dosage_forms_and_strengths_table: 380
##	patient_medication_information: 	366
##	questions: 				363
##	purpose: 				314
##	pregnancy_or_breast_feeding: 	258
##	instructions_for_use_table: 		234
##	general_precautions_table: 		172
##	geriatric_use_table: 			161
##	other_safety_information: 		123
##	stop_use: 				123
##	do_not_use: 				120
##	nonclinical_toxicology_table: 	117
##	risks: 					102

##	package_label_principal_display_panel_table: 96
##	contraindications_table: 95
##	carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table: 85
##	when_using: 82
##	ask_doctor: 71
##	overdosage_table: 70
##	storage_and_handling_table: 64
##	patient_medication_information_table: 63
##	pharmacogenomics: 57
##	safe_handling_warning: 47
##	boxed_warning_table: 41
##	mechanism_of_action_table: 35
##	laboratory_tests_table: 27
##	components: 25
##	references_table: 23
##	disposal_and_waste_handling: 19
##	information_for_owners_or_caregivers: 19
##	drug_abuse_and_dependence_table: 18
##	health_care_provider_letter: 17
##	active_ingredient_table: 17
##	pregnancy_table: 16
##	ask_doctor_or_pharmacist: 15
##	troubleshooting: 14
##	purpose_table: 12
##	user_safety_warnings: 12
##	health_care_provider_letter_table: 12
##	drug_and_or_laboratory_test_interactions_table: 12
##	nonteratogenic_effects_table: 10
##	abuse_table: 8
##	veterinary_indications: 8
##	inactive_ingredient_table: 8
##	animal_pharmacology_and_or_toxicology_table: 7
##	statement_of_identity: 6
##	spl_indexing_data_elements: 3
##	information_for_owners_or_caregivers_table: 3
##	cleaning: 2
##	when_using_table: 2
##	intended_use_of_the_device: 2
##	teratogenic_effects_table: 1
##	statement_of_identity_table: 1
##	safe_handling_warning_table: 1
##	health_claim: 1
##	risks_table: 1
##	summary_of_safety_and_effectiveness: 1
##	other_safety_information_table: 1
##	calibration_instructions: 1
##	dependence_table: 1
##	environmental_warning: 1







				
	
