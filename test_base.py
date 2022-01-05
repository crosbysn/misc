
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

full_finished_list = [company_id.backend_string for company_id in company.objects.exclude(英文名="NULL").all()]

print(len(full_finished_list))
print(company.objects.count())