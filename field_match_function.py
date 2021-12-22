
import urllib.request
import bs4	
from requests_html import HTMLSession
import hashlib

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from mainsite.models import company, individual, position,company_relation
 


company_relation_dict = {
    'getOwnershipStructure'             : 'Parent Company',
    'getEquityInvestment'               : 'Child Company',
    'getUltimateBeneficiaryNoPath'      : 'Ultimate Beneficiary',
    'getHoldingCompany'                 : 'Holding Company',


}
for company_relation_inst in company_relation.objects.all():
	function = company_relation_inst.relation_type
	print(function)
	function_updated = company_relation_dict[function]
	print(function_updated)
	company_relation_inst.relation_type = function_updated
	company_relation_inst.save()
	print(company_relation.relation_type)
'''
input_string = "f625a5b661058ba5082ca508f99ffe1b"
company_target = company.objects.get(backend_string=input_string, 企业名称="企查查科技有限公司")
for related_position in position.objects.filter(position_company=company_target).all():
	print(related_position.position_individual)

relation_set = company_relation.objects.filter(origin_company=company_target).all()
for relation in relation_set:
	print(relation.target_company.企业名称)
	print("{}%  [{}]".format(relation.percent_total, relation.relation_type))

print("Total of {} relations where this company is the origin point.".format(company_relation.objects.filter(origin_company=company_target).count()))
'''