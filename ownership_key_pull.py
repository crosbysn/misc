from requests_html import HTMLSession
import requests
import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields
import hashlib
import chinese_converter

session 	= HTMLSession()
firm_string   = 'f625a5b661058ba5082ca508f99ffe1b'

origin_company = company.objects.get(backend_string=firm_string)

cookie_ping = session.get("https://www.qcc.com/firm/{}.html".format(firm_string)) 
cookie = str(cookie_ping.cookies)

function_options = {
 'getOwnershipStructure'              : 'https://www.qcc.com/api/charts/getOwnershipStructure', 
 'getHoldingCompany'                  : 'https://www.qcc.com/api/charts/getHoldingCompany',  
 'getUltimateBeneficiaryNoPath'       : 'https://www.qcc.com/api/charts/getUltimateBeneficiaryNoPath',  
 'getEquityInvestment'              : ' https://www.qcc.com/api/charts/getEquityInvestment',  
 
 #'getEnterpriseOverview'              : 'https://www.qcc.com/api/charts/getEnterpriseOverview',  
 #'getSuspectedActualControllerNoPath' : 'https://www.qcc.com/api/charts/getSuspectedActualControllerNoPath',  

}
response_key = {
  'getOwnershipStructure'             : 'EquityShareDetail',
  'getEquityInvestment'               : 'EquityShareDetail',
  'getUltimateBeneficiaryNoPath'      : 'Names',
  'getHoldingCompany'                 : 'Names',
  
  #'getEnterpriseOverview'             : 'Oper',
  #'getSuspectedActualControllerNoPath': 'ControllerData',
}

function = 'getEquityInvestment'

for function in list(function_options):
  url = (function_options[function])

  payload = json.dumps({
    "keyNo": firm_string
  })
  headers = {
    'authority': 'www.qcc.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'dnt': '1',
    'ecd31b8846aea0d5fc99': '8153714e8f22e062e33a69f8fe4074561f15696b666ccd05725a0289615dee1f4064585e40e9901a68df7740e41fa207d0887e03676459b7080fe9e2d3cccbfc',
    'a13c5e819f41821a2748': '2c33dd41c4422ce0ffb6dd9076b1e49d95cf5f514aae7ed059da9d27c949189cd63dbd2599e6e657226ea52fdde9c71adea6a36703c806210eb1a20182057321',
    'a206edab9596abc73845': '366ff0731922f99f0869c5d5a2393e8f00362856630b442e101f859eab119e3ca748ec1a480d062185b37be12389761741c30f5e975c24b2960eccec2579c2e7',
    'b8e1d09e075621ece111': 'c536e7f23264e24a71d1b3d72a24124b035a62342ceea9a06a978633dde63d8d031e7706438bea46f3ee9e5d37b63a81691f110d9ff1a6f9af63a0ab2508f6ae',
    'c339d6c9d146f73cfdc5': '636de7911490b13560857cf7f226efa3dc8aa0974a05fc3c19d74a42d2021521ee330086267ea4c390df2d500bac87ada8461e69240f9eb5dff5c5803faf5d13',
    '9e9b205403ec3efe7232': '73cea9013f80a1c5b9e361a59df7c78a0f0d079982766b72d541393d785e9b421165d92d0f9c70fd993f2cd3a9ed96e6d2421a626a9c3896ba1566b3d51d4876',

    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"Windows"',
    'origin': 'https://www.qcc.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.qcc.com/web/charts/equity-chart?keyNo={}&name=undefined&uinfo='.format(firm_string),
    'accept-language': 'en-US,en;q=0.9',
    'cookie': cookie,
  }



  response = requests.request("POST", url, headers=headers, data=payload)
  print(function)
  function_key_list = []

  response_payload   = json.loads(response.text)['Result']
  response_lookup_value = response_key[function]
  company_list  = response_payload[response_lookup_value]
  test_company = company_list[0]
  for key in test_company:
    function_key_list.append(key)

  print(function_key_list)
