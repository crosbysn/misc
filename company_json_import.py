from requests_html import HTMLSession
import requests
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import hashlib

from functions.views import function_field_dictionary, qccfield_to_modelfield
from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report, figure_relation
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields


f = open('C:/Users/crosb/Desktop/qcc_company_archive/2ac66ce8c5dea0610395207b014335da.txt', "r", encoding='utf-8')

data = json.load(f)



for primary_key in data:
	print(primary_key)

