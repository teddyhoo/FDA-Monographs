import json
import csv
import re
from bs4 import BeautifulSoup
import lxml.html
from nltk import ngrams
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom



class  SIDER:
	def __init__(self,sider_line):
		self.cid_prim = sider_line[1]
		self.cid_sec = sider_line[2]
		self.concept_prim = sider_line[3]
		self.term_type = sider_line[4]
		self.term_name_general = sider_line[5]
		self.term_kind = sider_line[6]
		self.concept_sec = sider_line[7]
		self.term_syn = sider_line[8]

		##print ('Indication: ' + self.term_name_general)

class SEClass:
	def __init__(self,sider_line):
		self.cid_prim = sider_line[1]
		self.cid_sec = sider_line[2]
		self.concept_prim = sider_line[3]
		self.term_type = sider_line[4]
		self.concept_sec = sider_line[5]
		self.side_effect = sider_line[6]
		##print ('Side Effect: ' + self.side_effect)

class AdverseReactionReport:
	def __init__(self,adverse_dict):
		self.drug_indication = ''
		self.drug_admin = ''
		self.drug_dose_text = '' 
		self.drug = []
		self.medicinal_product = ''
		self.receivedate = ''

		adverse_keys = adverse_dict.keys()

		for key in adverse_keys:
			drug_name =''

			if key == 'receivedate':
				self.receivedate = adverse_dict[key]
				##print (self.receivedate)
			elif key == 'openfda':
				openfda_dict = adverse_dict[key]
				openfda_keys = openfda_dict.keys()
				##for key in openfda_keys:
					##if key == 'drug':
					##	drug_dict = openfda_keys[key].keys()
						##for drug_info in drug_dict:
							##print (drug_info + ': ' + drug_dict[drug_info])
			elif key == 'patient':
				patient_dict = adverse_dict[key]
				##for patient_info in patient_dict:
					##print (patient_info)
				##self.drug = patient_dict['drug'][0]
				##medicinal_product = drug['medicinalproduct']
				##if 'drugindication' in drug:
				##	self.drug_indication = drug['drugindication']
				##if 'drugadministrationroute' in drug:
				##	self.drug_admin = drug['drugadministrationroute']
				##if 'drugdosagetext' in drug:
				##	self.drug_dose_text = drug['drugdosagetext']










