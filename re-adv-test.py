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

adverse_1 = re.compile(r'(The following serious adverse reactions are):([A-Za-z\,\;\s\-\'\-]+)')
adverse_1a = re.compile(r'(The following adverse reactions are):([A-Za-z\,\;\s\-\'\-]+)')
adverse_2 = re.compile(r'(Most common adverse reactions are:)([A-Za-z\,\;\s\-\'\-]+)')
adverse_3 = re.compile(r'(Side effects most commonly reported were)([A-Za-z\,\;\s\-\'\-]+)')
adverse_4 = re.compile(r'(in more detail in other sections of the labeling:)([A-Za-z\,\;\s\-\'\-]+)')


adverse_2a = re.compile(r'(.+)(Most common adverse reactions \(incidence [\≥\>\<0-9\%]+\)\s?)([A-Za-z\,\;\s\-\'\-]+)')


text_Sample = '6 ADVERSE REACTIONS Adults: Most common adverse reactions (incidence >2%) are Headache, abdominal pain, nausea, diarrhea, vomiting, and flatulence. (6) Pediatric patients (2 to 16 years of age): Safety profile similar to that in adults, except that respiratory system events and fever were the most frequently reported reactions in pediatric studies. (8.4) To report SUSPECTED ADVERSE REACTIONS, contact Dr. Reddy’s Laboratories Inc., at 1-888-375-3784 or FDA at 1-800-FDA-1088 or www.fda.gov/medwatch. 6.1 Clinical Trials Experience with Omeprazole Monotherapy Because clinical trials are conducted under widely varying conditions, adverse reaction rates observed in the clinical trials of a drug cannot be directly compared to rates in the clinical trials of another drug and may not reflect the rates observed in practice. The safety data described below reflects exposure to omeprazole delayed-release capsules in 3096 patients from worldwide clinical trials (465 patients from US studies and 2,631 patients from international studies). Indications clinically studied in US trials included duodenal ulcer, resistant ulcer, and Zollinger-Ellison syndrome. The international clinical trials were double blind and open-label in design. The most common adverse reactions reported (i.e., with an incidence rate ≥ 2%) from omeprazole-treated patients enrolled in these studies included headache (6.9%), abdominal pain (5.2%), nausea (4%), diarrhea (3.7%), vomiting (3.2%), and flatulence (2.7%). Additional adverse reactions that were reported with an incidence ≥1% included acid regurgitation (1.9%), upper respiratory infection (1.9%), constipation (1.5%), dizziness (1.5%), rash (1.5%), asthenia (1.3%), back pain (1.1%), and cough (1.1%). The clinical trial safety profile in patients greater than 65 years of age was similar to that in patients 65 years of age or less. The clinical trial safety profile in pediatric patients who received omeprazole delayed-release capsules was similar to that in adult patients. Unique to the pediatric population, however, adverse reactions of the respiratory system were most frequently reported in the 2 to 16 year age group (18.5%). Similarly, accidental injuries were reported frequently in the 2 to 16 year age group (3.8%). [See Use in Specific Populations (8.4) ] 6.2 '

results = adverse_2a.match(text_Sample)
if results != None:
	match_groups = results.groups()
	print (str(len(match_groups)))
	print (results.groups(1))