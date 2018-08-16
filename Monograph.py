import json
import csv
import re
from bs4 import BeautifulSoup
import lxml.html
from nltk import ngrams
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom
from nltk import sent_tokenize
from nltk import ngrams


ddi_re = re.compile(r'(\s[\([0-9]+\.[0-9\)]+\s)')
adv_re_spilt = re.compile(r'\n')
cyp_re_t = re.compile(r'(^CYP\s?[A-Za-z0-9\s]{1,5}) (\w+)')
cyp_re_t2 = re.compile(r'(^cyp\s?[A-Za-z0-9\s]{1,5}) (\w+)')
cyp_re_t3 = re.compile(r'(^Cytochrome\s?[A-Za-z0-9\s]{1,5}) (\w+)')

cyp_increase_effect = re.compile(r'\s?CYP([A-Za-z0-9]+) inhibitors (\w+)')
cyp_decrease_effect = re.compile(r'decrease\s?([A-Za-z0-9\s]+) (\w+)')
cyp_1 = re.compile(r'([Inhibitors|Inducers]) of (CYP[A-Z0-9a-z]+), (CYP[A-Z0-9a-z]+), and (CYP[A-Z0-9a-z]+)(.+) ([increase | decrease])(.+)(concentration)')
cyp_2 = re.compile(r'[concomitant administration] with <INHIBITORS>|<INDUCERS> of (<CYP[A-Za-z0-9]+) (.+) <METABOLISM>')

cyp_1a = '(<INHIBITORS> | <INDUCERS>) of (<CYP[A-Z0-9a-z]+>, <CYP[A-Za-z0-9]+>, and <CYP[A-Za-z0-9]+>) (such as...+) have the potential to ([INCREASE | DECREASE]) <DRUG> <concentration'
cyp_4 = '[coadministration] with <INHIBITORS>|<INDUCERS> of <CYP[A-Za-z0-9]+) (.+) <METABOLISM>'
cyp_5 = '[Administration] of (<CYP[A-Za-z0-9]+) with <INHIBITORS>|<INDUCERS> of <CYP[A-Za-z0-9]+) (.+) (<METABOLISM>)'
cyp_6 = '[administration] of (<CYP[A-Za-z0-9]+) with <INHIBITORS>|<INDUCERS> of <CYP[A-Za-z0-9]+) (.+) (<METABOLISM>)'
cyp_7 = '(Drugs that) (<INHIBIT | INDUCE>) (<CYP[A-Za-z0-9]+) such as (.+) (<INCREASE | DECREASE>)'
cyp_8 = '[Administration] of (<CYP[A-Za-z0-9]+)  (<INHIBITORS>|<INDUCERS>) such as (.+) may effect (<METABOLISM>)'
cyp_9 = '[Administration] of (<CYP[A-Za-z0-9]+) with <INHIBITORS>|<INDUCERS> of <CYP[A-Za-z0-9]+) (.+) <METABOLISM>'
cyp_10 = '[Administration] of (<CYP[A-Za-z0-9]+) with <INHIBITORS>|<INDUCERS> of <CYP[A-Za-z0-9]+) (.+) <METABOLISM>'

cyp_regex_array = []
cyp_regex_array.append(cyp_increase_effect)
cyp_regex_array.append(cyp_decrease_effect)
cyp_regex_array.append(cyp_1)
cyp_regex_array.append(cyp_2)


p_glyco = 'P-Glycoprotein (PGP)'
adverse_1 = re.compile(r'(.+)(The following serious adverse reactions are):([A-Za-z\,\;\s\-\'\-]+)')
adverse_1a = re.compile(r'(.+)(The following adverse reactions are):([A-Za-z\,\;\s\-\'\-]+)')
adverse_2 = re.compile(r'(.+)(Most common adverse reactions are:)([A-Za-z\,\;\s\-\'\-]+)')
adverse_2a = re.compile(r'(.+)(Most common adverse reactions \(incidence [\≥\>\<0-9\%]+\)\s?)([A-Za-z\,\;\s\-\'\-]+)')
adverse_3 = re.compile(r'(.+)(Side effects most commonly reported were)([A-Za-z\,\;\s\-\'\-]+)')
adverse_4 = re.compile(r'(.+)(in more detail in other sections of the labeling:)([A-Za-z\,\;\s\-\'\-]+)')
adverse_5 = re.compile(r'(.+)(The following adverse reactions have been reported:)(.+)')
adverse_6 = re.compile(r'(.+)(The most frequent and common adverse reactions)(.+)are\s?(.+)')
adverse_7 = re.compile(r'(.+)(The most frequently reported adverse reactions are)\s?(.+)')
adverse_8 = re.compile(r'(.+)The most frequently occurring adverse reactions occurring in at least [0-9\%\.]+ of patients(.+)are(.+)')
adverse_9 = re.compile(r'(.+)(The following serious adverse reactions are described elsewhere in the labeling:)(.+)')
adverse_10 = re.compile(r'(.+)The most frequently reported adverse reactions for(.+)occurring in approximately ([0-9\%\.]+) to ([0-9\%\.]+)  of the overall study population were(.+)')

ddi_re_1 = re.compile(r'(.+)The concomitant use of(.+)and(.+)increases the risk of(.+)because(.+)')

regex_array = []
regex_array.append(adverse_1)
regex_array.append(adverse_1a)
regex_array.append(adverse_2)
regex_array.append(adverse_2a)
regex_array.append(adverse_3)
regex_array.append(adverse_4)
regex_array.append(adverse_5)
regex_array.append(adverse_6)
regex_array.append(adverse_7)
regex_array.append(adverse_8)
regex_array.append(adverse_9)
regex_array.append(adverse_10)

regex_results = None

indication_type_treatment= re.compile(r'(.+)treatment of(.+)')
indication_type_relief= re.compile(r'(.+)relief of symptoms of(.+)')
indication_type_management= re.compile(r'(.+)management of(.+)')
indication_type_adjunctive = re.compile(r'(.+)adjunctive therapy(.+)')
indication_type_combo = re.compile(r'(.+)in combination with(.+)')

sub_sec_split = re.compile(r'[A-Za-z]([0-9]+\.[0-9]+)\s+')
interactions_sec_num = re.compile('^([0-9]+) DRUG INTERACTIONS')




class ProductSummary:
	def __init__(self,prod_items):
		self.product_items = prod_items
		self.isValid = 'NO'
		if(len(self.product_items) > 0):


			self.numFields = str(len(self.product_items))
			self.isValid = 'YES'
			self.productID = self.product_items[0]
			self.companyID = self.productID.split('_')[1]
			self.productNDC = self.product_items[1]
			self.productTypeName = self.product_items[2]
			self.productProprietary = 'No proprietary'
			self.productProprietary = self.product_items[3]
			self.productProprietarySuffix =  self.product_items[4]
			self.productNonProprietaryName = self.product_items[5]
			self.productDosageFormName = self.product_items[6]
			self.productRouteName =  self.product_items[7]
			self.productLabelerName= self.product_items[12]
			self.productStartMarketingDate = self.product_items[8]
			self.productEndMarketingDate = self.product_items[9]
			self.productMarketingCategoryName= self.product_items[10]
			self.productApplicationNumber = self.product_items[11]
			self.productSubstanceName = self.product_items[13]
			self.productActiveNumeratorStrength = self.product_items[14]
			self.productActiveIngredientUnit = self.product_items[15]
			self.productPharmClasses = self.product_items[16]

			if self.productEndMarketingDate == None:
				print (self.productNonProprietaryName + ':  [Begin Mktg]: ' + self.productStartMarketingDate + ',  [End Mktg]: ' + self.productEndMarketingDate) 

			self.pharmEPC = []
			self.pharmPE = []
			self.methodOfAction = 'No method of action'
			match_epc = re.compile(r'([A-Za-z0-9\-\,\s]+) (\[EPC\])')
			match_pe = re.compile(r'([A-Za-z0-9\-\,\s]+) (\[PE\])')
			match_moa = re.compile(r'([A-Za-z0-9\-\s\,]+) (\[MOA\])')

			if self.productPharmClasses != None:
				pharm_elem = self.productPharmClasses.split(',')

				if len(pharm_elem)== 2:
					if match_epc.match(pharm_elem[0]):
						self.pharmEPC.append(pharm_elem[0])
					elif match_epc.match(pharm_elem[0]):
						self.pharmPE.append(pharm_elem[0])
					elif match_moa.match(pharm_elem[0]):
						self.methodOfAction = pharm_elem[0]

					self.methodOfAction = pharm_elem[1]

				elif len(pharm_elem) == 1:

					if match_epc.match(pharm_elem[0]):
						self.pharmEPC.append(pharm_elem[0])
					elif match_epc.match(pharm_elem[0]):
						self.pharmPE.append(pharm_elem[0])
					elif match_moa.match(pharm_elem[0]):
						self.methodOfAction = pharm_elem[0]

				elif len(pharm_elem) > 2:

					epc = ''
					pe = ''
					moa = ''

					for pharm in pharm_elem:

						result = match_epc.match(pharm)

						if result != None:
							match_groups = result.groups()
							epc = result.group(1)
							self.pharmEPC.append(epc)

						result2 = match_pe.match(pharm)

						if result2 != None:
							match_groups = result2.groups()
							pe = result2.group(1)
							self.pharmPE.append(pe)

						result3 = match_moa.match(pharm)
						if result3 != None:
							match_groups = result3.groups()
							moa = result3.group(1)
							self.methodOfAction = moa
	
class DrugMonograph:
	def  __init__(self,drug_info,corpus,corpus_indications, more_corpus):

		drug_keys= drug_info.keys()
		drug_fda = drug_info['openfda']
		keys_drug_fda = drug_fda.keys()
		self.all_keys_ = drug_fda.keys()
		self.num_fda_keys = len(drug_fda.keys())
		self.num_drug_keys = self.num_fda_keys + len(drug_keys)

		drug_monograph = drug_fda
		self.multi_ontology = corpus
		self.ontology_indications = corpus_indications
		self.more_ontology = more_corpus

		more_corp_keys = more_corpus.keys()
		for more_key in more_corpus:
			self.multi_ontology[more_key] = more_corpus[more_key]

		self.fertility = []
		self.drugfields = {}

		self.adverse_parse_terms  = {}

		self.cyp_text_raw = []
		self.ddi_parsed = []
		self.cyp_dict = {}
	
		self.regex_adverse_analysis = []
		self.regex_adverse_match_terms = []
		self.regex_adverse_match_table_terms = []
		self.adverse_reactions = []

		for drug_key in drug_keys:
			if drug_key in self.drugfields:
				self.drugfields[drug_key] = drug_info[drug_key]

		for drug_detail_key in self.all_keys_:
			if drug_detail_key in self.drugfields:
				self.drugfields[drug_detail_key] = drug_fda[drug_detail_key]

		if 'set_id' in drug_info:
			self.set_id = drug_info['set_id']
		else:
			self.set_id = 'No Set'
		if 'effective_time' in drug_info:
			self.effective_time = drug_info['effective_time']
		else:
			self.effective_time = 'No effective time'
		if 'version' in drug_info:
			self.version = drug_info['version']
		else:
			self.version = 'No version'
		if 'application_number' in drug_info:
			self.application_number = drug_info['application_number']
		else:
			self.application_number = 'No application number'

		self.product_type = ''
		if 'product_type' in drug_fda:
			self.product_type = drug_fda['product_type'][0]

		self.monograph_id = drug_info['id']
		print ('ID: ' + self.monograph_id)
		self.product_id ='No product id'
		if 'product_id' in  drug_info:
			self.product_id = drug_info['product_id']
			print ('Product ID: '  + self.product_id)
		self.rxcui = []
		if 'rxcui' in drug_fda:
			self.rxcui = drug_fda['rxcui']
		self.spl_id = []
		if 'spl_id' in drug_fda:
			self.spl_id = drug_fda['spl_id']
		self.spl_set_id = []
		if 'spl_set_id' in drug_fda:
			self.spl_set_id = drug_fda['spl_set_id']
		self.nui =[]
		if 'nui' in drug_info:
			self.nui = drug_fda['nui']
		self.product_ndc = []	
		if 'product_ndc' in drug_fda:
			self.product_ndc = drug_fda['product_ndc']	
		self.product_data_elements = []
		if 'product_data_elements' in drug_fda:
			self.self.product_data_elements = drug_fda['product_data_elements']

		self.spl_unclassified_section = []
		if 'spl_unclassified_section' in drug_fda:
			self.spl_unclassified_section = drug_info['spl_unclassified_section']
		self.spl_medguide = []
		if 'spl_medguide' in drug_fda:
			self.spl_medguide = drug_info['spl_medguide']
		self.spl_unclassified_section_table = []
		if 'spl_unclassified_section_table' in drug_fda:
			self.spl_unclassified_section_table = drug_info['spl_unclassified_section_table']
		self.spl_patient_package_insert_table = [] 
		if 'spl_patient_package_insert_table' in drug_fda:
			self.spl_patient_package_insert_table = drug_info['spl_patient_package_insert_table']
		self.spl_package_insert = []
		if 'spl_patient_package_insert' in drug_fda:
			self.spl_patient_package_insert = drug_info['spl_patient_package_insert']
		self.spl_indexing_data_elements = []
		if 'spl_indexing_data_elements' in drug_fda:
			self.spl_indexing_data_elements = drug_info['spl_indexing_data_elements']


		self.generic_name = 'No generic'		
		if 'generic_name' in drug_fda or 'brand_name' in drug_fda:
			if 'generic_name' in drug_fda:
				generic_string = drug_monograph['generic_name'][0]
				self.generic_name = generic_string
			else: 
				self.generic_name = 'No Generic Name'

			self.brand_name = []
			if 'brand_name' in drug_fda:
				self.brand_name = drug_fda['brand_name']   ############
			self.manufacturer_name = []
			if 'manufacturer_name' in drug_fda:
				self.manufacturer_name = drug_fda['manufacturer_name']
			self.pharm_class_epc = []		
			if 'pharm_class_epc' in drug_fda:
				self.pharm_class_epc = drug_fda['pharm_class_epc']    ############
			self.pharm_class_pe = []
			if 'pharm_class_pe' in drug_fda:
				self.pharm_class_pe = drug_fda['pharm_class_pe']   ############
			self.pharm_class_moa = []
			if 'pharm_class_moa' in drug_fda:
				self.pharm_class_moa = drug_fda['pharm_class_moa']   ###########
			self.pharm_class_cs= []
			if 'pharm_class_ce' in drug_fda:
				self.pharm_class_ce = drug_fda['pharm_class_ce']   ############
			self.package_label_display = []		
			if 'package_label_principal_display_panel' in drug_keys:
				self.package_label_display = drug_info['package_label_principal_display_panel'] ############
			self.package_label_principal_display_panel_table = []
			if 'package_label_principal_display_panel_table' in drug_keys:
				self.package_label_principal_display_panel_table  = drug_info['package_label_principal_display_panel_table']   ############
			self.indications_usage  = []
			if 'indications_and_usage' in drug_keys:
				self.indications_usage = drug_info['indications_and_usage']   ############
			self.indications_usage_table  = []
			if 'indications_and_usage_table' in drug_keys:
				self.indications_usage_table = drug_info['indications_and_usage_table']    ############
			self.description =[]
			if 'description' in drug_keys:
				self.description = drug_info['description']    ############
			self.purpose = []
			if 'purpose' in drug_keys:
				self.purpose = drug_info['purpose']       ############
			self.purpose_table =[]
			if 'purpose_table' in drug_fda:
				self.purpose_table = drug_info['purpose_table']  ############
			self.information_for_patients =[]
			if 'information_for_patients' in drug_keys:
				self.information_for_patients = drug_info['information_for_patients']   ############
			self.instructions_for_use =[]
			if 'instructions_for_use' in drug_fda:
				self.instructions_for_use = drug_info['instructions_for_use']   ###########

			self.route = []
			if 'route' in drug_fda:
				self.route = drug_fda['route']    ############
			self.dosage_admin = []
			if 'dosage_and_administration' in drug_fda:
				self.dosage_admin = drug_fda['dosage_and_administration']   ############
			self.dosage_and_administration_table = []
			if 'dosage_and_administration_table' in drug_keys:
				self.dosage_and_administration_table = drug_info['dosage_and_administration_table']   ############
			self.contraindications = []
			if 'contraindications' in drug_keys:
				self.contraindications = drug_info['contraindications']  ############
			self.contraindications_table = []
			if 'contraindications_table' in drug_keys:
				self.contraindications = drug_info['contraindications_table']  ###########
			self.warnings = []
			if 'warnings' in drug_keys:
				self.warnings = drug_info['warnings']  ############
			self.warnings_and_cautions =[]
			if 'warnings_and_cautions' in drug_keys:
				self.warnings_and_cautions = drug_info['warnings_and_cautions'] 
			self.warnings_and_cautions_table =[]
			if 'warnings_and_cautions_table' in drug_keys:
				self.warnings_and_cautions_table = drug_info['warnings_and_cautions_table'] 
			self.precautions = []
			if 'precautions' in drug_keys:
				self.precautions = drug_info['precautions']  ############
			self.precautions_table =[]
			if 'precautions_table' in drug_keys:
				self.precautions_table = drug_info['precautions_table']  ############
			self.general_precautions =[]
			if 'general_precautions' in drug_keys:
				self.general_precautions = drug_info['general_precautions']  ############
			self.general_precautions_table =[]
			if 'general_precautions_table' in drug_keys:
				self.general_precautions_table = drug_info['general_precautions_table']  ############
			self.warnings_table =[]
			if 'warnings_table' in drug_keys:
				self.warnings_table = drug_info['warnings_table'] 
			self.risks =[]
			if 'risks' in drug_keys:
				self.risks = drug_info['risks'] 
			self.risks_table =[]
			if 'risks_table' in drug_keys:
				self.risks_table = drug_info['risks_table'] 
			self.summary_of_safety_and_effectiveness =[]
			if 'summary_of_safety_and_effectiveness' in drug_keys:
				self.summary_of_safety_and_effectiveness = drug_info['summary_of_safety_and_effectiveness'] 
			##self.adverse_reactions = []
			if 'adverse_reactions' in drug_keys:
				self.adverse_reactions = drug_info['adverse_reactions']  ############
			self.adverse_reactions_table = []
			if 'adverse_reactions_table' in drug_keys:
				self.adverse_reactions_table = drug_info['adverse_reactions_table']  ############
			self.drug_interactions = []
			if 'drug_interactions' in drug_keys:
				self.drug_interactions = drug_info['drug_interactions']   ############
			self.drug_interactions_table =[]
			if 'drug_interactions_table' in drug_keys:
				self.drug_interactions_table = drug_info['drug_interactions_table']   ############
			self.boxed_warning =[]
			if 'boxed_warning' in drug_keys:
				self.boxed_warning = drug_info['boxed_warning'] ###########
			self.pharmacokinetics = []
			if 'pharmacokinetics' in drug_keys:
				self.pharmacokinetics = drug_info['pharmacokinetics']  #######
			self.pharmacokinetic_table =[]
			if 'pharmacokinetic_table' in drug_keys:
				self.pharmacokinetics_table = drug_info['pharmacokinetics_table']  #######
			self.mechanism_of_action =[]
			if 'mechanism_of_action' in drug_keys:
				self.mechanism = drug_info['mechanism_of_action']  #######
			self.how_supplied = []
			if 'how_supplied' in drug_keys:
				self.how_supplied = drug_info['how_supplied']

			self.description_table =[]
			if 'description_table' in drug_fda:
				self.description_table = drug_info['description_table']			
			self.nursing_mothers =[]
			if 'nursing_mothers' in drug_keys:
				self.nursing_mothers = drug_info['nursing_mothers']
			self.clinical_pharmacology =[]
			if 'clinical_pharmacology' in drug_keys:
				self.pharmacology = drug_info['clinical_pharmacology']
			self.active_ingredient =[]
			if 'active_ingredient' in drug_fda:
				self.active_ingredient = drug_info['active_ingredient']  #######
			self.active_ingredient_table =[]
			if 'active_ingredient_table' in drug_fda:
				self.active_ingredient_table = drug_info['active_ingredient_table']  #######
			self.inactive_ingredient =[]
			if 'inactive_ingredient' in drug_fda:
				self.inactive_ingredient['inactive_ingredient'] = drug_info['inactive_ingredient']
			self.when_using_table =[]
			if 'when_using_table' in drug_fda:
				self.when_using_table  = drug_info['when_using_table'] 
			self.dosage_forms_and_strengths  = []
			if 'dosage_forms_and_strengths' in drug_fda:
				self.dosage_forms_and_strengths = drug_info['dosage_forms_and_strengths']
			self.dosage_forms_and_strengths_table  = []
			if 'dosage_forms_and_strengths_table' in drug_fda:
				self.dosage_forms_and_strengths_table =drug_info['dosage_forms_and_strengths_table']
			self.method_of_action = []
			if 'method_of_action' in drug_fda:
				self.method_of_actions =drug_info['method_of_action']


			self.pregnancy =[]
			if 'pregnancy' in drug_info:
				self.pregnancy = drug_info['pregnancy']   #######
			self.pregnancy_table =[]
			if 'pregnancy_table' in drug_info:
				self.pregnancy_table = drug_info['pregnancy_table']  #######
			self.labor_and_delivery =[]
			if 'labor_and_delivery' in drug_info:
				self.labor_delivery =   drug_info['labor_and_delivery']  #######
			self.carcinogenesis_and_mutagenesis_and_impairment_of_fertility = []
			if 'carcinogenesis_and_mutagenesis_and_impairment_of_fertility' in drug_info:
				self.carcinogenesis_and_mutagenesis_and_impairment_of_fertility =   drug_info['carcinogenesis_and_mutagenesis_and_impairment_of_fertility']
			self.pregnancy_or_breast_feeding =[]
			if 'pregnancy_or_breast_feeding' in drug_info:
				self.pregnancy_or_breast_feeding = drug_info['pregnancy_or_breast_feeding'] #######
			self.pregnancy_or_breast_feeding_table =[]
			if 'pregnancy_or_breast_feeding_table' in drug_info:
				self.pregnancy_or_breast_feeding_table = drug_info['pregnancy_or_breast_feeding_table'] #######
			self.nursing_mothers =[]
			if 'nursing_mothers' in drug_info:
				self.nursing_mothers = drug_info['nursing_mothers'] #######
			self.pediatric_use =[]
			if 'pediatric_use' in drug_info:
				self.pediatric_use = drug_info['pediatric_use']
			self.pediatric_use_table =[]
			if 'pediatric_use_table' in drug_info:
				self.pediatric_use_table = drug_info['pediatric_use_table']
			self.geriatric_use =[]
			if 'geriatric_use' in drug_info:
				self.geriatric_use = drug_info['geriatric_use']
			self.geriatric_use_table =[]
			if 'geriatric_use_table' in drug_info:
				self.nursing_mothers = drug_info['geriatric_use_table']
			self.use_in_specific_populations_table =[]
			if 'use_in_specific_populations_table' in drug_info:
				self.use_in_specific_populations_table = drug_info['use_in_specific_populations_table']
			self.use_in_specific_populations =[]
			if 'use_in_specific_populations' in drug_info:
				self.use_in_specific_populations = drug_info['use_in_specific_populations']

			self.storage_and_handling = []
			if 'storage_and_handling' in drug_info:
				self.storage_and_handling = drug_info['storage_and_handling']			##   35,264
			self.storage_and_handling_table = []
			if 'storage_and_handling_table' in drug_info:
				self.storage_and_handling_table = drug_info['storage_and_handling_table'] 			##   35,264
			self.safe_handling_warning_table = []
			if 'safe_handling_warning_table' in drug_info:
				self.safe_handling_warning_table = drug_info['safe_handling_warning_table']			##   35,264
			self.disposal_and_waste_handling = []
			if 'disposal_and_waste_handling' in drug_info:
				self.disposal_and_waste_handling = drug_info['disposal_and_waste_handling']		##   35,264
			self.safe_handling_warning = []
			if 'safe_handling_warning' in drug_info:
				self.safe_handling_warning = drug_info['safe_handling_warning']		##   35,264
			self.boxed_warning_table = []
			if 'boxed_warning_table' in drug_info:
				self.boxed_warning_table = drug_info['boxed_warning_table']			##   35,264
			self.how_supplied_table = []
			if 'how_supplied_table' in drug_info:
				self.how_supplied_table= drug_info['how_supplied_table'] 		##   35,264
			self.laboratory_tests = [] 
			if 'laboratory_tests' in drug_info:
				self.laboratory_tests = drug_info['laboratory_tests'] 
			self.laboratory_tests_table = [] 
			if 'laboratory_tests_table' in drug_info:
				self.laboratory_tests_table = drug_info['laboratory_tests_table']
			self.drug_and_or_laboratory_test_interactions_table = []
			if 'drug_and_or_laboratory_test_interactions_table' in drug_info:
				self.drug_and_or_laboratory_test_interactions_table= drug_info['drug_and_or_laboratory_test_interactions_table']
			self.drug_and_or_laboratory_test_interactions = []
			if 'drug_and_or_laboratory_test_interactions' in drug_info:
				self.drug_and_or_laboratory_test_interactions = drug_info['drug_and_or_laboratory_test_interactions'] 
		if 'unii' in drug_fda:
			self.unii = drug_fda['unii']
			##self.formatOuput(drug_fda)
	def write_html(self, text, file_output):

		file_output.write(text)
	def write_identifier(self,fileout):
		fileout.write('<table width=\"100%\">\n')
		fileout.write('<tr><th>Set ID</th> <th>Type</th> <th>Set ID</th>')
		fileout.write('<tr><td>' + self.monograph_id + '</td><td>' + self.product_type + '</td><td>' + self.set_id + '</td></tr>\n')
		fileout.write('</table>')
		fileout.write('<table width=\"100%\">\n')
		fileout.write('<tr><th>RxCUI</th> <th>UNII</th> <th>SPL SET ID</th>')
		fileout.write('<tr>')
		fileout.write('<td>')
		for rxcui_num in self.rxcui:
			fileout.write(rxcui_num + '<BR>\n')
		fileout.write('</td>')
		fileout.write('<td>')
		for unii in self.unii:
			fileout.write(unii + '<BR>\n')
		fileout.write('</td>')
		fileout.write('<td>')
		for spl_set_id_ in self.spl_set_id:
			fileout.write(spl_set_id_ + '<BR>')
		fileout.write('</td></tr></table>')
	def formatOuput(self,drug_fda):

		drug_monograph_fileout = open('../../PetOwnerPortal/DrugMonograph/' + self.monograph_id + '.html','w')
		drug_monograph_fileout.write('<HTML>\n<HEAD>\n')
		drug_monograph_fileout.write('<link rel=\"stylesheet\" type=\"text/css\" href=\"../style_sheets/monograph.css\">\n')
		drug_monograph_fileout.write('</HEAD>\n<BODY>\n')

		drug_monograph_fileout.write('<table width=\"100%\">\n')
		drug_monograph_fileout.write('<tr><th>Brand Name</th> <th>Pharma Class EPC</th>')
		drug_monograph_fileout.write('<tr>')
		drug_monograph_fileout.write('<td>')
		if 'brand_name' in drug_fda:
			for brand in drug_fda['brand_name']:
				self.write_html(str(brand)+'</br>\n', drug_monograph_fileout)
		drug_monograph_fileout.write('</td>')
		drug_monograph_fileout.write('<td>')
		if self.pharm_class_epc != None:
			for pharmClass in self.pharm_class_epc:
				self.write_html(pharmClass+'<br>\n', drug_monograph_fileout)
		if self.pharm_class_pe != None:
			for pharmaPE in self.pharm_class_pe:
				self.write_html(pharmaPE+'<br>\n', drug_monograph_fileout)
		if self.pharm_class_moa != None:
			for pharmClass in self.pharm_class_moa:
				self.write_html(pharmClass+'<br>\n', drug_monograph_fileout)
		if self.pharm_class_cs != None:
			for pClass in self.pharm_class_cs:
				self.write_html(pClass+'<br>\n', drug_monograph_fileout)
		drug_monograph_fileout.write('</td>')
		drug_monograph_fileout.write('</tr></table>')

		self.write_identifier(drug_monograph_fileout)

		for spl_id_num in self.spl_id:
			self.write_html('<h4>SPL ID: ' + spl_id_num + '</h4>\n', drug_monograph_fileout)
		for ndc_num in self.product_ndc:
			self.write_html('<h4>PRODUCT NDC: ' + ndc_num + '</h4>\n', drug_monograph_fileout)
		for spl_product_data_element_item in self.product_data_elements:
			self.write_html('<h4>SPL Product Data Elements: ' + spl_product_data_element_item +'</h4>\n', drug_monograph_fileout)

		self.write_indications(drug_monograph_fileout)
		self.write_description(drug_monograph_fileout)
		self.write_ingredients(drug_monograph_fileout)
		self.write_howsupplied(drug_monograph_fileout)
		self.write_dosage_admin(drug_monograph_fileout)
		
		self.write_pregnancy(drug_monograph_fileout)
		self.write_pharmacokinetics(drug_monograph_fileout)

		self.write_contraindications(drug_monograph_fileout)
		self.write_precautions(drug_monograph_fileout)

		self.write_adverse(drug_monograph_fileout)
		self.write_druginteractions(drug_monograph_fileout)

		drug_monograph_fileout.close()
	def write_indications(self,fileout):
		if len(self.indications_usage) > 0:
			self.write_html('<h3>INDICATIONS</h3>\n',fileout)
			for indication in self.indications_usage:
				##self.indications_regex(indication,fileout)
				##self.ngrams_indications(indication,4,fileout)
				self.write_html('<p>' + indication, fileout)
	def indications_regex(self,indication_text,fileout):
		indications_terms = None
		results = indication_type_treatment.match(indication_text)
		results2 = indication_type_relief.match(indication_text)
		results3 = indication_type_management.match(indication_text)
		results4 = indication_type_adjunctive.match(indication_text)

		if results != None:
			match_groups = results.groups()
			print (results.group(2))

		if results2 != None:
			match_groups = results2.groups()
			print (results2.group(2))

		if results3 != None:
			match_groups = results3.groups()
			print (results3.group(2))

		if results4 != None:
			match_groups = results4.groups()
			print (results4.group(2))
	def ngrams_indications(self,sentence,number,fileout):
		ngramresults = ngrams(sentence.split(),number)
		terms_dic = {}
		for words in ngramresults:
			word1 = words[0].lower()
			word2 = words[1].lower()
			word3 = words[2].lower()
			word4 = words[3].lower()


			compare_indication_onto_keys = self.ontology_indications.keys()

			for indication_key in compare_indication_onto_keys:
				compare_word_array = []
				mWord = self.ontology_indications[indication_key]
				match1 = False
				match2 = False				
				match3 = False
				match4 = False
				match_ngram = False
				for word_multi in mWord:
					if word_multi == word1:
						match1 = True 
					elif word_multi == word2:
						match2 = True
					elif word_multi == word3:
						match3 = True
					elif word_multi == word4:
						match4 = True

				if match1 and match2 and match3 and match4:
					match_word = mWord[0] + ' ' + mWord[1] + ' ' + mWord[2] + ' ' + mWord[3]
					terms_dic[match_word] = indication_key
					match_ngram = True
					##print ('indications ngrams for: ' + self.generic_name + str(words))


				elif match1 and match2 and match3 and not match_ngram:
					match_word =mWord[0] + ' ' + mWord[1] + ' ' + mWord[2]
					terms_dic[match_word] = indication_key
					match_ngram = True
					##print ('indications ngrams for: ' + self.generic_name + str(words))

				elif match1 and match2 and not match_ngram:
					match_word =mWord[0] + ' ' + mWord[1]
					terms_dic[match_word] = indication_key
					match_ngram = True
					##print ('indications ngrams for: ' + self.generic_name + str(words))


				elif match1 and not match_ngram:
					match_word = mWord[0]
					terms_dic[match_word] = match_word
					match_ngram = True
					##print ('indications ngrams for: ' + self.generic_name + str(words))
							

		fileout.write('<H3>Matched</h3>\n' )
		fileout.write('<p>\n')
		match_keys = terms_dic.keys()
		for key in match_keys:
			fileout.write(key + ' | ')
			num_keys = key.split()
			##if len(num_keys) > 1:
			##	print (key + '\n')
		fileout.write('</p><br>')
	def write_description(self,fileout):
		if len(self.purpose_table) > 0:
			self.write_html('<h3>PURPOSE TABLE</h3>\n',fileout)
			for purpose in self.purpose_table:
				self.write_html('<p>' + purpose, fileout)
		if len(self.description_table) > 0:
			self.write_html('<h3>DESCRIPTION TABLE</h3>\n',fileout)
			for descrip in self.description_table:
				self.write_html('<p>' + descrip, fileout)
		if len(self.description) > 0:
			self.write_html('<h3>DESCRIPTION</h3>\n',fileout)
			for desc in self.description:
				self.write_html('<p>' + desc, fileout)
		if len(self.information_for_patients) > 0:
			self.write_html('<h3>INFORMATION FOR PATIENTS</h3>\n',fileout)
			for info in self.information_for_patients:
				self.write_html('<p>' + info, fileout)
		if len(self.instructions_for_use) > 0:
			self.write_html('<h3>INSTRUCTIONS FOR USE</h3>\n',fileout)
			for instruct in self.instructions_for_use:
				self.write_html('<p>' + instruct, fileout)
		if len(self.purpose) > 0:
			self.write_html('<h3>PURPOSE</h3>\n',fileout)
			for purp in self.purpose:
				self.write_html('<p>' + purp, fileout)
	def write_ingredients(self,fileout):
		if len(self.active_ingredient) > 0:
			self.write_html('<h3>ACTIVE INGREDIENTS</h3>\n',fileout)
			for ingredient in self.active_ingredient:
				self.write_html('<p>' + ingredient, fileout)
		if len(self.active_ingredient_table) > 0:
			self.write_html('<h3>ACTIVE INGREDIENTS</h3>\n',fileout)
			for ingredient in self.active_ingredient_table:
				self.write_html('<p>' + ingredient, fileout)
	def write_howsupplied(self,fileout):
		if len(self.how_supplied) > 0:
			self.write_html('<h3>HOW SUPPLIED</h3>\n',fileout)
			for supplied in self.how_supplied:
				self.write_html('<p>' + supplied, fileout)	
	def write_dosage_admin(self,fileout):
		if len(self.dosage_admin) > 0:
			self.write_html('<H3>DOSAGE AND ADMIN\n',fileout)
			for dose in self.dosage_admin:
				self.write_html('<p>' + dose)
		if len(self.dosage_and_administration_table) > 0:
			self.write_html('<H3>DOSAGE AND ADMIN TABLE\n',fileout)
			for dose in self.dosage_and_administration_table:
				self.write_html(dose,fileout)
		if len(self.route) > 0:
			self.write_html('<H3>ROUTE</H3>\n',fileout)
			for r in self.route:
				self.write_html(r,fileout)
	def write_pregnancy(self,fileout):
		if len(self.pregnancy) > 0:
			self.write_html('<h3>PREGNANCY</h3>\n',fileout)
			for preg in self.pregnancy:
				self.write_html('<p>' + preg, fileout)
		if len(self.pregnancy_table) > 0:
			self.write_html('<h3>PREGNANCY</h3>\n',fileout)
			for preg in self.pregnancy_table:
				self.write_html('<p>' + preg, fileout)
		if len(self.labor_and_delivery) > 0:
			self.write_html('<h3>LABOR AND DELIVERY</h3>\n',fileout)
			for labor in self.labor_and_delivery:
				self.write_html('<p>' + labor, fileout)
		if len(self.pregnancy_or_breast_feeding) > 0:
			self.write_html('<h3>PREGNANCY AND BREASTFEEDING</h3>\n',fileout)
			for preg_bf in self.pregnancy_or_breast_feeding:
				self.write_html('<p>' + preg_bf, fileout)

		if len(self.pregnancy_or_breast_feeding_table) > 0:
			self.write_html('<h3>PREGNANCY AND BREASTFEEDING</h3>\n',fileout)
			for preg_bf in self.pregnancy_or_breast_feeding_table:
				self.write_html('<p>' + preg_bf, fileout)

		if len(self.nursing_mothers) > 0:
			self.write_html('<h3>NURSING MOTHERS</h3>\n',fileout)
			for nursing in self.nursing_mothers:
				self.write_html('<p>' + nursing, fileout)
	def write_pharmacokinetics(self,fileout):
		if len(self.pharmacokinetics) > 0:
			self.write_html('<h3>PHARMACOKINETICS</h3>\n',fileout)
			for pharma in self.pharmacokinetics:
				self.write_html('<p>' + pharma, fileout)
		if len(self.pharmacokinetic_table) > 0:
			self.write_html('<h3>PHARMACOKINETIC TABLE</h3>\n',fileout)
			for pk in self.pharmacokinetic_table:
				self.write_html('<p>' + pk, fileout)
	def write_contraindications(self,fileout):
		if len(self.contraindications) > 0:
			self.write_html('<h3>CONTRAINDICATIONS</h3>\n',fileout)
			for contraindication in self.contraindications:
				self.write_html('<p>' + contraindication, fileout)
		if len(self.contraindications_table) > 0:
			self.write_html('<h3>CONTRAINDICATIONS TABLE</h3>\n',fileout)
			for contraindication in self.contraindications_table:
				self.write_html('<p>' + contraindication, fileout)
	def write_precautions(self,fileout):
		if len(self.warnings) > 0:
			self.write_html('<h3>WARNINGS</h3',fileout)
			for warning in self.warnings:
				self.write_html(warning,fileout)
		if len(self.precautions) > 0:
			self.write_html('<h3>PRECAUTIONS</h3>',fileout)
			for precaution in self.precautions:
				self.write_html(precaution,fileout)
		if len(self.general_precautions) > 0:
			self.write_html('<h3>GENERAL PRECAUTIONS</h3>',fileout)
			for gen_pre in self.general_precautions:
				self.write_html(gen_pre,fileout)
		if len(self.general_precautions_table):
			self.write_html('<h3>GENERAL PRECAUTIONS TABLE</h3>',fileout)
			for gen_tbl in self.general_precautions_table:
				self.write_html(gen_tbl,fileout)
		if len(self.boxed_warning):
			self.write_html('<h3>BOXED WARNING</h3>',fileout)
			for boxed in self.boxed_warning:
				self.write_html(boxed,fileout)	
	def write_druginteractions(self,fileout):
		if len(self.drug_interactions) >0:
			self.write_html('<h3>INTERACTIONS</h3>\n',fileout)
			for interaction in self.drug_interactions:
				self.ddi_parse(interaction,fileout)
		if len(self.drug_interactions_table) >0:
			self.write_html('<h3>INTERACTIONS TABLE</h3>\n',fileout)
			for interaction in self.drug_interactions_table:
				##self.ddi_parse(interaction,fileout)
				soup = BeautifulSoup(interaction,'lxml')
				table = soup.find_all('table')[0]
				table_headers = soup.find_all('th')
				print ('Headers: ' + str(table_headers))
				for row in table.find_all('tr'):
					cells = row.find_all('td')
					if len(cells) > 0:
						for i in range(len(cells)):
							if len(table_headers) > 0:
								med_with_header = str(cells[i].find(text=True))
								med_term = cells[i].find(text=True)
								self.ddi_parsed.append(med_with_header)
								print(str(cells[i].find(text=True)))
								print (med_term)
							else:
								med_with_header = 'No header: ' + str(cells[i].find(text=True))
								med_term = cells[i].find(text=True)
								self.ddi_parsed.append(med_with_header)
								print( 'No header: ' + str(cells[i].find(text=True)))
								print (med_term)
	def ddi_parse(self, ddi_text,fileout):
		ddi_elems = ddi_re.split(ddi_text)
		for elem in ddi_elems:
			self.write_html('<div><p>' + elem + '</p></div><br>',fileout)
			ddi_results = ddi_re_1.match(elem)
			if ddi_results != None:
				match_groups = ddi_results.groups()
				##match_text = ddi_results(2) + ' ' + ddi_results(3) + ' ' + ddi_results(4)
				##print (match_text)
			self.find_cyp_marker(elem,fileout)
	def cyp_ngrams(self, cyp_text):
		ngramresults = ngrams(cyp_text.split(),3)
		for words in ngramresults:
			print (words)
	def find_cyp_marker(self, cyp_text,fileout):

		results = cyp_re_t.match(cyp_text)

		if results != None:
			match_groups = results.groups()
			self.write_html('<div>\n',fileout)
			self.write_html('<table><tr><th>CYP Term</th><th>Results</th></tr>\n',fileout)
			self.write_html('<tr><td>' +  results.group(1) + '</td><td>' +results.group(2) + '</td></tr></table></div><br>\n',fileout)
			print (self.generic_name + results.group(2))

		results = cyp_re_t2.match(cyp_text)

		if results != None:
			match_groups = results.groups()
			self.write_html('<div>\n',fileout)
			self.write_html('<table><tr><th>CYP Term</th><th>Results</th></tr>\n',fileout)
			self.write_html('<tr><td>' +  results.group(1) + '</td><td>' +results.group(2) + '</td></tr></table></div><br>\n',fileout)
			print (self.generic_name + results.group(2))

		results = cyp_re_t3.match(cyp_text)

		if results != None:
			match_groups = results.groups()
			self.write_html('<div>\n',fileout)
			self.write_html('<table><tr><th>CYP Term</th><th>Results</th></tr>\n',fileout)
			self.write_html('<tr><td>' +  results.group(1) + '</td><td>' +results.group(2) + '</td></tr></table></div><br>\n',fileout)
			print (self.generic_name + results.group(2))

		results = cyp_increase_effect.match(cyp_text)

		if results != None:
			match_groups = results.groups()
			self.write_html('<div>\n',fileout)
			self.write_html('<table><tr><th>CYP Term</th><th>Results</th></tr>\n',fileout)
			self.write_html('<tr><td>' +  results.group(1) + '</td><td>' +results.group(2) + '</td></tr></table></div><br>\n',fileout)
			print (self.generic_name + results.group(2))
		
		results = cyp_decrease_effect.match(cyp_text)

		if results != None:
			match_groups = results.groups()
			self.write_html('<div>\n',fileout)
			self.write_html('<table><tr><th>CYP Term</th><th>Results</th></tr>\n',fileout)
			self.write_html('<tr><td>' +  results.group(1) + '</td><td>' +results.group(2) + '</td></tr></table></div><br>\n',fileout)
			print (self.generic_name + results.group(2))
	def find_ngram_indication(self, sentence, number, fileout):
 		ngramresults = ngrams(sentence.split(),number)
 		terms_array = []
 		for words in ngramresults:
 			numWord = len(words)
 			counter = 0
 			adver_term_multi = []
 			num_match_words = 0
 			word1 = words[0]
 			word2 = words[1]
 			word3 = words[2]
 			word4 = words[3]
	def find_ngrams(self,sentence, number,fileout):
		ngramresults = ngrams(sentence.split(),number)
		terms_dic = {}
		ngrams_counter = 0
		for words in ngramresults:
			word1 = words[0].lower()
			word2 = words[1].lower()
			word3 = words[2].lower()
			word4 = words[3].lower()
			compare_ontology_keys = self.multi_ontology.keys()
			for compare_word_key in compare_ontology_keys:
				compare_word_array = []
				mWord = self.multi_ontology[compare_word_key]
				match1 = False
				match2 = False				
				match3 = False
				match4 = False
				match_ngram = False

				for word_multi in mWord:
					if word_multi == word1:
						match1 = True 
					elif word_multi == word2:
						match2 = True
					elif word_multi == word3:
						match3 = True
					elif word_multi == word4:
						match4 = True

				if match1 and match2 and match3 and match4:
					match_word = mWord[0] + ' ' + mWord[1] + ' ' + mWord[2] + ' ' + mWord[3]
					##print ('ngram match 4: ' + match_word)
					##print ('ngrams for: ' + self.generic_name + str(words))
					terms_dic[match_word] = compare_word_key
					match_ngram = True

				elif match1 and match2 and match3 and not match_ngram:
					match_word =mWord[0] + ' ' + mWord[1] + ' ' + mWord[2]
					#3print ('ngram match 3: ' + match_word)
					##print ('ngrams for: ' + self.generic_name + str(words))
					terms_dic[match_word] = compare_word_key
					match_ngram = True

				elif match1 and match2 and not match_ngram:
					match_word =mWord[0] + ' ' + mWord[1]
					##print ('ngram match 3 : ' + match_word)
					##print ('ngrams for: ' + self.generic_name + str(words))
					terms_dic[match_word] = compare_word_key
					match_ngram = True

				elif match1 and not match_ngram:
					match_word = mWord[0]
					##print ('ngram match 1: ' + match_word)
					##print ('ngrams for: ' + self.generic_name + str(words))
					terms_dic[match_word] = match_word
					match_ngram = True

		fileout.write('<H3>Matched</h3>\n' )
		fileout.write('<p>\n')
		match_keys = terms_dic.keys()
		for key in match_keys:
			fileout.write(key + ' | ')
			num_keys = key.split()
			##if len(num_keys) > 1:
			##	print (key + '\n')
		fileout.write('</p><br>')
	def setup_drug_fields(self):
		self.drugfields['food_safety_warning'] = 'None'				## 1
		self.drugfields['stop_use'] = 'None'
		self.drugfields['stop_use_table'] = 'None'
		self.drugfields['do_not_use'] = 'None'
		self.drugfields['do_not_use_table'] = 'None'
		self.drugfields['other_safety_information'] = 'None'
		self.drugfields['user_safety_warnings'] = 'None'
		self.drugfields['keep_out_of_reach_of_children'] = 'None'
		self.drugfields['keep_out_of_reach_of_children_table'] = 'None'
		self.drugfields['abuse'] = 'None'
		self.drugfields['abuse_table'] = 'None'
		self.drugfields['dependence'] = 'None'
		self.drugfields['dependence_table'] = 'None'
		self.drugfields['drug_abuse_and_dependence'] = 'None'			## 9,633
		self.drugfields['drug_abuse_and_dependence_table'] = 'None'		##     36
		self.drugfields['controlled_substance'] = 'None'
		self.drugfields['overdosage'] = 'None'
		self.drugfields['overdosage_table'] = 'None'
		self.drugfields['ask_doctor_table'] = 'None'
		self.drugfields['ask_doctor_or_pharmacist_table'] = 'None'
		self.drugfields['ask_doctor_or_pharmacist'] = 'None'
		self.drugfields['instructions_for_use_table'] = 'None'
		self.drugfields['ask_doctor'] = 'None'
		self.drugfields['questions'] = 'None'
		self.drugfields['when_using'] = 'None'
		self.drugfields['information_for_owners_or_caregivers'] = 'None'
		self.drugfields['information_for_owners_or_caregivers_table'] = 'None'
		self.drugfields['questions_table'] = 'None'
		self.drugfields['troubleshooting'] = 'None'
		##self.drugfields['information_for_patients'] = 'None'
		self.drugfields['information_for_patients_table'] = 'None'
		self.drugfields['patient_medication_information'] = 'None'
		self.drugfields['patient_medication_information_table'] = 'None'
		self.drugfields['pharmacodynamics_table'] = 'None'
		self.drugfields['pharmacodynamics'] = 'None'
		self.drugfields['pharmacogenomics'] = 'None'
		self.drugfields['pharmacogenomics_table'] = 'None'
		self.drugfields['mechanism_of_action_table'] = 'None'
		self.drugfields['clinical_pharmacology_table'] = 'None'
		self.drugfields['clinical_studies'] = 'None'
		self.drugfields['clinical_studies_table'] = 'None'
		self.drugfields['animal_pharmacology_and_or_toxicology'] = 'None'
		self.drugfields['animal_pharmacology_and_or_toxicology_table'] = 'None'
		self.drugfields['nonclinical_toxicology_table'] = 'None'
		self.drugfields['carcinogenesis_and_mutagenesis_and_impairment_of_fertility'] = 'None'

		self.drugfields['teratogenic_effects'] = 'None'
		self.drugfields['teratogenic_effects_table'] = 'None'
		self.drugfields['nonteratogenic_effects'] = 'None'
		self.drugfields['nonteratogenic_effects_table'] = 'None'
		self.drugfields['carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table'] = 'None'
		self.drugfields['microbiology'] = 'None'
		self.drugfields['microbiology_table'] = 'None'
		self.drugfields['nonclinical_toxicology'] = 'None'
		self.drugfields['recent_major_changes'] = 'None'
		self.drugfields['recent_major_changes_table'] = 'None'
		self.drugfields['effective_time'] = 'None'
		self.drugfields['health_claim'] = 'None'
		self.drugfields['health_claim_table'] = 'None'
		self.drugfields['health_care_provider_letter'] = 'None'
		self.drugfields['health_care_provider_letter_table'] = 'None'
		self.drugfields['assembly_or_installation_instructions'] = 'None'
		self.drugfields['other_safety_information_table'] = 'None'
		self.drugfields['accessories'] = 'None'
		self.drugfields['references'] = 'None'
		self.drugfields['references_table'] = 'None'
		self.drugfields['alarms'] = 'None'
		self.drugfields['alarms_table'] = 'None'
		self.drugfields['cleaning'] = 'None'
		self.drugfields['environmental_warning'] = 'None'
		self.drugfields['statement_of_identity_table'] = 'None'
		self.drugfields['inactive_ingredient_table'] = 'None'
		self.drugfields['intended_use_of_the_device'] = 'None'
		self.drugfields['guaranteed_analysis_of_feed'] = 'None'
		self.drugfields['components'] = 'None'
		self.drugfields['statement_of_identity'] = 'None'
		self.drugfields['veterinary_indications'] = 'None'
		self.drugfields['calibration_instructions'] = 'None'
		self.drugfields['residue_warning'] = 'None'
	def parse_adverse_table(self,adverse_text):
		soup = BeautifulSoup(adverse_text, 'lxml')
		table = soup.find_all('table')[0]
		table_headers = soup.find_all('th')
		##print ('Headers: ' + str(table_headers))
		for row in table.find_all('tr'):
			cells = row.find_all('td')
			if len(cells) > 0:
				for i in range(len(cells)):
					##print (str(len(table_headers)))
					if len(table_headers) > 0:
						med_with_header = str(cells[i].find(text=True))
						##print(med_with_header)
						self.regex_adverse_match_table_terms.append(med_with_header)
					else:
						##print(str(cells[i].find(text=True)))
						med_with_header ='No header: ' + str(cells[i].find(text=True))
						self.regex_adverse_match_table_terms.append(med_with_header)

					med_term = cells[i].find(text=True)
					##print (med_term)
	def write_adverse(self,fileout):
		if len(self.adverse_reactions) > 0:
			self.write_html('<h3>ADVERSE</h3>\n',fileout)
			if self.product_type == 'HUMAN PRESCRIPTION DRUG':
				for adverse in self.adverse_reactions:
					self.adverse_parse(adverse,fileout)

		if len(self.adverse_reactions_table) > 0:
			if self.product_type == 'HUMAN PRESCRIPTION DRUG':
				for adverse_tab in self.adverse_reactions_table:
					print('ADVERSE TABLE FINDING NGRAMS')
					self.parse_adverse_table(adverse_tab)
					self.write_html('<h3>ADVERSE TABLE</h3>\n',fileout)
					self.write_html('<div><p>'+ adverse_tab  + '</div><br><br>',fileout)
	def adverse_parse(self,adv_text, fileout):
		adv_elem = adv_re_spilt.split(adv_text)
		self.adverse_regex_parse(adv_text,fileout)
		for elem in adv_elem:
			self.write_html('<div><p>' + elem + '</p><br><br></div><br>',fileout)
	def check_regex(self,adverse_text,reg_ex,fileout):
		regex_results = reg_ex.match(adverse_text)
		if regex_results != None:
			match_groups = regex_results.groups()
			print ('Number of match group elements: '  + str(len(match_groups)))
			term_list = regex_results.group(3)
			term_arr= term_list.split(',')
			self.write_html('<div><table><tr><th>Match term</th><th>Match</th></tr>\n',fileout)
			self.write_html('<tr><td>' + regex_results.group(2) + '</td><td>' + regex_results.group(3) + '</td><td></tr></table></div><br>\ngrams',fileout)
			print ('subroutine ADVERSE PARSE FOR ' + self.generic_name)
			for term in term_arr:
				self.adverse_parse_terms[self.generic_name] = term
				self.write_html('<div><p>' + term + '</p><br><br></div><br>',fileout)
				self.regex_adverse_match_terms.append(term)
			return True
		else:
			self.regex_adverse_analysis.append(adverse_text)
			return False
	def adverse_regex_parse(self,adv_text,fileout):
		adverse_terms = None
		found_match = False
		regex_results = None

		for regex in regex_array:
			check_results = self.check_regex(adv_text, regex,fileout)
			if check_results == True:
				found_match = True

		if not found_match:
			print(adv_text)
			##self.regex_adverse_analysis.append(adv_text)

## The following serious adverse reactions are discussed below and elsewhere in the labeling
## The following serious adverse reactions are described, or described in greater detail, in other sections
## The following serious adverse reactions are described elsewhere in the labeling:
## Some patients may develop
## Most common adverse reactions (incidence ≥5%) are:
## The following clinically significant adverse reactions are described elsewhere in labeling:
##  The most common reactions (≥3%) were
## The most commonly reported infusion reactions occurring in at least 10% of patients 6 months of age and older were
##  The following serious adverse reactions are described below and elsewhere in the labeling:
##  The most common adverse reaction in adults was
##  The following adverse reactions are discussed elsewhere in the labeling:
## The most common side effect reported with PROCARDIA XL was edema which was dose related and ranged in 
## frequency from approximately 10% to about 30% at the highest dose studied (180 mg). Other common adverse experiences 
## reported in placebo-controlled trials include: Adverse Effect PROCARDIA XL (%) (N=707) Placebo (%) (N=266) 
## Headache 15.8 9.8 
## Fatigue 5.9 4.1 
## Dizziness 4.1 4.5 
## Constipation 3.3 2.3 
## Nausea 3.3 1.9

		##self.drugfields['laboratory_tests'] = 'None'
		##self.drugfields['laboratory_tests_table'] = 'None'
		##self.drugfields['drug_and_or_laboratory_test_interactions_table'] = 'None'
		##self.drugfields['drug_and_or_laboratory_test_interactions'] = 'None'
		##self.drugfields['pharmacokinetics'] = 'None'
		##self.drugfields['pharmacokinetics_table'] = 'None'
		##self.drugfields['mechanism_of_action'] = 'None'
		##self.drugfields['clinical_pharmacology'] = 'None'
		##self.drugfields['labor_and_delivery'] = 'None'
		##self.drugfields['nursing_mothers'] = 'None'
		##self.drugfields['use_in_specific_populations_table'] = 'None'
		##self.drugfields['use_in_specific_populations'] = 'None'
		## IDENTIFICATION - SPL, PACKAGE LABELING, ID
		##self.drugfields['openfda'] = 'None'					## 114,337
		##self.drugfields['id'] = 'None'						## 114,337
		##self.drugfields['version'] = 'None'					## 114,337
		##self.drugfields['spl_product_data_elements'] = 'None'			## 113,811
		##self.drugfields['set_id'] = 'None'					## 114,337
		##self.drugfields['spl_unclassified_section'] = 'None'			##  48,037
		##self.drugfields['spl_medguide'] = 'None' 				##    9,296
		##self.drugfields['spl_unclassified_section_table'] = 'None' 		## 2,805
		##self.drugfields['spl_patient_package_insert_table'] = 'None' 		## 1,505
		##self.drugfields['spl_medguide_table'] = 'None'				## 3,952
		##self.drugfields['spl_patient_package_insert'] = 'None'			## 1,505
		##self.drugfields['spl_indexing_data_elements'] = 'None'		##    10
		##self.drugfields['package_label_principal_display_panel_table'] = 'None'	## 401
		##self.drugfields['package_label_principal_display_panel'] = 'None' 	##113,723
		## INDICATIONS AND DESCRIPTION
		##self.drugfields['indications_and_usage'] = 'None'			## 108,563	
		##self.drugfields['indications_and_usage_table'] = 'None'		##     1,017
		##self.drugfields['description'] = 'None'				##  47,244
		##self.drugfields['purpose'] = 'None'					##  64,685
		##self.drugfields['instructions_for_use'] = 'None'			##   1,708
		##uself.drugfields['purpose_table'] = 'None'				##    2,492
		##self.drugfields['description_table'] = 'None'				##     2,362

		## DOSAGE AND ADMINISTRATION, STORAGE, HANDLING
		##self.drugfields['active_ingredient'] = 'None'				## 66,795
		##self.drugfields['active_ingredient_table'] = 'None'			##  2,838
		##self.drugfields['inactive_ingredient'] = 'None'				
		##self.drugfields['when_using_table'] = 'None'
		##self.drugfields['dosage_and_administration'] = 'None'		## 108,072
		##self.drugfields['dosage_and_administration_table'] = 'None'	##   21,336
		##self.drugfields['route'] = 'None'					## 	  50
		##self.drugfields['dosage_forms_and_strengths'] = 'None'		##   14,656
		##self.drugfields['dosage_forms_and_strengths_table'] = 'None'		##	549


		##self.drugfields['how_supplied'] = 'None'				##   44,541

		## CONTRAINDICATIONS, BOXED WARNING, PRECAUTIONS, RISKS, WARNINGS
		## DRUG INTERACTIONS, ADVERSE REACTIONS, FOOD SAFETY, STOP USE
		##self.drugfields['contraindications'] = 'None'					## 44,188
		##self.drugfields['contraindications_table'] = 'None'				##       145
		##self.drugfields['precautions'] = 'None'					##  29,629
		##self.drugfields['general_precautions'] = 'None'				##  17,055
		##self.drugfields['warnings'] = 'None'
		##self.drugfields['boxed_warning'] = 'None'					##  16,218

		##self.drugfields['geriatric_use'] = 'None'
		##self.drugfields['geriatric_use_table'] = 'None'
		##self.drugfields['pediatric_use'] = 'None'
		##self.drugfields['pediatric_use_table'] = 'None'
		##self.drugfields['adverse_reactions'] = 'None'				## 45,368
		##self.drugfields['adverse_reactions_table'] = 'None'				## 20,495

			##self.drugfields['storage_and_handling'] = 'None'
			##self.drugfields['how_supplied_table'] = 'None'				
			##self.drugfields['storage_and_handling_table'] = 'None'		
			##self.drugfields['safe_handling_warning_table'] = 'None'
			##self.drugfields['disposal_and_waste_handling'] = 'None'
			##self.drugfields['safe_handling_warning'] = 'None'
			##self.drugfields['boxed_warning_table'] = 'None'				
			##self.drugfields['summary_of_safety_and_effectiveness'] = 'None'		
			##self.drugfields['general_precautions_table'] = 'None'				
			##self.drugfields['risks'] = 'None'
			##self.drugfields['risks_table'] = 'None'
			##self.drugfields['warnings_and_cautions'] = 'None'
			##self.drugfields['warnings_and_cautions_table'] = 'None'
			##self.drugfields['warnings_table'] = 'None'
			##self.drugfields['food_safety_warning'] = 'None'				
			##self.drugfields['stop_use'] = 'None'
			##self.drugfields['stop_use_table'] = 'None'
			##self.drugfields['risks'] = 'None'
			##self.drugfields['do_not_use'] = 'None'
			##self.drugfields['do_not_use_table'] = 'None'
			##self.drugfields['other_safety_information'] = 'None'
			##self.drugfields['user_safety_warnings'] = 'None'
			##self.drugfields['keep_out_of_reach_of_children'] = 'None'
			##self.drugfields['keep_out_of_reach_of_children_table'] = 'None'
			##self.drugfields['abuse'] = 'None'
			##self.drugfields['abuse_table'] = 'None'
			##self.drugfields['dependence'] = 'None'
			##self.drugfields['dependence_table'] = 'None'
			##self.drugfields['drug_abuse_and_dependence'] = 'None'			## 9,633
			##self.drugfields['drug_abuse_and_dependence_table'] = 'None'		##     36
			##self.drugfields['controlled_substance'] = 'None'
			##self.drugfields['overdosage'] = 'None'
			##self.drugfields['overdosage_table'] = 'None'
			##self.drugfields['ask_doctor_table'] = 'None'
			##self.drugfields['ask_doctor_or_pharmacist_table'] = 'None'
			##self.drugfields['ask_doctor_or_pharmacist'] = 'None'
			##self.drugfields['instructions_for_use_table'] = 'None'
			##self.drugfields['ask_doctor'] = 'None'
			##self.drugfields['questions'] = 'None'
			##self.drugfields['when_using'] = 'None'
			##self.drugfields['information_for_owners_or_caregivers'] = 'None'
			##self.drugfields['information_for_owners_or_caregivers_table'] = 'None'
			##self.drugfields['questions_table'] = 'None'
			##self.drugfields['troubleshooting'] = 'None'
			##self.drugfields['information_for_patients'] = 'None'
			##self.drugfields['information_for_patients_table'] = 'None'
			##self.drugfields['patient_medication_information'] = 'None'
			##self.drugfields['patient_medication_information_table'] = 'None'
			## LIFE STAGE / SPECIAL POPULATIONS
		##self.drugfields['storage_and_handling'] = 'None'			##   35,264
		##self.drugfields['how_supplied_table'] = 'None'				##     6,856
		##self.drugfields['storage_and_handling_table'] = 'None'		## 	123
		##self.drugfields['safe_handling_warning_table'] = 'None'
		##self.drugfields['disposal_and_waste_handling'] = 'None'
		##self.drugfields['safe_handling_warning'] = 'None'
		##self.drugfields['boxed_warning_table'] = 'None'	

		##self.drugfields['general_precautions_table'] = 'None'				##       213
		##self.drugfields['risks'] = 'None'
		##self.drugfields['risks_table'] = 'None'
		##self.drugfields['warnings_and_cautions'] = 'None'
		##self.drugfields['warnings_and_cautions_table'] = 'None'
		##self.drugfields['warnings_table'] = 'None'
		##self.drugfields['drug_interactions'] = 'None'
		##self.drugfields['drug_interactions_table'] = 'None'

		##self.drugfields['pregnancy_or_breast_feeding'] = 'None'			## 19,271
		##self.drugfields['pregnancy_or_breast_feeding_table'] = 'None'

		##self.drugfields['pregnancy'] = 'None'
		##self.drugfields['pregnancy_table'] = 'None'	