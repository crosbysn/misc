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

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report

from functions.models import index_pages, skipped_company
from functions.views import function_field_dictionary, qccfield_to_modelfield, check_individual, proxy_request, remove_fluff, standardize, empty_check, link_individual

from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields

from get_company_ids import get_ids #function to return index page of companies that hasn't been reviewed yet
from get_company_page import get_company_page
from get_company_backend import get_company_backend
from offline_company_page import get_company_page as offline_company_page
from offline_company_backend import get_company_backend as offline_company_backend
from functions.views import function_field_dictionary, qccfield_to_modelfield
import time

from proxy_request_bee import proxy_request as proxy_request_bee
from new_proxy_tester import proxy_request
pages_per_run = 100
start_time = time.time()
count = 0
active_region = False
from datetime import datetime

# combined_list file records all the company strings checked by the process. As a final step we can collect all these and check against
# 	our database. Missing files can be added to the "skipped_company" objects. This is a backup, skipped_company objects should catch all.  



timenow = str(datetime.now())
timenow = timenow.replace("-", "_")
timenow = timenow.replace(" ", "_")
timenow = timenow.replace(":", "_")
timenow = timenow.split(".")[0]
region_code = input("Input region code: (e.g. g_GZ_520400)")
filename = '{}_combined_company_json'.format(region_code)
starter_file = {
	"company_list" : [],
}

json_filename = filename + ".txt"
with open(json_filename, 'w', encoding='utf-8') as startfile:
	json.dump(starter_file, startfile, ensure_ascii=False)


region_json_filename = "subregion_json_" + region_code + ".txt"

full_finished_list = [company_id for company_id.backend_string in company.objects.exclude(英文名="NULL").all()]

finished_companies_text = open(finished_companies_filename, "r", encoding='utf-8')
finished_companies_json = json.load(finished_companies_text)
initial_finished_list = list(finished_companies_json)
for region_page in list(full_region_json):
	region_page_company_list = full_region_json[region_page]
	for company_id in region_page_company_list:
		if company_id not in initial_finished_list:
			print(company_id)
			company_json_initial 		= offline_company_page(company_id)
			print("Basic page pulled, moving to relations.")
			company_json 				= offline_company_backend(company_json_initial)
			combined_company_text = open(json_filename, "r", encoding='utf-8')
			combined_company_json = json.load(combined_company_text)	
			company_json['index_page_source'] = region_page
			combined_company_json[company_id] = company_json
			with open(json_filename, 'w', encoding='utf-8') as outfile:
			    json.dump(combined_company_json, outfile, ensure_ascii=False)
			print("Saved json for {}".format(company_id))
			finished_companies_text = open(finished_companies_filename, "r", encoding='utf-8')
			finished_companies_json = json.load(finished_companies_text)
			finished_companies_json[company_id] = company_id
			with open(finished_companies_filename, 'w', encoding='utf-8') as outfile:
			    json.dump(finished_companies_json, outfile, ensure_ascii=False)			
'''		
for number in range(0, pages_per_run):
	print("Active region is {}".format(active_region))
	company_id_return 	= get_ids(active_region)
	region_page 		= company_id_return[1] + "_" + str(company_id_return[2])
	active_region 		= company_id_return[1] 
	company_id_list 	= company_id_return[0]
	
	for company_id in company_id_list:

'''