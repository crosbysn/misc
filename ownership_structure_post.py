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

multiple_pull_mode = False #set to true if you want to itterate through several. Leaving this in case bulk / error fixing pulls are needed later. 
query_list   = 'd9f0e83c6be0d8fda45238389100257e' #remove this and pass as a variable in the live version, string is preset for texting

if multiple_pull_mode == False:
  firm_string_list = [query_list,]
else:
  firm_string_list = query_list

def remove_currency_characters(target_dictionary):
  currency_field_list = [
  'ShouldCapi',
  'RegistCapi',
  ]
  remove_dictionary = {
    '万元人民币' : '000',
    '万元'    : '000',
    '萬元'    : '000000',
    '亿元'    : '000000000',
    '人民幣'  : '',
    '元'      : ',',
  }
  for currency_field in currency_field_list:
      output_variable = target_dictionary[currency_field]
      for remove_target in list(remove_dictionary):
        output_variable = output_variable.replace(remove_target, remove_dictionary[remove_target])
      try:
        output_variable = float(output_variable)  
        target_dictionary[currency_field] = output_variable
      except:
        try:
          target_dictionary.pop(currency_field)
        except:
          pass
  return(target_dictionary)

for firm_string in firm_string_list:
  session   = HTMLSession()
  origin_company = company.objects.get(backend_string=firm_string) #add function moving forward to reste cookie after some amount (need to see what the server allows) of pings
  cookie_ping = session.get("https://www.qcc.com/firm/{}.html".format(firm_string)) 
  cookie = str(cookie_ping.cookies)
  function_options = {
   'getOwnershipStructure'              : 'https://www.qcc.com/api/charts/getOwnershipStructure', 
   'getUltimateBeneficiaryNoPath'       : 'https://www.qcc.com/api/charts/getUltimateBeneficiaryNoPath',  
   'getEquityInvestment'              : ' https://www.qcc.com/api/charts/getEquityInvestment',
   'getHoldingCompany'                  : 'https://www.qcc.com/api/charts/getHoldingCompany',  
   #'getEnterpriseOverview'              : 'https://www.qcc.com/api/charts/getEnterpriseOverview',  
   #'getSuspectedActualControllerNoPath' : 'https://www.qcc.com/api/charts/getSuspectedActualControllerNoPath',
   }  
  payload = json.dumps({"keyNo": firm_string})
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
    '9e9b205403ec3efe7232': '4de659cb1fa47861f5bb555477c2c4a6f3498374f9da4a2224f6a1dd866f57430d0d89577275aac113163ea3089fa6bee82f58c3fa0d29b2c1897ddd01adee3b',
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
    'cookie': cookie,}

  response_key = {
    'getOwnershipStructure'             : 'EquityShareDetail',
    'getEquityInvestment'               : 'EquityShareDetail',
    'getUltimateBeneficiaryNoPath'      : 'Names',
    'getHoldingCompany'                 : 'Names',
    #'getSuspectedActualControllerNoPath': 'ControllerData',
    #'getEnterpriseOverview'             : 'Oper',}
    }

  for function in list(response_key):
    url = (function_options[function])
    response = requests.request("POST", url, headers=headers, data=payload)
    response_payload   = json.loads(response.text)['Result']
    response_lookup_value = response_key[function]
    company_list  = response_payload[response_lookup_value]
    list_len = len(company_list)
    list_pos = 0
    print()
    print("---{}---".format(function))
    first_key = list(company_list[0])[0]
    try:
      force_compute_value = (company_list[0][first_key])
      print("Function returned {} entities. Debugcheck returned first company with ID: {}.".format(list_len, force_compute_value))
      function_pull_possible = True
    except:
      function_pull_possible = False
    if function_pull_possible == False:
      print("No returnable values for {} using {}. Creating error report with type 'CHART_FUNCTION'".format(origin_company.企业名称, function))
      new_error = error_report(
          model_type    = 'company',
          model_inst    = firm_string,
          error_type    = 'CHART_FUNCTION',
          text          = response.text)
      new_error.save()
    else:
      for result_item in company_list:
        list_pos += 1

       
        company_results_dict = {}
        company_results_dict_cleaned = {}
        company_results_dict['KeyNo'] = result_item['KeyNo']
        company_results_dict['Name'] = result_item['Name']
        company_results_dict['CompanyCode'] = result_item['CompanyCode']
        company_results_dict['EconKind'] = result_item['EconKind']
        company_results_dict['Percent'] = result_item['Percent']
        company_results_dict['PercentTotal'] = result_item['PercentTotal']
        company_results_dict['Level'] = result_item['Level']
        company_results_dict['result_org'] = result_item['Org']
        company_results_dict['ShouldCapi'] = result_item['ShouldCapi']
        company_results_dict['StockRightNum'] = result_item['StockRightNum']
        company_results_dict['DetailCount']  = result_item['DetailCount']
        company_results_dict['ShortStatus'] = result_item['ShortStatus']
        company_results_dict['StockType'] = result_item['StockType']
        company_results_dict['InvestType'] = result_item['InvestType']
        company_results_dict['RegistCapi'] = result_item['RegistCapi']
        company_results_dict['Tags'] = result_item['Tags']
        company_results_dict['DetailList'] = result_item['DetailList']
        for KeyNo in company_results_dict:
          if type(company_results_dict[KeyNo]) == str:
            traditionalized_string = chinese_converter.to_traditional(company_results_dict[KeyNo])
            company_results_dict[KeyNo] = traditionalized_string
            company_results_dict_cleaned[KeyNo] = traditionalized_string
            if len(company_results_dict[KeyNo]) == 0:
              pass
          else:
            company_results_dict_cleaned[KeyNo] = company_results_dict[KeyNo]
        company_results_dict = company_results_dict_cleaned
        company_results_dict['Percent'] = float((company_results_dict['Percent'].replace("%", "")))
        company_results_dict['PercentTotal'] = float((company_results_dict['PercentTotal'].replace("%", "")))
        
        company_results_dict = remove_currency_characters(company_results_dict)


        try:
          linked_company = company.objects.get(backend_string = company_results_dict['KeyNo'], 企业名称 = result_item['Name'])
          company_found = True

        except:
          linked_company = company(
            backend_string = company_results_dict['KeyNo'],
            企业名称 = result_item['Name']

            )
          linked_company.save()
          company_found = False
        if company_found == True:
          link_message = "Company exists to link!"
        else:
          link_message = "Company did not exist, creating and linking!"
        print("{}/{}. {}".format(list_pos, list_len, link_message))
        relation_inst = company_relation(
          relation_type   = function,
          parent_company  = origin_company,
          child_company   = linked_company)
        if company_results_dict.has_key('EconKind'):
          relation_inst.econ_kind     = company_results_dict['EconKind']
        if company_results_dict.has_key('Percent'):
          relation_inst.percent     = company_results_dict['Percent']
        if company_results_dict.has_key('result_org'):
          relation_inst.org       = company_results_dict['result_org']
        if company_results_dict.has_key('PercentTotal'):
          relation_inst.percent_total   = company_results_dict['PercentTotal']
        if company_results_dict.has_key('ShouldCapi'):
          relation_inst.shouldcapi    = company_results_dict['ShouldCapi']
        if company_results_dict.has_key('StockRightNum'):
          relation_inst.stockrightnum = company_results_dict['StockRightNum']
        if company_results_dict.has_key('DetailCount'):
          relation_inst.detailcount   = company_results_dict['DetailCount']
        if company_results_dict.has_key('ShortStatus'):
          relation_inst.shortstatus   = company_results_dict['ShortStatus']
        if company_results_dict.has_key('StockType'):
          relation_inst.stocktype     = company_results_dict['StockType']
        if company_results_dict.has_key('InvestType'):
          relation_inst.investtype    = company_results_dict['InvestType']
        if company_results_dict.has_key('RegistCapi'):
          relation_inst.registered_cap  = company_results_dict['RegistCapi']    
        if company_results_dict.has_key('DetailList'):
          relation_inst.detaillist = company_results_dict['DetailList']    


        relation_inst.save()
        for tag in company_results_dict['Tags']:
          tag_name = chinese_converter.to_simplified(tag['Name'])
          tag_inst = relation_tag_sub(
            type_tag              = tag['Type'],
            name                  = tag_name,
            original_response     = tag
            )
          tag_inst.save()
          relation_inst.tags.add(tag_inst)
          relation_inst.save()  
        

        #tags      = models.ManyToManyField(relation_tag_sub)







# ----- notes and values below this line, mostly scrap but kept in case it is useful later and to prevent losses / having to dig old copies out of repo
function_field_dictionary = {
  'getEquityInvestment'                 : ['KeyNo', 'Name','CompanyCode','EconKind','Percent','PercentTotal','Level','Org','ShouldCapi','StockRightNum','DetailCount','ShortStatus','StockType','InvestType','RegistCapi','Tags','DetailList'],
  'getOwnershipStructure'               : ['KeyNo', 'Name', 'CompanyCode', 'EconKind', 'Percent', 'PercentTotal', 'Level', 'Org', 'ShouldCapi', 'StockRightNum', 'DetailCount', 'ShortStatus', 'StockType', 'InvestType', 'RegistCapi', 'Tags', 'DetailList'],
  'getHoldingCompany'                   : ['KeyNo', 'Name', 'Percent', 'PercentTotal', 'Level', 'Org', 'Oper', 'ShortStatus', 'StartDate', 'RegistCapi', 'Type', 'EconKind'],  
  'getUltimateBeneficiaryNoPath'        : ['KeyNo', 'Name', 'Percent', 'PercentTotal', 'Level', 'Org'],
  }

qccfield_to_modelfield = {
  #'KeyNo'         : ,
  #'Name'          : ,      Name and KeyNo tabbed out because they are used in all cases to generate a company object to link 
  'CompanyCode'   : 'company_code',
  'EconKind'      : 'econ_kind',
  'Percent'       : 'percent',
  'PercentTotal'  : 'percent_total',
  'Org'           : 'org',
  'ShouldCapi'    : 'shouldcapi',
  'StockRightNum' : 'stockrightnum',
  'DetailCount'   : 'detailcount',
  'ShortStatus'   : 'shortstatus',
  'StockType'     : 'stocktype',
  'InvestType'    : 'investtype',
  'RegistCapi'    : 'registered_cap',
  #'Tags'          : ,    Tags are also an object of their own that is linked, not directly entered into company / company_relation
  'DetailList'    : 'detaillist', 
  'Oper'          : 'figure_raw_string',
}

