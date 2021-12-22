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
from functions.views import function_field_dictionary, qccfield_to_modelfield

multiple_pull_mode = False #set to true if you want to itterate through several. Leaving this in case bulk / error fixing pulls are needed later. 
#query_list = input("String ID:  ")
query_list = []
'''
for company_inst in company.objects.all():
  relations_count = company_relation.objects.filter(origin_company=company_inst).count()
  print(relations_count)
  if relations_count == 0 and company_inst.relations_check == False:
    query_list.append(company_inst.backend_string)
  else:
    company_inst.relations_check = True
    company_inst.save()
print(query_list)
'''
query_list = 'f625a5b661058ba5082ca508f99ffe1b'
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
    '万元'      : '000',
    '萬元'      : '000000',
    '亿元'      : '000000000',
    '人民幣'  : '',
    '元'      : ',',
  }
  for currency_field in currency_field_list:
      try:
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
      except:
        pass
  return(target_dictionary)

def send_request(target_url, firm_string):
    payload = json.dumps({"keyNo": firm_string})
    s = requests.Session()
    r = s.post(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'K5UPOMMS2EJLHRDXLS743G02C6GEM4YV0XFEJW8P8JUIEATU9Y5QIJGJKJ2J7XZ2047N1KEDIO3VB465',
            'url': target_url, 
            'render_js': 'false', 
        },
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
        },
        data = payload, 

    )
        
    return r

for firm_string in firm_string_list:
  total_relations = 0
  session   = HTMLSession()
  origin_company = company.objects.get(backend_string=firm_string) #add function moving forward to reste cookie after some amount (need to see what the server allows) of pings
  function_options = {
   'getOwnershipStructure'              : 'https://www.qcc.com/api/charts/getOwnershipStructure', 
   'getUltimateBeneficiaryNoPath'       : 'https://www.qcc.com/api/charts/getUltimateBeneficiaryNoPath',  
   'getEquityInvestment'              : 'https://www.qcc.com/api/charts/getEquityInvestment',
   'getHoldingCompany'                  : 'https://www.qcc.com/api/charts/getHoldingCompany',  
   #'getEnterpriseOverview'              : 'https://www.qcc.com/api/charts/getEnterpriseOverview',  
   #'getSuspectedActualControllerNoPath' : 'https://www.qcc.com/api/charts/getSuspectedActualControllerNoPath',
   }  


company_relation_dict = {
    'getOwnershipStructure'             : 'Parent Company',
    'getEquityInvestment'               : 'Child Company',
    'getUltimateBeneficiaryNoPath'      : 'Ultimate Beneficiary',
    'getHoldingCompany'                 : 'Holding Company',


}
  response_key = {
    'getOwnershipStructure'             : 'EquityShareDetail',
    'getEquityInvestment'               : 'EquityShareDetail',
    'getUltimateBeneficiaryNoPath'      : 'Names',
    'getHoldingCompany'                 : 'Names',
    #'getSuspectedActualControllerNoPath': 'ControllerData',
    #'getEnterpriseOverview'             : 'Oper',}
    }

  for function in list(response_key):
    function_fields = function_field_dictionary[function]
    url = (function_options[function])
    response = send_request(url, firm_string)
    if json.loads(response.text)['Status'] == 200:
      error_status = False
    else:
      new_error = error_report(
        model_type  = "company_relation",
        model_inst  = firm_string,
        error_type  = "RELATION_PULL_ERROR",
        text        = json.loads(response.text)['Status'])
      new_error.save()
      error_status = True
    if error_status == True:
      print("Error occured ({}/{}), report filed. Moving to next company.".format(new_error.error_type, new_error.text))
    else:
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
        origin_company.relations_check = True
        company_inst.save()
      else:
        for result_item in company_list:
          list_pos += 1
          company_results_dict = {}
          company_results_dict_cleaned = {}
          company_results_keys = list(result_item)
          for function_key in function_fields:
            if function_key in company_results_keys:
              if len(str(result_item[function_key])) > 0:
                company_results_dict[function_key] = result_item[function_key]
          for key in company_results_dict:
            if type(company_results_dict[key]) == str:
              standardized_string = chinese_converter.to_simplified(company_results_dict[key])
              company_results_dict_cleaned[key] = standardized_string
            else:
              company_results_dict_cleaned[key] = company_results_dict[key]
          company_results_dict = company_results_dict_cleaned        
          for percent_key in ['Percent', 'PercentTotal']:
            if percent_key in list(company_results_dict):
              company_results_dict[percent_key] = float((company_results_dict[percent_key].replace("%", "")))
          company_results_dict = remove_currency_characters(company_results_dict)
          try:
            linked_company = company.objects.get(backend_string = firm_string, 企业名称 = company_results_dict['Name'])
            company_found = True
          except:
            linked_company = company(
              backend_string = firm_string,
              企业名称 = company_results_dict['Name']
              )
            linked_company.save()
            company_found = False
          if company_found == True:
            link_message = "Company exists to link!"
          else:
            link_message = "Company did not exist, creating and linking!"
          print("{}/{}. {}".format(list_pos, list_len, link_message))
          for existing_relation in company_relation.objects.filter(relation_type=function,origin_company=origin_company,target_company=linked_company).all():
            existing_relation.delete()

          relation_inst = company_relation(
            relation_type   = company_relation_dict[function],
            origin_company  = origin_company,
            target_company   = linked_company)
          relation_inst.save()
          total_relations += 1
          try:
            company_results_dict.pop('KeyNo')
          except:
            pass
          company_results_dict.pop('Name')
          if 'Tags' in function_fields:
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
            company_results_dict.pop('Tags')  
          for key in list(company_results_dict):
            print("{} : {}".format(key, company_results_dict[key]))
            setattr(relation_inst, qccfield_to_modelfield[key], company_results_dict[key])
            relation_inst.save()
  print("Company has a total of {} recorded relationships vs. {} recieved in this pull.".format(total_relations, company_relation.objects.filter(origin_company=origin_company).count()))
  origin_company.relations_check = True
  origin_company.save()










