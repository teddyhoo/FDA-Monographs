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
		drug_monograph = drug_fda
		if len(drug_keys) < 5:
			print(str(drug_monograph))

		self.id = drug_info['id']
		self.rxcui = 'No RXCUI'
		self.generic_name = 'No generic'
		self.brand_name = 'No brand name'
		self.product_ndc = 'No PRODUCT NDC'
		self.spl_id = 'No SPL id'
		self.spl_set_id = 'No SPL set id'		
		self.product_id = 'No product_id'

		self.UMLS_CUI = 'No UMLS'
		self.MeSH_DUI = 'No MESH DUI'
		self.MeSH_Description = 'No MeSH Description'

		self.pharm_class = 'No Pharma' 
		self.pharm_class_pe = 'No Pharma PE'
		self.product_type = 'No Product Type'
		self.manufacturer_name = 'No Mfr'
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
