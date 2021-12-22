from requests_html import HTMLSession
import requests
import json

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qcc_project.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from mainsite.models import company, individual, position, relation_tag_sub, company_relation, error_report, figure_relation
from qcc_project.settings import figure_fields, company_model_translations, company_empty_string, date_fields
import hashlib
#import chinese_converter
from functions.views import function_field_dictionary, qccfield_to_modelfield


from new_proxy_tester import proxy_request


def get_company_backend(company_json):
  firm_string  = company_json['meta']['backend_string']




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
  total_relations = 0

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
    function_subdictionary = {}
    function_fields = function_field_dictionary[function]
    url = (function_options[function])
    response = proxy_request(url, firm_string)
    if json.loads(response)['Status'] == 200:
      company_json['backend-error'] = False
      error_status = False
    else:
      company_json['backend-error'] = True
      error_status = True
    if error_status == False:
      response_payload   = json.loads(response)['Result']
      response_lookup_value = response_key[function]
      company_list  = response_payload[response_lookup_value]
      try:
        force_compute_value = len(company_list)
        print(force_compute_value)
        if force_compute_value > 0:
          function_pull_possible = True
        else:
          function_pull_possible = False
      except:
        function_pull_possible = False
      company_json_backend = {}
      if function_pull_possible == False:
        function_subdictionary['no-relationships'] = True
        company_json[function] = function_subdictionary
      else:
        function_subdictionary['no-relationships'] = False
        for result_item in company_list:

          # ---- this if function is to select between operator and company relationships. the majority of info is the same, but the sublists (company vs. operator) are different
          #if function != "getUltimateBeneficiaryNoPath":
          if True == True:   
            relation_instance_dictionary = {}
            company_results_dict = {}
            company_results_dict_cleaned = {}
            tags_list = []
            
            company_results_keys = list(result_item)
            for function_key in function_fields:
              if function_key in company_results_keys:
                if len(str(result_item[function_key])) > 0:
                  company_results_dict[function_key] = result_item[function_key]
            for key in company_results_dict:
              print("{} : {}".format(key, company_results_dict[key]))
              if type(company_results_dict[key]) == str:
                company_results_dict_cleaned[key] = company_results_dict[key]              
              else:
                company_results_dict_cleaned[key] = company_results_dict[key]
            company_results_dict = company_results_dict_cleaned        
            for percent_key in ['Percent', 'PercentTotal']:
              if percent_key in list(company_results_dict):
                company_results_dict[percent_key] = float((company_results_dict[percent_key].replace("%", "")))
            company_results_dict = remove_currency_characters(company_results_dict)
            if 'Tags' in function_fields:
              for tag in company_results_dict['Tags']:
                #tag_name = chinese_converter.to_simplified(tag['Name'])
                tag_dictionary  = {
                  'name'                : tag['Name'],
                  'type_tag'            : tag['Type'],
                  'original_response'   : tag,
                  }
                tags_list.append(tag_dictionary)
              company_results_dict.pop('Tags')  
              relation_instance_dictionary['tags'] = tags_list
            try:
              subdictionary_key = company_results_dict['KeyNo']
            except:
              company_results_dict['KeyNo'] = "individual"
              subdictionary_key = company_results_dict['Name']

            relation_instance_dictionary['name'] = company_results_dict['Name']
            relation_instance_dictionary['id_string'] = company_results_dict['KeyNo']
            company_results_dict.pop('Name')
            try:
              for key in list(company_results_dict):
                true_key = qccfield_to_modelfield[key]
                relation_instance_dictionary[true_key] = company_results_dict[key]
            except:
              pass
            relation_instance_dictionary['raw'] = result_item
            function_subdictionary[subdictionary_key] = relation_instance_dictionary
    company_json[function] = function_subdictionary
  return(company_json)







