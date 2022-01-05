
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

def debug_check(debug_message, debug_status=debug_status):
	if debug_status == True:
		print(debug_message)
	else:
		pass
def process_json_company(focused_company, qccfield_to_modelfield=qccfield_to_modelfield):

	found_keys = list(focused_company['meta'])
	try:
		company_obj = company.objects.get(backend_string = focused_company['meta']['backend_string'], 企业名称 = focused_company['meta']['企业名称'])
		print("Company matching {} ({}) found, updating existing entry.".format(company_obj.企业名称, company_obj.backend_string))
	except:
		company_obj = company(
			backend_string=focused_company['meta']['backend_string'],
			企业名称 = focused_company['meta']['企业名称'],
			)
		company_obj.save()
		print("No existing company record found, creating for {} ({}.".format(company_obj.企业名称, company_obj.backend_string))
	potential_model_fields = [f.name for f in company._meta.get_fields()]
	for key in found_keys:
		if key != '企业名称':
			if key[len(key)-1] == "\n":
				new_key = key[:len(key)-1]
				focused_company['meta'][new_key] = focused_company['meta'][key]
				focused_company['meta'].pop(key)
				key = new_key
			if key in potential_model_fields:
				setattr(company_obj, key, focused_company['meta'][key])
			else:
				debug_check("Key not found for: {}".format(key))
				if key in figure_fields: # will create duplicates if figure is listed in header information and detail information, need to scrape out duplicates in later step. better to keep extra than potentially lose data 
					debug_check("Adding to figure fields.")
					new_figure_dictionary = {}
					new_figure_dictionary['name'] = focused_company['meta'][key]
					new_figure_dictionary['position'] = key
					focused_company['operators'].append(new_figure_dictionary) 
	company_obj.save()
	try:
		company_obj.index_page_source = focused_company['index_page_source']
		company_obj.save()
	except:
		print("No index page source found, verify file predates recording index_pages.")
	operator_list = focused_company['operators']
	for operator in operator_list:
		try: 
			operator_name 		= operator['name']
			operator_position 	= operator['position']
			operator_id 		= operator['backend_string']
			try:
				operator_obj = individual.objects.get(backend_string=operator_id, name=operator_name)
				debug_check("Found individual matching {}, {}".format(operator_obj.backend_string, operator_obj.name))
			except:
				operator_obj = individual(
					backend_string = operator_id,
					name = operator_name)
				operator_obj.save()
			try:
				position_obj = position.objects.get(position_individual = operator_obj, position_company = company_obj, position_title = operator_position)
				debug_check("Found position matching {}, {}".format(position_obj.position_individual.operator_name, position_obj.position_company.backend_string))

			except:
				position_obj = position(
					position_individual = operator_obj,
					position_company = company_obj,
					position_title = operator_position )
				position_obj.save()

		except:
			if len(operator_name) != 0 :
				unlinked_position_figure_obj = unlinked_position_figure(
					name 				= operator_name,
					position_company  	= company_obj,
					position_title     	= operator_position)

				unlinked_position_figure_obj.save()
				debug_check("{} / {}".format(unlinked_position_figure_obj.name, unlinked_position_figure_obj.position_title))
				debug_check("Operator key is incomplete, info is retained in 'offline_json_raw' attribute of company object and as an 'unlinked_position_figure'.")
			else:
				debug_check("Operator key is majority incomplete, no object created. Info retained in the offline_json_raw element.")
	company_obj.offline_json_raw = focused_company
	company_obj.save()
	relation_field_keys = [f.name for f in company_relation._meta.get_fields()]
	qccfield_to_modelfield = qccfield_to_modelfield
	try:
		qccfield_to_modelfield.pop('Oper')
	except:
		debug_check("No operative found for company.")
	relations_function_list = ['getOwnershipStructure', 'getUltimateBeneficiaryNoPath', 'getEquityInvestment', 'getHoldingCompany']
	for relation_type in relations_function_list:
		debug_check(relation_type)
		for company_key in list(focused_company[relation_type])[1:]:
			focused_relation = focused_company[relation_type][company_key]['raw']
			

			relation_object = company_relation(
				relation_type = relation_type,
				origin_company = company_obj,
				original_response = focused_relation,
				)
			try:
				target_company = company.objects.get(backend_string=focused_relation['KeyNo'], 企业名称=focused_relation['Name'])
				debug_check("Company exists to link with relation company ({} ({})".format(target_company.backend_string, target_company.企业名称))
			except:
				target_company = company(
					backend_string=focused_relation['KeyNo'], 
					企业名称=focused_relation['Name']
					)
				target_company.save()
				
				debug_check("Company created to link with relation company ({} ({})".format(target_company.backend_string, target_company.企业名称))
			relation_object.target_company = target_company
			focused_relation = remove_currency_characters(focused_relation)
			for percent_key in ['Percent', 'PercentTotal']:
				if percent_key in list(focused_relation):
					if len(focused_relation[percent_key]) != 0: #do not trunacte to an if ~ and statement, len of key depends on key existing
						focused_relation[percent_key] = float((focused_relation[percent_key].replace("%", "")))
			try:
				if len(focused_relation['Tags']) > 0:
					relation_object.tags_raw = focused_relation['Tags']
			except:
				try: 
					if len(focused_relation['tags']) > 0:
						relation_object.tags_raw = focused_relation['tags']
				except:
					pass
			for key in list(qccfield_to_modelfield):
				try: 
					if len(focused_relation[key]) > 0:
						setattr(relation_object, qccfield_to_modelfield[key], focused_relation[key])
					else:
						debug_check("Empty field in relation for {}".format(key))
				except:
					debug_check("No entry in relation for {}.".format(key))

			relation_object_check = company_relation.objects.filter(relation_type=relation_type, origin_company=company_obj, target_company=target_company).all()
			if len(relation_object_check) == 1:
				debug_check("Relation duplicate exists, replacing with current relation information.")
				relation_object_check.delete()
			elif len(relation_object_check) > 1:
				debug_check("Multiple duplicate relations existed, potential substantial error.")
				for relation_dup in relation_object_check:
					relation_dup.delete()

			relation_object.save()


import_filename_list = ['combined_company_json_2021_12_21_21_45_36', 'combined_company_json_2021_12_21_21_45_48', 'combined_company_json_2021_12_21_21_45_44', 'combined_company_json_2021_12_21_21_45_53']
# only preset in the development version, otherwise will pull filenames from directory list function

from datetime import datetime, date
start = datetime.now()
def percentage_done(completed, total, initial_done, start=start):
	completed = len(completed)
	total = len(total) - initial_done
	progress = completed/total
	percent_progress = progress * 100 
	print()
	print()
	print()
	print("{}% Company Logs Finished. ({}/{})".format(percent_progress, completed, total))
	current = datetime.now()
	duration = current - start
	duration = duration.total_seconds()
	projected_duration = duration / progress
	projected_duration_minutes = projected_duration/60
	projected_duration_seconds = str(round(projected_duration, 2))
	projected_duration_minutes = str(round(projected_duration_minutes, 2))
	print("Process has taken {} seconds, expected to take another {} seconds ({} minutes).".format(duration, projected_duration_seconds, projected_duration_minutes))
	print()
	print()
import_filename_done = []
import_filename_broken = []
initial_done = len(import_filename_done)
for import_filename_inst in import_filename_list:
	try:
		if import_filename_inst not in import_filename_done:
			print(import_filename_inst)
			import_filename_done.append(import_filename_inst)
			import_filename = import_filename_inst + ".txt"

			single_mode 	= False

			full_file_json = open(import_filename, "r", encoding='utf-8')
			full_file_json = json.load(full_file_json)
			focused_company_list = []
			if single_mode == True:
				focused_company = list(full_file_json)[1]
				focused_company_id_list = [focused_company, ]
			else:
				focused_company_id_list = list(full_file_json)[1:]
			for company_id in focused_company_id_list:
				focused_company_list.append(full_file_json[company_id])
			for focused_company in focused_company_list:
				process_json_company(focused_company)

			print(company.objects.all().count())
			print(individual.objects.all().count())
			print(company_relation.objects.all().count())
		else:
			
			print("Already processed {}.".format(import_filename_inst))
		percentage_done(import_filename_done, import_filename_list, initial_done)
	except:
		import_filename_done.remove(import_filename_inst)
		import_filename_broken.append(import_filename_inst)
		print("File structure failure in {}. Total failure count at: {}.".format(import_filename_broken, len(import_filename_broken)))
print(import_filename_done)
print("  ")
print()
print()
print()
print("DONE")
print()
print()
print(import_filename_broken)
