from requests_html import HTMLSession
import requests
import json


session 	= HTMLSession()
firm_string = 'd9f0e83c6be0d8fda45238389100257e'
cookie_ping = session.get("https://www.qcc.com/firm/{}.html".format(firm_string)) 
cookie = str(cookie_ping.cookies)

url = "https://www.qcc.com/api/charts/getEquityInvestment"

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

response_dict 	= json.loads(response.text)['Result']
company_list 	= response_dict['EquityShareDetail']

test_company 	= company_list[0]

for company in test_company:
	print("{}: {}".format(company, test_company[company]))

	
	print()

'''KeyNo
Name
CompanyCode
EconKind
Percent
PercentTotal
Level
Org
ShouldCapi
StockRightNum
DetailCount
ShortStatus
StockType
InvestType
RegistCapi
Tags
DetailList
'''

