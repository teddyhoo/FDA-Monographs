import json
import csv
import re
from bs4 import BeautifulSoup
import lxml.html
from nltk import ngrams
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import xml.dom.minidom


class NDFElement:

	def __init__(self,name, code, id, level, kind,item_properties,role_properties,concept_properties):

		self.determine_kind(kind)

		self.name = name
		self.code = code
		self.id = id
		self.level = level
		self.rxcui = 'None'
		self.rx_name = 'None'
		self.mesh_name = 'None'
		self.mesh_cui = 'None'
		self.mesh_defintion = 'None'
		self.treat_mesh_def = 'None'
		self.physiological_mesh_def = 'None'
		self.mdef = 'None'
		self.category = ''

		self.UMLS = 'None'
		self.fda_unii = 'None'

		self.properties = {}
		self.properties = item_properties
		self.role_properties = {}
		self.role_properties = role_properties
		self.concept_properties = {}
		self.concept_properties = concept_properties
		self.med_properties = {}
		self.roles = {}
		self.concepts = {}

		
	def determine_kind(self,kind):
		if kind == 'C8':
			self.kind = 'DRUG'
		elif kind == 'C18':
			self.kind = 'DOSE'
		elif kind == 'C6':
			self.kind = 'PHYSIOLOGICAL_EFFECT'
		elif kind == 'C10':
			self.kind = 'INGREDIENT'
		elif kind == 'C12':
			self.kind = 'MECHANISM_OF_ACTION'
		elif kind == 'C14':
			self.kind = 'PHARMACOKINETICS'
		elif kind == 'C16':
			self.kind = 'DISEASE'
		elif kind == 'K20':
			self.kind = 'THERAPEUTIC'
		else:
			self.kind = kind

	def add_roles_concepts(self,role_dict='None',concept_dict='None'):

		role_keys = role_dict.keys()
		concept_keys = concept_dict.keys()

		for prop in self.properties:
			if prop == 'MeSH_Definition':
				self.mdef = self.properties[prop]
			elif prop == 'Level':
				self.level = self.properties[prop]
			elif prop == 'RxNorm_CUI':
				self.rxcui = self.properties[prop]

		if len(role_keys) > 0:
			for key in role_keys:
				self.roles[key] = role_dict[key]
				if key == 'RxNorm_CUI':
					self.rxcui = role_dict[key]
				elif key == 'Level':
					self.level = role_dict[key]
				elif key == 'MeSH_Definition' or key == 'C142':
					self.mdef = role_dict[key]

		if len(concept_keys) > 0:
			for key in concept_keys:
				self.concepts[key] = concept_dict[key]

class ADReCS:
	def __init__(self, drug_id, drug_name, drug_description,drug_atc, drug_synonyms, drug_indications, drug_cas):
		self.drug_id = drug_id
		self.drug_name = drug_name
		self.drug_description = drug_description
		self.drug_atc = drug_atc
		self.drug_synonyms = drug_synonyms
		self.drug_indications = drug_indications
		self.drug_cas = drug_cas
		self.adrs = []

	def addADR(self,adr_term,adr_id,adr_frequency):
		adr_item = ADR(adr_term,adr_id,frequency)
		adrs.append(adr_item)


class SNOMED:
	def __init__(self,concept_id, module_id, ref_comp_id, sct_name,  icd_name):
		self.conceptID = concept_id
		self.moduleID = module_id
		self.refCompId = ref_comp_id
		self.sctName = sct_name
		self.icdName = icd_name
class SNOMED_MAP:
	def __init__(self,concept_id, module_id, ref_comp_id, refComponent):
		self.conceptID_map = concept_id
		self.moduleID_map = module_id
		self.refsetID = ref_comp_id
		self.refComponentID = refComponent
class RXNNORM:
	def __init__(self,concept):
		self.rxn_cui = concept[0]
		self.rxn_aui = concept[7]
		self.drug_name = concept[14]
class RXNREL:
	def __init__(self,concept):
		self.rxn_cui_1 = concept[0]
		self.rxn_atom_1 = concept[1]
		self.rxn_cui_2 = concept[4]
		self.rxn_atom_2 = concept[5]
		self.relation_type = concept[6]
		self.relation_text = concept[7]



