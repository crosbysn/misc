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
pages_per_run = 500
start_time = time.time()
count = 0
active_region = False

for number in range(0, pages_per_run):
	print("Active region is {}".format(active_region))
	company_id_return 	= get_ids(active_region)
	active_region 		= company_id_return[1]
	company_id_list 	= company_id_return[0]
	missed_list 		= []
	try:
		for company_id in company_id_list:
			print(company_id)
			company_json_initial 		= offline_company_page(company_id)
			print("Basic page pulled, moving to relations.")
			company_json 				= offline_company_backend(company_json_initial)
			with open('{}.txt'.format(company_id), 'w', encoding='utf-8') as outfile:
			    json.dump(company_json, outfile, ensure_ascii=False)
			print("Saved json for {}".format(company_id))
	except:
			
		for missed_company in missed_list:
			missed_company_obj = skipped_company(
				backend_string = missed_company
				)
			missed_company_obj.save()
	count +=1
	print(count)



end_time = time.time()
total_time = end_time - start_time
time_per_ping = pages_per_run/total_time
print(time_per_ping)

