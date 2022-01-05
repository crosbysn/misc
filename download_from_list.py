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

from get_company_ids_static import get_ids #function to return index page of companies that hasn't been reviewed yet
from get_company_page import get_company_page
from get_company_backend import get_company_backend
from offline_company_page import get_company_page as offline_company_page
from offline_company_backend import get_company_backend as offline_company_backend
from functions.views import function_field_dictionary, qccfield_to_modelfield
import time
from functions.models import index_pages
from proxy_request_bee import proxy_request as proxy_request_bee
from new_proxy_tester import proxy_request
from qcc_project.settings import subregion_codes
total_count = 0




json_filename = "subregion_json_g_GX_450300.txt"
full_file_json = open(json_filename, "r", encoding='utf-8')
full_file_json = json.load(full_file_json)

for subregion_page in list(full_file_json):
	company_id_list = full_file_json[subregion_page]
	if len(company_id_list) > 0:
		company_id_dictionary = {}
		for company_id in company_id_list:
			



