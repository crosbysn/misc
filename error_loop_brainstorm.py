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
from functions.models import index_pages
from proxy_request_bee import proxy_request as proxy_request_bee
from new_proxy_tester import proxy_request


progress = ((index_pages.objects.filter(emptied=True).count()) / index_pages.objects.all().count() ) * 100
print(str(progress) + "%")
print()
for index_page in index_pages.objects.filter(emptied=False):
	if index_page.next_page != 0:
		print(index_page.index_code)
		print(index_page.next_page)
		print()
