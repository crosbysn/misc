
import json
import requests

target_url = 'https://www.qcc.com/api/charts/getEquityInvestment'
firm_string = 'd9f0e83c6be0d8fda45238389100257e'
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
print(send_request(target_url, firm_string).text)

