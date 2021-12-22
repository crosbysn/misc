
import urllib.request
import bs4	

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from mainsite.models import company, individual, company_relation, figure_relation
from functions.models import index_pages

for company_obj in individual.objects.all():
	company_obj.delete()
print(individual.objects.all().count())
for company_obj in company.objects.all():
	company_obj.delete()
print(company.objects.all().count())

for relation_obj in company_relation.objects.all():
	relation_obj.delete()
print(company_relation.objects.all().count())

for relation_obj in figure_relation.objects.all():
	relation_obj.delete()
print(figure_relation.objects.all().count())

for page_itr in index_pages.objects.all():
	page_itr.next_page = 0
	page_itr.save()