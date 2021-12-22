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

from proxy_request_dynamic import proxy_request


pages_per_run = 5

active_region = False

for number in range(0, pages_per_run):
	print("Active region is {}".format(active_region))
	company_id_return 	= get_ids(active_region)
	active_region 		= company_id_return[1]
	company_id_list 	= company_id_return[0]
	missed_list 		= []
	for company_id in company_id_list:
		get_company_page(company_id)
		print("Getting relational info...")
		get_company_backend(company_id)

	for missed_company in missed_list:
		missed_company_obj = skipped_company(
			backend_string = missed_company
			)
		missed_company_obj.save()
	print("Logged missed pages for {} due to incomplete scrape of current page.".format(missed_list))
	print(len(missed_list))

with open('{}.txt'.format(company_id), 'w') as outfile:
    json.dump(data, outfile)