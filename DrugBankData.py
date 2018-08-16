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

class DrugBank:
	def __init__(self,drugbank_id,drugbank_element):
		self.drugbank_id = drugbank_id
		self.unii = ''
		self.drug_name = ''
		self.indication = ''
		self.description = ''
		self.pharmacodynamics = ''
		self.mechanism_of_action = ''
		self.toxicity = ''
		self.absorption = ''
		self.route_of_elimination = ''
		self.half_life = ''
		self.state = ''
		self.clearance = ''
		self.metabolism = ''
		self.effects = []
		self.drug_interactions = []
		self.food_interactions = []
		self.adverse_reactions = []
		self.products = []
		self.dosages_arr = []
		self.categories = []
		self.sequences = []
		self.atc_codes = []

		self.metab = []
		self.serum = []
		self.thera = []
		self.excretion = []
		self.absorption_arr = []
		self.risk_severity = []
		self.bioavailability = []
		self.activity_inc_dec = []
		self.other_ddi_array = []
		self.categories = [] 
		self.parsed_indication = []

		self.parse = 'false'
		self.indication_noun = ''
		self.indication_verb = ''
		self.indication_adverb = ''
		self.indication_type = ''
		self.drugidplusunii = ''
		self.drugbank_file = 'No file set'

		
		## acute treatment, palliative treatment, prevention, management, adjunct, maintenance, relief of symptoms, 
		## reduce incidence and severity of
		## chronic, prophylaxis, alternate treatment for, suppressive treament
		## symptomatic treatment, immediate control of, partial replacement therapy
		## topical, induce, screening test


		for elem in drugbank_element:
			if elem.tag == '{http://www.drugbank.ca}name':
				self.drug_name = elem.text

			elif elem.tag == '{http://www.drugbank.ca}description':
				if elem.text != None:
					self.description = elem.text
					
			elif elem.tag == '{http://www.drugbank.ca}unii':
				if elem.text != None:
					self.unii = elem.text
					
					self.drugidplusunii = './DrugbankFiles/__' + self.drugbank_id + '_' + self.unii + '.html'
					self.drugbank_file = open(self.drugidplusunii,'w')
					self.drugbank_file.write ('<html><head></head><body>\n\n')
					self.drugbank_file.write ('<h1>DRUG NAME: ' + self.drug_name + '</h1>\n')
					self.drugbank_file.write ('<h2>UNII : ' + self.unii + '</h2>\n')
					self.drugbank_file.write ('<h2>Description</h2>\n')
					self.drugbank_file.write ('<p>' + self.description + '\n')				

		for elem in drugbank_element:

			if elem.tag == '{http://www.drugbank.ca}name':
				self.drug_name = elem.text

			elif elem.tag == '{http://www.drugbank.ca}drugbank-id':
				self.drugbank_id = elem.text

			elif elem.tag == '{http://www.drugbank.ca}description':
				if elem.text != None:
					self.description = elem.text
					
			elif elem.tag == '{http://www.drugbank.ca}unii':
				if elem.text != None:
					self.unii = elem.text

			elif elem.tag == '{http://www.drugbank.ca}indication':
				if elem.text != None:
					self.indication = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>INDICATION </h2>\n')
						self.drugbank_file.write ('<p>' + self.indication + '\n')

			elif elem.tag == '{http://www.drugbank.ca}pharmacodynamics':
				if elem.text !=None:
					self.pharmacodynamics = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>PHARMACODYNAMICS</h2>\n')
						self.drugbank_file.write ('<p>' + self.pharmacodynamics + '\n')
			elif elem.tag == '{http://www.drugbank.ca}mechanism-of-action':
				if elem.text !=None:
					self.mechanism_of_action = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Mechanism of Action</h2>\n')
						self.drugbank_file.write('<p>' + self.mechanism_of_action + '\n')
			elif elem.tag == '{http://www.drugbank.ca}toxicity':
				if elem.text !=None:
					self.toxicity = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Toxicity</h2>\n')
						self.drugbank_file.write(self.toxicity + '\n')
			elif elem.tag == '{http://www.drugbank.ca}absorption':
				if elem.text !=None:
					self.absorption = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Absorption</h2>')
						self.drugbank_file.write('<p>' + self.absorption + '\n')
			elif elem.tag == '{http://www.drugbank.ca}half-life':
				if elem.text !=None:
					self.half_life= elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Half-Life</h2>')
						self.drugbank_file.write('<p>' + self.half_life)
			elif elem.tag == '{http://www.drugbank.ca}route-of-elimination':
				if elem.text !=None:
					self.route_of_elimination= elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Route of Elimination</h2>')
						self.drugbank_file.write('<p>' +  self.route_of_elimination)
			elif elem.tag == '{http://www.drugbank.ca}clearance':
				if elem.text !=None:
					self.clearance = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Clearance</h2>')
						self.drugbank_file.write('<p>' + self.clearance)
			elif elem.tag == '{http://www.drugbank.ca}state':
				if elem.text !=None:
					self.state = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>State</h2>')
						self.drugbank_file.write('<p>' + self.state)

			elif elem.tag == '{http://www.drugbank.ca}metabolism':
				if elem.text !=None:
					self.metabolism = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Metabolism</h2>')
						self.drugbank_file.write('<p>' + self.metabolism)

			elif elem.tag == '{http://www.drugbank.ca}volume-of-distribution':
				if elem.text != None:
					self.volume_of_distribution = elem.text
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>Volume of Distribution</h2>')
						self.drugbank_file.write('<p>' + self.volume_of_distribution)
			elif elem.tag == '{http://www.drugbank.ca}categories':
				cats = list(elem)
				obj_type = type(cats)
					
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write('<h2>CATEGORIES</h2>\n')
					self.drugbank_file.write('<UL>\n')
				for cat in cats:
					if cat.tag == '{http://www.drugbank.ca}category':
						subcats = list(cat)
						cat_tag = ''
						mesh_id = ''
						for sub in subcats:
							if sub.text != None:
								if sub.tag == '{http://www.drugbank.ca}category':
									cat_tag = sub.text
								elif sub.tag == '{http://www.drugbank.ca}mesh-id':
									mesh_id = sub.text
						
						if self.drugbank_file != 'No file set':
							self.drugbank_file.write ('<li>' + cat_tag + ', Mesh ID: ' + mesh_id)
									
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write('</UL>')
			elif elem.tag == '{http://www.drugbank.ca}products':
				products = list(elem)
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write('<h2>PRODUCTS</h2>\n')

				for product in products:
					if product.tag == '{http://www.drugbank.ca}product':

						prod_items = product.getchildren()
						drug_name = ''
						labeller = ''
						ndc_id = ''
						ndc_product_code = ''
						dpd_id = ''
						start_mktg = ''
						end_mktg = ''
						dose_form = ''
						strength = ''
						route = ''
						fda_app_num = ''
						generic = ''
						otc = ''
						approved = ''
						country = ''
						source = ''

						for prod_detail in prod_items:
							if prod_detail.tag == '{http://www.drugbank.ca}name':
								drug_name = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}labeller':
								labeller= prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}ndc-id':
								ndc_id= prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}ndc-product-code':
								ndc_product_code= prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}started-marketing-on':
								start_mktg = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}ended-marketing-on':
								end_mktg = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}dosage-form':
								dose_form = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}strength':
								strength = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}route':
								route = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}fda-application-number':
								fda_app_num = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}generic':
								generic = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}over-the-counter':
								otc = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}approved':
								approved = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}country':
								country = prod_detail.text
							elif prod_detail.tag == '{http://www.drugbank.ca}source':
								source = prod_detail.text

							##if drug_name != None and labeller != None and dose_form != None and strength != None and route != None and otc != None:
							##	print ('PRODUCT: ' + drug_name + ', ' + labeller + ', ' + dose_form + ', ' + strength + ', ' + route + ', ' + otc)

							new_product = DrugBankProduct(drug_name, labeller, ndc_id, ndc_product_code)
							self.products.append(new_product)

			elif elem.tag ==  '{http://www.drugbank.ca}atc-codes':
				atc_codes = list(elem)
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write ('<h2>ATC CODES </h2>\n')
					self.drugbank_file.write ('<ul>\n')

				for atc_code in atc_codes:
					levels = list(atc_code)
					for level in levels:
						if self.drugbank_file != 'No file set':
							self.drugbank_file.write ('<li>' + level.text + '\n')

				if self.drugbank_file != 'No file set':
					self.drugbank_file.write ('</ul>\n')

			elif elem.tag == '{http://www.drugbank.ca}general-references':
				articles = list(elem)

				if self.drugbank_file != 'No file set':
					self.drugbank_file.write ('<h2>REFERENCES</h2>\n')
					self.drugbank_file.write ('<ul>\n')
				

				for article in articles:
					##print (article.tag + ' [TAG] -- Number of articles: ' + str(len(article)))

					if article.tag == '{http://www.drugbank.ca}articles' and len(article) > 0:
						references = list(article)
						for ref in references:
							if ref.tag == '{http://www.drugbank.ca}article':
								citations = list(ref)
								pubid = ''
								citationid = ''
								for cite in citations:									
									if cite.tag ==  '{http://www.drugbank.ca}pubmed-id':
										pubid =  cite.text
									elif cite.tag == '{http://www.drugbank.ca}citation':
										citationid = cite.text

								if pubid != None and citationid != None and self.drugbank_file != 'No file set':
										self.drugbank_file.write ('<li>Pub ID: ' + pubid + ' (' +citationid+') \n')
							
							##elif ref.tag == '{http://www.drugbank.ca}textbooks':
							##	print('Textbook')
							##elif ref.tag == '{http://www.drugbank.ca}links':
							##	print('Links')
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write('</ul>')

			elif elem.tag == '{http://www.drugbank.ca}dosages':
				dosage = list(elem)
				obj_type = type(dosage)
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write ('<h2>DOSAGES</h2>\n')
					self.drugbank_file.write ('<ul>\n')
				for dose_item in dosage:
					
					form = ''
					route = ''
					strength = ''
					
					if dose_item.tag == '{http://www.drugbank.ca}dosage':
						dose_detail = list(dose_item)
						for dose_info in dose_detail:
							
							if dose_info.tag == '{http://www.drugbank.ca}form':
								if dose_info.text != None:
									form = dose_info.text
							elif dose_info.tag == '{http://www.drugbank.ca}route':
								if dose_info.text != None:
									route = dose_info.text
							elif dose_info.tag == '{http://www.drugbank.ca}strength':
								if dose_info.text != None:
									strength = dose_info.text

						if self.drugbank_file != 'No file set':
							self.drugbank_file.write ('<li>' + form + '(' + route + ')' + '-->' + strength + '\n')

						dose_obj = DrugBankDosage(form,route,strength)
						self.dosages_arr.append(dose_obj)
					
				if self.drugbank_file != 'No file set':
					self.drugbank_file.write('</ul>\n')

			elif elem.tag == '{http://www.drugbank.ca}drug-interactions':
				if elem.text != None:
					items = list(elem)
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>DRUG INTERACTIONS</h2>\n')

					for item in items:
						interactions = list(item)
						interaction_id = ''
						interaction_name = ''
						interaction_description = ''

						for interaction in interactions:
							if interaction.tag == '{http://www.drugbank.ca}drugbank-id':
								interaction_id = interaction.text
							elif interaction.tag == '{http://www.drugbank.ca}name':
								interaction_name = interaction.text
							elif interaction.tag == '{http://www.drugbank.ca}description':
								interaction_description = interaction.text
							
						if self.drugbank_file != 'No file set':
							self.drugbank_file.write ('<p>' + interaction_id + ', ' + interaction_name + ', ' + interaction_description +'\n') 
						##drug_interaction = DrugBankInteraction(interaction_id, interaction_name, interaction_description)
						##self.drug_interactions.append(drug_interaction)

			elif elem.tag == '{http://www.drugbank.ca}food-interactions':
				if elem.text !=None:
					items = list(elem)					
					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>FOOD INTERACTIONS </h2>\n')

					for item in items:
						if item.tag == '{http://www.drugbank.ca}food-interaction':
							self.drugbank_file.write ('<p>' + item.text + '\n')
							##self.food_interactions.append(item.text)
							##self.parse_food_interaction(item.text)

			

			elif elem.tag == '{http://www.drugbank.ca}snp-adverse-drug-reactions':
				if elem.text !=  None:
					items = list(elem)

					if self.drugbank_file != 'No file set':
						self.drugbank_file.write ('<h2>ADVERSE REACTIONS </h2>\n')

					for item in items:
						if item.tag == '{http://www.drugbank.ca}reaction':
							reaction_details = list(item)
							
							r_protein = ''
							r_gene = ''
							r_uniprot = ''
							r_rsid = ''
							r_allele = ''
							r_adverse = ''
							r_description = ''
							r_pubmedid = ''

							for reaction in reaction_details:
								if reaction.tag == '{http://www.drugbank.ca}protein-name':
									if reaction.text != None:
										r_protein = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}gene-symbol':
									if reaction.text != None:
										r_gene = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}uniprot-id':
									if reaction.text != None:
										r_uniprot = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}rs-id':
									if reaction.text != None:
										r_rsid = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}allele':
									if reaction.text != None:
										r_allele = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}adverse-reaction':
									if reaction.text != None:
										r_adverse = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}description':
									if reaction.text != None:
										r_description = reaction.text

								elif reaction.tag == '{http://www.drugbank.ca}pubmed-id':
									if reaction.text != None:
										r_pubmedid = reaction.text

							adverse_react = DrugBankAdverse(r_protein, r_gene, r_uniprot, r_rsid, r_allele, r_adverse, r_description, r_pubmedid)
							self.drugbank_file.write ('<p>' + r_adverse + ', ' + r_description + '\n')
							print (r_adverse + ', ' + r_description + '\n')

							self.adverse_reactions.append(adverse_react)
						else: 
							print ('########No adverse' + item.tag + ' ' + item.text)
			


			elif elem.tag ==  '{http://www.drugbank.ca}snp-effects':
				if elem.text != None:
					self.snp_effects = elem

			elif elem.tag ==  '{http://www.drugbank.ca}enzymes':
				if elem.text != None:
					self.enzymes = elem

			elif elem.tag ==  '{http://www.drugbank.ca}protein-binding':
				if elem.text != None:
					self.protein_binding = elem

			elif elem.tag ==  '{http://www.drugbank.ca}carriers':
				if elem.text != None:
					self.carriers = elem

			elif elem.tag ==  '{http://www.drugbank.ca}targets':
				if elem.text != None:
					self.targets  = elem

			elif elem.tag ==  '{http://www.drugbank.ca}reactions':
				if elem.text != None:
					self.reactions  = elem

			elif elem.tag ==  '{http://www.drugbank.ca}patents':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}cas-number':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}pathways':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}classification':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}ahfs-codes':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}msds':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}calculated-properties':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}mixtures':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}salts':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}synonyms':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}external-identifiers':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}external-links':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}packagers':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}groups':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}pdb-entries':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}transporters':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}average-mass':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}monoisotopic-mass':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}synthesis-reference':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}manufacturers':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}fda-label':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}prices':
				if elem.text != None:
					self.patents = elem
			elif elem.tag ==  '{http://www.drugbank.ca}experimental-properties':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}affected-organisms':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}international-brands':
				if elem.text != None:
					self.patents = elem

			elif elem.tag ==  '{http://www.drugbank.ca}sequences':
				if elem.text != None:
					self.patents = elem
			else:
				print ('Tag no match: ' + elem.tag)
		if self.drugbank_file != 'No file set':
			self.drugbank_file.close()


	def write_drugbank_info(file_to_write, field_type, field_text):
		file_to_write.write(field_text)

	def parse_food_interaction(self, interaction):
		print (interaction)

		## Interaction types:
		## Verb: avoid, take 
		self.food_i1 = re.compile(r'(Take) ([A-Za-z]+) (food)')
		self.food_i2 = re.compile(r'(Avoid) (alcohol)')

		if self.food_i1.match(interaction):
			results = self.food_i1.match(interaction)
			if results != None:
				match_groups = results.groups()
				print ('[v]' + results.group(1) + '[a]' + results.group(2) + '[n]' + results.group(3))

		if self.food_i2.match(interaction):
			results = self.food_i2.match(interaction)
			if results != None:
				match_groups = results.groups()
				print('[v]' + results.group(1) + '[n]' + results.group(2))


	def parse_indication(self, indication):
		self.indication_r1 = re.compile(r'([A-Za-z0-9]+) (treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r6 = re.compile(r'([A-Za-z0-9\,\s\-\(\)]+) (is indicated for the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r18 = re.compile(r'([A-Za-z0-9\s\-\(\)]+) (used in the treatment of) ([A-Za-z0-9\s\-\(\)]+)')
		self.indication_r18_1 = re.compile(r'([A-Za-z0-9\s\-\(\)]+) (used for the treatment of) ([A-Za-z0-9\s\-\(\)]+)')
		self.indication_r17 = re.compile(r'([A-Za-z0-9\s\-\(\)]+) (is used as) ([A-Za-z0-9\s\-\(\)]+)')
		self.indication_r29 = re.compile(r'(For use in the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r19 = re.compile(r'(Used in the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r10 = re.compile(r'(Intended for the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r9 = re.compile(r'(For the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r8 = re.compile(r'(Treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r37 = re.compile(r'(Treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r36 = re.compile(r'(Used for the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r38 = re.compile(r'(For the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r40 = re.compile(r'(Indicated in the treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')


		self.indication_r22 = re.compile(r'(For use as a adjunct in) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r25 = re.compile(r'(For use as an adjunct to) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r32 = re.compile(r'(For use as adjunctive therapy to) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r41 = re.compile(r'(Used as adjunctive therapy in the) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r20 = re.compile(r'(Used to) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r21 = re.compile(r'(Used for) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r4 = re.compile(r'(To be used as) ([A-Za-z0-9\,\s\-\(\)]+)') 

		self.indication_r2 = re.compile(r'(Used to treat) ([A-Za-z0-9\,\s\-\(\)]+)') 		
		self.indication_investigated = re.compile(r'(Investigated for use\/treatment in) ([A-Za-z0-9\,\s\-\(\)]+)')

		
		self.indication_r3 = re.compile(r'(For management of) ([A-Za-z0-9\,\s\-\(\)]+)') 
		self.indication_r3_1 = re.compile(r'(For the management of) ([A-Za-z0-9\,\s\-\(\)]+)') 
		self.indication_r42 = re.compile(r'(For the management of the signs and symptoms of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r11 = re.compile(r'(For the treatment and prevention of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r12 = re.compile(r'(For use in treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r13 = re.compile(r'(For use as a) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r7 = re.compile(r'(Investigated for use/treatment in) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r14 = re.compile(r'(Intended for use as a) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r5 = re.compile(r'(For the relief of) ([A-Za-z0-9\,\s\-\(\)]+)') 

		self.indication_r44 = re.compile(r'(For the treatment or relief of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r15 = re.compile(r'(For the treatment and management of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r16 = re.compile(r'(For the treatment and prevention of) ([A-Za-z0-9\,\s\-\(\)]+)')


		self.indication_r31 = re.compile(r'(For symptomatic treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r33 = re.compile(r'(For the short-term treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r28 = re.compile(r'(For maintenance treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r34 = re.compile(r'(For palliative treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r35 = re.compile(r'(For the palliative treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r24 = re.compile(r'(For the acute treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r47 = re.compile(r'(For the prevention and treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r48 = re.compile(r'(For the acute and chronic treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r49 = re.compile(r'(For the control of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r50 = re.compile(r'(For treatment and management of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r51 = re.compile(r'(For the topical treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r45 = re.compile(r'(For prevention of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r52 = re.compile(r'(For the reduction of symptoms of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r26 = re.compile(r'(Used to prevent or reduce the severity of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r23 = re.compile(r'(For the prevention of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r43 = re.compile(r'(Investigated for use/treatment in) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r46 = re.compile(r'(Used primarily to treat) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r53 = re.compile(r'(May be used to treat) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r55 = re.compile(r'(For the reduction of) ([A-Za-z0-9\,\s\-\(\)]+)')

		self.indication_r54 = re.compile(r'(For relief of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_r27 = re.compile(r'(For the relief and treatment of) ([A-Za-z0-9\,\s\-\(\)]+)')
		self.indication_regex_mult = re.compile(r'([A-Za-z0-9\s\-\(\)]+) (and) ([A-Za-z0-9\s\-\(\)]+)')

		## For palliative management of 
		##  For the acute and maintenance treatment of 
		##  For the initial treatment of
		##  For the short-term treatment (up to 8 weeks) of
		##  Indicated for the treatment of


		if self.indication_r1.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r1.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(3)
				self.indication_adverb = results.group(2)

		elif self.indication_r2.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r3.match(indication):
			self.parse ='true'
			indication_type = 'MANAGEMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r3_1.match(indication):
			self.parse = 'true'
			indication_type = 'MANAGEMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r4.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)
		elif self.indication_r5.match(indication):
			self.parse = 'true'

		elif self.indication_r6.match(indication):
			self.parse ='true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r6.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(3)
				self.indication_adverb = results.group(2)

		elif self.indication_r7.match(indication):
			self.parse = 'true'
			self.indication_type = 'INVESTIGATED'

		elif self.indication_r8.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r8.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r9.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r9.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)
		elif self.indication_r10.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r10.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)


		elif self.indication_r11.match(indication):
			self.parse = 'true'
			indication_type = 'TREATMENT AND PREVENTION'

		elif self.indication_r12.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'

		elif self.indication_r13.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'

		elif self.indication_r14.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'

		elif self.indication_r15.match(indication):
			self.parse = 'true'

		elif self.indication_r16.match(indication):
			self.parse = 'true'

		elif self.indication_r17.match(indication):
			self.parse = 'true'

		elif self.indication_r18.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r18.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(3)
				self.indication_adverb = results.group(2)

		elif self.indication_r18_1.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r18_1.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(3)
				self.indication_adverb = results.group(2)

		elif self.indication_r19.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'

		elif self.indication_r20.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r21.match(indication):
			self.parse = 'true'
			results = self.indication_r21.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r22.match(indication):
			self.parse = 'true'
			self.indication_type= 'ADJUNCT'
			results = self.indication_r22.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r23.match(indication):
			self.parse = 'true'

		elif self.indication_r24.match(indication):
			self.parse = 'true'

		elif self.indication_r25.match(indication):
			self.parse = 'true'
			self.indication_type= 'ADJUNCT'
			results = self.indication_r25.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r26.match(indication):
			self.parse = 'true'

		elif self.indication_r27.match(indication):
			self.parse = 'true'

		elif self.indication_r28.match(indication):
			self.parse = 'true'

		elif self.indication_r29.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r29.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r31.match(indication):
			self.parse = 'true'

		elif self.indication_r32.match(indication):
			self.parse = 'true'
			self.indication_type= 'ADJUNCT'
			results = self.indication_r32.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r33.match(indication):
			self.parse = 'true'

		elif self.indication_r34.match(indication):
			self.parse = 'true'
			self.indication_type = 'PALLIATIVE'

		elif self.indication_r35.match(indication):
			self.parse = 'true'
			self.indication_type = 'PALLIATIVE'

		elif self.indication_r36.match(indication):
			self.parse = 'true'
			results = self.indication_r21.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r37.match(indication):
			self.parse = 'true'
			self.indication_type= 'TREATMENT'
			results = self.indication_r37.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r38.match(indication):
			self.parse = 'true'
			self.indication_type = 'TREATMENT'
			results = self.indication_r38.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)
	

		elif self.indication_r40.match(indication):
			self.parse = 'true'
			self.indication_type = 'TREATMENT'
			results = self.indication_r40.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r41.match(indication):
			self.parse = 'true'
			self.indication_type= 'ADJUNCT'
			results = self.indication_r41.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r42.match(indication):
			self.parse = 'true'
			self.indication_type = 'MANAGEMENT'
			results = self.indication_r2.match(indication)
			if results != None:
				match_groups = results.groups()
				self.indication_noun = results.group(2)
				self.indication_adverb = results.group(1)

		elif self.indication_r43.match(indication):
			self.parse = 'true'

		elif self.indication_r44.match(indication):
			self.parse = 'true'

		elif self.indication_r45.match(indication):
			self.parse = 'true'

		elif self.indication_r46.match(indication):
			self.parse = 'true'	

		elif self.indication_r47.match(indication):
			self.parse = 'true'	
		elif self.indication_r48.match(indication):
			self.parse = 'true'	

		elif self.indication_r49.match(indication):
			self.parse = 'true'

		elif self.indication_r50.match(indication):
			self.parse = 'true'

		elif self.indication_r51.match(indication):
			self.parse = 'true'
		elif self.indication_r52.match(indication):
			self.parse = 'true'	
		elif self.indication_r53.match(indication):
			self.parse = 'true'	
		elif self.indication_r54.match(indication):
			self.parse = 'true'
		elif self.indication_r55.match(indication):
			self.parse = 'true'	
		elif self.indication_investigated.match(indication):
			self.parse = 'true'					

		##elif self.parse == 'false': 
		##	print ('--> ' + indication)

	def lookup_icon_by_term(self, term):

		if term == 'anticoagulant':
			return '<img src=\"./MedImages/blood-vessel-128x128@3x.png\" height=30 width=30>'
		elif term == 'QTc-prolonging':
			return '<img src=\"./MedImages/QT@3x.png\" height=30 width=30>'
		elif term == 'hypotensive':
			return '<img src=\"./MedImages/heart-failure@3x.png\" height=30 width=30>'
		elif term == 'CNS depressant':
			return '.<img src=\"./MedImages/blue-brain-128x128@3x.png\" height=30 width=30>'
		elif term == 'cardiotoxic':
			return '<img src=\"./MedImages/contraindicated-yellow@3x.png\" height=30 width=30>'
		elif term == 'hypoglycemic':
			return '<img src=\"./MedImages/diabetic-icon-128x128@3x.png\" height=30 width=30>'
		elif term == 'adverse efffects':
			return '<img src=\"./MedImages/contraindicated-icon@3x.png\" height=30 width=30>'
		else:
			return None

	def write_ddi(self,type_data,filename,reaction_kind):
		inc_source = []
		dec_source = []
		inc_dest = []
		dec_dest = []

		reaction_icon = ''
		effect_html = ''
		if reaction_kind == 'Metabolism':
			reaction_icon = '<i class=\"fas fa-recycle\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Serum':
			reaction_icon = '<i class=\"fas fa-expand-arrows-alt\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Absorption':
			reaction_icon = '<i class=\"fas fa-sync\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Excretion':
			reaction_icon = '<i class=\"fas fa-sign-out-alt\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Therapeutic':
			reaction_icon = '<i class=\"fas fa-plus-square\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Serum':
			reaction_icon = '<i class=\"fas fa-eye-dropper\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'RiskSeverity':
			reaction_icon = '<i class=\"fas fa-exclamation-triangle\" style=\"font-size:30px;color:black\"></i>'
		elif reaction_kind == 'Activity':
			reaction_icon = '<i class=\"fas fa-external-link-alt\" style=\"font-size:30px;color:black\"></i>'
		
		filename.write('<H2>' + reaction_kind + '</H2>')


		for effect in type_data:
			if effect.inc_dec == 'increased' or effect.inc_dec == 'increase': 

				if effect.direction == 'source_drug':

					inc_source.append(effect)

				elif effect.direction == 'dest_drug':

					inc_dest.append(effect)

			elif effect.inc_dec == 'decreased' or effect.inc_dec == 'decrease':

				if effect.direction == 'source_drug': 

					dec_source.append(effect)

				elif effect.direction == 'dest_drug': 

					dec_dest.append(effect)

		if len(inc_source) > 0:

			if reaction_kind == 'RiskSeverity' or reaction_kind == 'Activity':
				icon = self.lookup_icon_by_term(effect.effect)
				if icon != None:
					effect_html = icon + '<i>' + effect.effect + '</i>\n'
				else: 
					effect_html = '<i>' + effect.effect + '</i>\n'

			filename.write('\n<H3>\n' + reaction_icon + '<i class=\"fas fa-arrow-alt-circle-up\" style=\"font-size:30px;color:green;\"></i>' + self.drug_name + '<i class=\"fas fa-long-arrow-alt-right\" style=\"font-size:30px;color:blue;\"></i>' + effect_html +'</h3>\n')
			
			for effect in inc_source:
				filename.write(effect.precipitant + ', ')

		if len(dec_source) > 0:

			if reaction_kind == 'RiskSeverity' or reaction_kind == 'Activity':
				icon = self.lookup_icon_by_term(effect.effect)
				if icon != None:
					effect_html = icon + '<i>' + effect.effect + '</i>\n'
				else: 
					effect_html = '<i>' + effect.effect + '</i>\n'

			filename.write('\n<H3>\n' + reaction_icon + '<i class=\"fas fa-arrow-alt-circle-up\" style=\"font-size:30px;color:green;\"></i>' + self.drug_name + '<i class=\"fas fa-long-arrow-alt-right\" style=\"font-size:30px;color:blue;\"></i>' + effect_html +'</h3>\n')
			
			for effect in dec_source:
				filename.write(effect.precipitant + ', ')

		if len(inc_dest) > 0:

			if reaction_kind == 'RiskSeverity' or reaction_kind == 'Activity':
				icon = self.lookup_icon_by_term(effect.effect)
				if icon != None:
					effect_html = icon + '<i>' + effect.effect + '</i>\n'
				else: 
					effect_html = '<i>' + effect.effect + '</i>\n'

			filename.write('\n<H3>\n' + reaction_icon + '<i class=\"fas fa-arrow-alt-circle-up\" style=\"font-size:30px;color:green;\"></i>' + self.drug_name + '<i class=\"fas fa-long-arrow-alt-left\" style=\"font-size:30px;color:silver;\"></i>' + effect_html +'</h3>\n')
			
			for effect in inc_dest:
				filename.write(effect.precipitant + ', ')

		if len(dec_dest) > 0:

			if reaction_kind == 'RiskSeverity' or reaction_kind == 'Activity':
				icon = self.lookup_icon_by_term(effect.effect)
				if icon != None:
					effect_html = icon + '<i>' + effect.effect + '</i>\n'
				else: 
					effect_html = '<i>' + effect.effect + '</i>\n'

			filename.write('\n<H3>\n' + reaction_icon + '<i class=\"fas fa-arrow-alt-circle-up\" style=\"font-size:30px;color:green;\"></i>' + self.drug_name + '<i class=\"fas fa-long-arrow-alt-right\" style=\"font-size:30px;color:silver;\"></i>' + effect_html +'</h3>\n')

			for effect in dec_dest:
				filename.write(effect.precipitant + ', ')

	def write_drug_bank_file(self,filename):

		filename.write('<BR><BR>')

		filename.write('<H1 id=\"drugName\">' + self.drug_name + '</H1>\n')

		filename.write('\n<H2 id=\"drugDescription\">Description</H2>\n')
		filename.write('<P>' + self.description + '\n')

		filename.write('\n<H2>Indications</H2>\n')
		if self.indication_type != '' and self.indication_noun != '' and self.indication_adverb != '':
			filename.write('<P>' + self.indication_type + ' --> ' + self.indication_noun)
		else: 
			filename.write('<P>' + self.indication + '\n')

		filename.write('\n<H2>Pharmacodynamics</H2>\n')
		filename.write(self.pharmacodynamics)

		if self.mechanism_of_action != '':
			filename.write('\n<H2>Mechanism of Action</H2>\n')
			drugbank_file.write(self.mechanism_of_action)
		if self.toxicity != '':
			filename.write('\n<H2>Toxicity</H2>\n')
			drugbank_file.write(self.toxicity)
		
		if self.absorption != '':
			filename.write('\n<H2>Absorption</H2>\n')
			drugbank_file.write(self.absorption)

		if self.half_life != '':
			filename.write('\n<H2>Half-Life</H2>\n')
			drugbank_file.write(self.half_life)

		if self.route_of_elimination != '':
			filename.write('\n<H2>Route of Elimination</H2>\n')
			drugbank_file.write(self.route_of_elimination)

		if self.metabolism != '':
			filename.write('\n<H2>Metabolism</H2>\n')
			drugbank_file.write(self.metabolism)


		if len(self.atc_codes) > 0:
			drugbank_file.write('\n<H2>ATC Codes</H2>\n')
			for atc_code in atc_codes:
				filename.write('\n<p>' + atc_code)

		if len(self.dosages_arr) > 0:
			filename.write('\n<H2>Dosages</H2>')
			filename.write('<table>\n<thead>\n<tr>\n<td>Form</td><td>Route</td><td>Strength</td>\n</tr>\n</thead>\n<tbody>\n')
			for dosage in self.dosages_arr:
				filename.write('<tr>\n')
				filename.write('\t<td>' + dosage.form + '</td><td>'+dosage.route+ '</td><td>' + dosage.strength +'</td>\n')
				filename.write('</tr>\n')

			filename.write('</tbody>\n</table>')
		

		filename.write('\n<h3>Drug Interactions</h3>\n')

		if len(self.metab) > 0:
			self.write_ddi(self.metab,filename,'Metabolism')
		if len(self.serum) > 0:
			self.write_ddi(self.serum,filename,'Serum')
		if len(self.thera) > 0 :
			self.write_ddi(self.thera,filename,'Therapeutic')
		if len(self.excretion) > 0:
			self.write_ddi(self.excretion,filename,'Excretion')
		if len(self.absorption_arr) > 0:
			self.write_ddi(self.absorption,filename,'Absorption')
		if len(self.risk_severity) > 0:
			self.write_ddi(self.risk_severity,filename,'RiskSeverity')
		if len(self.activity_inc_dec) > 0:
			self.write_ddi(self.activity_inc_dec,filename,'Activity')

		if len(self.other_ddi_array) > 0:
			drugbank_file.write('\n<H3>Other</h3>\n')
	
			for other_effect in self.other_ddi_array:
				drugbank_file.write('<p>'+ other_effect.text_parse + '\n')

		if len(self.food_interactions) > 0:
			drugbank_file.write('\n\n<h3 id=\"foodInteractions\">Food Interactions</h3>\n')
			for food_interaction in self.food_interactions:
				drugbank_file.write('\n<p>' + food_interaction + ', ')
		
		if len(self.adverse_reactions) > 0:
			drugbank_file.write('\n\n<h3>Adverse Reactions</h3>\n')
			for adverse_obj in self.adverse_reactions:
				drugbank_file.write('<P>' +adverse_obj.r_gene + '\n')
				drugbank_file.write('<p>' +adverse_obj.r_allele + '\n')
				drugbank_file.write('<P>' +adverse_obj.r_adverse + '\n')
				drugbank_file.write('<p> ' +adverse_obj.r_description + '\n')
		
		if len(self.atc_codes) > 0:
			drugbank_file.write('\n<h3>ATC Codes</h3>\n')
			for atc_code in atc_codes:
				drugbank_write('<P>' + atc_code + '\n')

	def symbol(self, symbol):

		inc_dec_symbolize = ''

		if symbol == 'increase':
			inc_dec_symbolize = ' ^^ '
		elif symbol == 'decrease':
			inc_dec_symbolize = ' [--] '

		return inc_dec_symbolize

	def compare_precipitant_source_drug(self, drug_name, precipitant, regex_result):

		if precipitant == self.drug_name:
			precipitant - regex_result.group(5)

	def regexDDI(self):

		self.CNS_preprocess = re.compile(r'([A-Za-z0-9\s\-\(\)]+){1,3} (may increase the central nervous system depressant \(CNS depressant\) activities of) ([A-Za-z0-9\s\-\(\)]+){1,3}')
		
		self.Metab_re = re.compile(r'(The metabolism of) ([A-Za-z0-9\s\-\(\)]+){1,3} (can be) ([a-z]+) (when combined with) ([A-Za-z0-9\s\-\(\)]+){1,3}')
		self.Serum_re = re.compile(r'(The serum concentration of) ([A-Za-z0-9\s\-\(\)]+){1,3} (can be) ([a-z]+) (when it is combined with) ([A-Za-z0-9\s\-\(\)]+){1,3}')
		self.Thera_re = re.compile(r'(The therapeutic efficacy of) ([A-Za-z0-9\s\-\(\)]+){1,3} (can be) ([a-z]+) (when used in combination with) ([A-Za-z0-9\s\-\(\)]+){1,5}')
		self.Absorption_re = re.compile(r'([A-Za-z0-9\s\-\(\)]+){1,3} (may) ([a-z]+) (the absorption of) ([A-Za-z0-9\s\-\(\)]+){1,3}')
		self.Excretion_re = re.compile(r'([A-Za-z0-9\s\-\(\)]+){1,3} (may) ([a-z]+) (the excretion rate of) ([A-Za-z0-9\-\s]+){1,3}')
		self.Bioavailability_re = re.compile(r'(The bioavailability of) ([A-Za-z0-9\s\-\(\)]+){1,3} (can be) ([a-z]+) (when combined with) ([A-Za-z0-9\s\-\(\)]+){1,3}')

		self.Risk_Severity_re = re.compile(r'(The risk or severity of) ([A-Za-z0-9\s\-\(\)]+){1,3} (can be) ([a-z]+) (when) ([A-Za-z0-9\s\-\(\)]+){1,3} (is combined with) ([A-Za-z0-9\s\-\(\)]+){1,3}')
		self.Activity_re = re.compile(r'([A-Za-z0-9\s\-\(\)]+){1,3} (may) ([a-z]+) (the) ([A-Za-z0-9\s\-]+){1,3} (activities of) ([A-Za-z0-9\s\-\(\)]+){1,3}')	
	
		self.Effect_re = re.compile(r'([A-Za-z0-9\-]+){1,3} (may be) ([a-z]+) (when it is combined with) ([A-Za-z0-9\-\s]+){1,3}')

		for drug_Bank_interaction in self.drug_interactions:
			result = self.CNS_preprocess.match(drug_Bank_interaction.text_parse)
			if result != None:
				match_groups = result.groups()
				drug = result.group(1)
				precip = result.group(3)
				inter_descr =drug + ' may increase the CNS depressant activities of '  + precip
				drug_Bank_interaction.text_parse  =  inter_descr

			if self.Metab_re.match(drug_Bank_interaction.text_parse):
				result = self.Metab_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(2)
					inc_dec = result.group(4)
					precip = result.group(6)
					if precip == self.drug_name:
						precip = result.group(2)
						drug = result.group(6)
						drug_Bank_interaction.set_type_and_effect('METABOLISM', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('METABOLISM', inc_dec, 'No effect', precip,'dest_drug')


					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  = drug + inc_dec_symbolize + ' --> '  + precip
					self.metab.append(drug_Bank_interaction)

			elif self.Serum_re.match(drug_Bank_interaction.text_parse):
				result = self.Serum_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(2)
					inc_dec = result.group(4)
					precip = result.group(6)

					if precip == self.drug_name:
						precip = result.group(2)
						drug = result.group(6)
						drug_Bank_interaction.set_type_and_effect('SERUM', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('SERUM', inc_dec, 'No effect', precip,'dest_drug')

					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize  + ' --> '  + precip
					drug_Bank_interaction.set_type_and_effect('SERUM', inc_dec, 'No effect', precip)
					self.serum.append(drug_Bank_interaction)

			elif self.Thera_re.match(drug_Bank_interaction.text_parse):
				result = self.Thera_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(2)
					inc_dec = result.group(4)
					precip = result.group(6)
					if precip == self.drug_name:
						precip = result.group(2)
						drug = result.group(6)
						drug_Bank_interaction.set_type_and_effect('THERAPEUTIC', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('THERAPEUTIC', inc_dec, 'No effect', precip,'dest_drug')
					
					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize  + ' --> '  + precip
					drug_Bank_interaction.set_type_and_effect('THERAPEUTIC', inc_dec, 'No effect', precip)
					self.thera.append(drug_Bank_interaction)

			elif self.Absorption_re.match(drug_Bank_interaction.text_parse):
				result = self.Absorption_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(1)
					inc_dec = result.group(3)
					precip = result.group(5)

					if precip == self.drug_name:
						precip = result.group(1)
						drug = result.group(5)
						drug_Bank_interaction.set_type_and_effect('ABSORPTION', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('ABSORPTION', inc_dec, 'No effect', precip,'dest_drug')
					
					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize + effect + ' --> '  + precip
					drug_Bank_interaction.set_type_and_effect('ABSORPTION', inc_dec, 'No effect', precip)
					self.absorption_arr.append(drug_Bank_interaction)

			elif self.Excretion_re.match(drug_Bank_interaction.text_parse):
				result = self.Excretion_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(1)
					inc_dec = result.group(3)
					precip = result.group(5)

					if precip == self.drug_name:
						precip = result.group(1)
						drug = result.group(5)
						drug_Bank_interaction.set_type_and_effect('EXCRETION', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('EXCRETION', inc_dec, 'No effect', precip,'dest_drug')
				

					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize  + ' --> '  + precip
					drug_Bank_interaction.set_type_and_effect('EXCRETION', inc_dec, 'No effect', precip)
					self.excretion.append(drug_Bank_interaction)

			elif self.Bioavailability_re.match(drug_Bank_interaction.text_parse):
				result = self.Bioavailability_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					drug = result.group(1)
					inc_dec = result.group(3)
					precip = result.group(5)

					if precip == self.drug_name:
						precip = result.group(1)
						drug = result.group(5)
						drug_Bank_interaction.set_type_and_effect('BIOAVAILABILITY', inc_dec, 'No effect', precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('BIOAVAILABILITY', inc_dec, 'No effect', precip,'dest_drug')
					

					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize + ' --> '  + precip
					drug_Bank_interaction.set_type_and_effect('BIOAVAILABILITY', inc_dec, 'No effect', precip)
					self.bioavailability.append(drug_Bank_interaction)

			elif self.Risk_Severity_re.match(drug_Bank_interaction.text_parse):
				result = self.Risk_Severity_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					effect = result.group(2)
					inc_dec = result.group(4)
					drug = result.group(8)
					precip = result.group(6)

					##print ('RISK/SEVERITY --> Effect: ' + effect + ', Inc/Dec:' + inc_dec + ', Drug: ' + drug + ', Precip: ' + precip)
					if precip == self.drug_name:
						precip = result.group(8)
						drug = result.group(6)
						drug_Bank_interaction.set_type_and_effect('RISK_SEVERITY', inc_dec, effect, precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('RISK_SEVERITY', inc_dec, effect, precip,'dest_drug')

					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  effect + inc_dec_symbolize + drug  + ' --> '  + precip
					self.risk_severity.append(drug_Bank_interaction)

			elif self.Activity_re.match(drug_Bank_interaction.text_parse):
				result = self.Activity_re.match(drug_Bank_interaction.text_parse)
				if result != None:
					match_groups = result.groups()
					precip = result.group(1)
					inc_dec = result.group(3)
					effect = result.group(5)
					drug = result.group(7)
					##print ('ACTIVITY --> Effect: ' + effect + ', Inc/Dec:' + inc_dec + ', Drug: ' + drug + ', Precip: ' + precip)

					if precip == self.drug_name:
						precip = result.group(7)
						drug = result.group(1)
						drug_Bank_interaction.set_type_and_effect('ACTIVITY', inc_dec, effect, precip,'source_drug')
					else:
						drug_Bank_interaction.set_type_and_effect('ACTIVITY', inc_dec, effect, precip,'dest_drug')

					inc_dec_symbolize = self.symbol(inc_dec)
					drug_Bank_interaction.text_parse  =  drug + inc_dec_symbolize + effect + ' --> '  + precip
					self.activity_inc_dec.append(drug_Bank_interaction)
			else:
				##print ('[+++]Appending non-match: ' + drug_Bank_interaction.text_parse)
				self.other_ddi_array.append(drug_Bank_interaction)

		##print('-----------------------------------------------')
		##print ('Finished regex replace for DrugBank ID: ' + self.drugbank_id)

	def postprocessRegex(self, term_text):
		print(term_text)
		self.postProcess = re.compile(r'')

class DrugBankProduct:
	def __init__(self, name, labeller, ndc_id, ndc_product_code):
		self.drug_name = name
		self.labeller = labeller
		self.ndc_id = ndc_id
		self.ndc_product_code = ndc_product_code

class DrugBankDosage:
	def __init__(self, form, route, strength):
		self.form = form
		self.route = route
		self.strength = strength

class DrugBankAdverse:
	def __init__(self,protein,gene,uniprot,rsid,allele,adverse,description,pubmed):

		self.r_protein = 'None'
		self.r_gene = 'None'
		self.r_uniprot = 'None'
		self.r_rsid = 'None'
		self.r_allele = 'None'
		self.r_adverse = 'None'
		self.r_description = 'None'
		self.r_pubmedid = 'None'

		self.r_protein = protein
		self.r_gene = gene
		self.r_uniprot = uniprot
		self.r_rsid = rsid
		self.r_allele = allele
		self.r_adverse = adverse
		self.r_description = description
		self.r_pubmedid = pubmed

class DrugBankInteraction:

	def __init__(self, drug_id, drug_name, description):
		self.source_drug_name = drug_name
		self.source_drug_id = drug_id
		self.text_parse = description
		self.precipitant = ''
		self.effect = ''
		self.effect_type = ''
		self.direction = ''
		self.inc_dec = ''

	def set_type_and_effect(self, effect_type = 'Unknown', inc_dec = 'None', effect = 'No effect', precipitant = 'No precip', direction='source_drug'):
		self.effect_type = effect_type
		self.effect = effect
		self.precipitant = precipitant
		self.inc_dec = inc_dec
		self.direction = direction

class DrugBankFoodInteraction:
	def __init__(self, drug_id, drug_name, noun, verb, modifier):
		self.drug_id = drug_id
		self.drug_name = drug_name
		self.noun = noun
		self.verb = verb
		self.modifier = modifier