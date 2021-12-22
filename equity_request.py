import requests
import json

url = "https://www.qcc.com/api/charts/getEquityInvestment"

payload = json.dumps({
  "keyNo": "d9f0e83c6be0d8fda45238389100257e"
})
headers = {
  'authority': 'www.qcc.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
  'dnt': '1',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
  'content-type': 'application/json',
  'accept': 'application/json, text/plain, */*',
  'x-requested-with': 'XMLHttpRequest',
  'a13c5e819f41821a2748': '2c33dd41c4422ce0ffb6dd9076b1e49d95cf5f514aae7ed059da9d27c949189cd63dbd2599e6e657226ea52fdde9c71adea6a36703c806210eb1a20182057321',
  'sec-ch-ua-platform': '"Windows"',
  'origin': 'https://www.qcc.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.qcc.com/web/charts/equity-chart?keyNo=d9f0e83c6be0d8fda45238389100257e',
  'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
  'cookie': '_uab_collina=162744968933816721588883; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201627449690165%2C%22updated%22%3A%201627449934257%2C%22info%22%3A%201627449690166%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22undefined%22%7D; qcc_did=eaa820a5-bc9f-4df0-a873-00e9bafacab8; UM_distinctid=17c2af5cdc2c23-053b39048999de-b7a1a38-1fa400-17c2af5cdc3e61; CNZZDATA1254842228=1036727909-1632801313-%7C1633991104; acw_tc=2ff6189c16340807267565193ea4aed9e981b4f62c28bf08896b0e8473; QCCSESSID=8cfa039fe24f906fb6c90163e7; zg_did=%7B%22did%22%3A%20%2217aeb8f88317cf-0d5c22e7c464b-2343360-1fa400-17aeb8f8832e2b%22%7D; zg_294c2ba1ecc244809c552f8f6fd2a440=%7B%22sid%22%3A%201634080743855%2C%22updated%22%3A%201634080849894%2C%22info%22%3A%201634080743857%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22undefined%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201634080743855%7D'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
