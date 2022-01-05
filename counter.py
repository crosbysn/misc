
import urllib.request
import bs4	

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from mainsite.models import company, individual, company_relation, figure_relation, unlinked_position_figure
from functions.models import index_pages

print("Companies")
print(company.objects.all().count())
print("Individuals")
print(individual.objects.all().count())
print("Relations")
print(company_relation.objects.all().count())