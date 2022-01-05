
import urllib.request
import bs4	
from requests_html import HTMLSession
from bs4 import BeautifulSoup, NavigableString
import requests
import time
import hashlib
#import chinese_converter
import sys
import eventlet
if sys.version_info[0]==2:
	import six
	from six.moves.urllib import request
if sys.version_info[0]==3:
	from eventlet.green.urllib import request
import random
import socket
import os
import json
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report, unlinked_position_figure

from functions.models import index_pages, skipped_company
from functions.views import function_field_dictionary, qccfield_to_modelfield, check_individual, proxy_request, remove_fluff, standardize, empty_check, link_individual

from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

from functions.views import function_field_dictionary, qccfield_to_modelfield
import time
from functions.models import index_pages
from qcc_project.settings import subregion_codes
total_count = 0
debug_status = False

import json
def remove_currency_characters(target_dictionary):
	currency_field_list = [
	'ShouldCapi',
	'RegistCapi',
	]
	remove_dictionary = {
		'万元人民币' : '000',
		'万元'      : '000',
		'萬元'      : '000000',
		'亿元'      : '000000000',
		'人民幣'  : '',
		'元'      : ',',
		}
	for currency_field in currency_field_list:
		try:
			output_variable = target_dictionary[currency_field]
			for remove_target in list(remove_dictionary):
				output_variable = output_variable.replace(remove_target, remove_dictionary[remove_target])
			try:
				output_variable = float(output_variable)  
				target_dictionary[currency_field] = output_variable
			except:
				try:
					target_dictionary.pop(currency_field)
				except:
					pass
		except:
			pass
	return(target_dictionary)

def depreciation_check(target_relation):
	raw_response = target_relation.original_response
	if 'name' in list(raw_response):
		result = True
	else:
		result = False
	return result 

def make_json_readable(raw_response_string):
	problem_characters = {
		"'" : '"',
		'False' : '"False"',
		'True' 	: '"True"',
		'None' 	: '"None"',
	}
	for problem_character in list(problem_characters):
		raw_response_string = raw_response_string.replace(problem_character, problem_characters[problem_character])
	return(raw_response_string)

true_keys = [] # used as container for keys after depreciation_check (which side of the qccfield the file used)
relations_list = company_relation.objects.filter(percent_total__isnull=True, shouldcapi__isnull=True, raw_to_fields_successful=False).all()
for relation_inst in relations_list:
	total_failure = True 	#variable defaults to True, switches to fault if a single key has success. Used to distinguish between "except" triggers from true
							#  errors and those causes by keys not being in the original / raw response because of function (get) type

	original_response_dict_string = make_json_readable(relation_inst.original_response)
	original_response_dict = json.loads(original_response_dict_string)
	for key in list(original_response_dict):
		print(type(original_response_dict[key]))

	print(original_response_dict)
	depreciation_check_value = depreciation_check(relation_inst)
	attribute_pair_dictionary = {}
	for key in list(qccfield_to_modelfield):
		print(key)
		try:
			if depreciation_check(relation_inst) == False:
				print(original_response_dict[key])
				attribute_pair_dictionary[qccfield_to_modelfield[key]] = original_response_dict[key]
			else:
				print(original_response_dict[qccfield_to_modelfield[key]])
				attribute_pair_dictionary[key] = original_response_dict[key]
			total_failure = False
		except:
			print("Well, oops... Nothing for that key ({}).".format(key))

	for key in list(attribute_pair_dictionary):
		print("{} - {}".format(key, attribute_pair_dictionary[key]))

	for field_name in company_relation._meta.get_fields():
		print(getattr(relation_inst, field_name.name))
	relation_inst.save()

