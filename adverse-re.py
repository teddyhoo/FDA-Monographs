import json
import csv
import re

from bs4 import BeautifulSoup
from spldata import ProductSummary
from spldata import DrugMonograph


drugFiles = ['drug-label-0001-of-0006.json',
'drug-label-0002-of-0006.json',
'drug-label-0002-of-0006.json',
'drug-label-0004-of-0006.json',
'drug-label-0005-of-0006.json',
'drug-label-0006-of-0006.json']




adverse_re_1 = re.compile(r'(<ADVERSE> was the most frequent complaint) ([0-9\%]+)')
adverse_re_2 = re.compile(r'(Side effects most commonly reported were [ADVERSE]+, [ADVERSE]+)')
adverse_re_3 = re.compile(r'The following have also been reported: [BODY SYSTEM]: [ADVERSE]+, [ADVERSE]+')
adverse_re_4 = re.compile(r'Most common adverse reactions in adults (\(incidence ##%\))')
adverse_re_5 = re.compile(r'Additional adverse reactions [A-Za-z\s]+ included: [ADVERSE]+, [ADVERSE]+')

## The most common reactions reported ... included
## Additional  adverse reactions that were reported with an incidence of >= 1%  included
## side effects most commonly reported
## delimiters between adverse terms  ,  and ; and "or"
split_section = re.compile(r'([0-9]+\.[0-9]+\s)')



for drugSource in drugFiles:
		with open(drugSource) as json_file:
			print ('OPEN FILE')
			data = json.load(json_file)
			for display_name in data['results']:
				drug_mono = DrugMonograph(display_name)
				drug_filename = 'adverse-test.txt'
				drug_file = open(drug_filename,'w')
				drug_file.write('-------------------------------------------------------------------------------------------')
				drug_file.write('--------------------------DRUG: ' + drug_mono.generic_name + '----------------------------\n')
				drug_file.write('-------------------------------------------------------------------------------------------')

				adverse_reactions = re.split(split_section, drug_mono.adverse_reactions)
				##if adverse_reactions != None:
					##for adverse in adverse_reactions:
						##print('------------------------------------------SECTION---------------------------------\n')
						##print (adverse)

				drug_interactions_sections = re.split(split_section, drug_mono.drug_interactions)
				if len(drug_interactions_sections) > 0:
					for drug_interactions in drug_interactions_sections:
						drug_file.write('--------INTERACTIONS SECTION----------\n')
						drug_file.write(drug_interactions)
						interaction_items = re.findall(r'(CYP[A-Z0-9]+\s)', drug_interactions)
						if interaction_items != None:
							for interaction in interaction_items:
								drug_file.write(interaction)
				drug_file.flush()
				drug_file.close()










