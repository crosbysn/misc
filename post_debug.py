 
import sys
import eventlet
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
if sys.version_info[0]==3:
    from eventlet.green.urllib import request
import random
import socket
import json
import urllib
firm_string = 'd9f0e83c6be0d8fda45238389100257e'
request_url = 'https://www.qcc.com/api/charts/getOwnershipStructure'
values = {"keyNo": firm_string}

data = urllib.parse.urlencode(values).encode("utf-8")



use_datacenter = True #set to false to use residential

res_user = 'lum-customer-c_6986a326-zone-qichacha'
res_password = 'k97wx2y50im1'
center_user = 'lum-customer-c_6986a326-zone-qcc'
center_password = '1s3d20mmk9tb'
if use_datacenter:
    username = center_user
    password = center_password
else:
    username = res_user
    password = res_password


super_proxy = socket.gethostbyname('zproxy.lum-superproxy.io')

url = "http://%s-country-us-session-%s:%s@"+super_proxy+":%d"
port = 22225


session_id = random.random()
proxy = url % (username, session_id, password,
                                      port)
proxy_handler = request.ProxyHandler({'http': proxy, 'https': proxy})
opener = request.build_opener(proxy_handler)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
opener.addheaders = [
    ('ecd31b8846aea0d5fc99', '8153714e8f22e062e33a69f8fe4074561f15696b666ccd05725a0289615dee1f4064585e40e9901a68df7740e41fa207d0887e03676459b7080fe9e2d3cccbfc'), 
    ('a13c5e819f41821a2748', '2c33dd41c4422ce0ffb6dd9076b1e49d95cf5f514aae7ed059da9d27c949189cd63dbd2599e6e657226ea52fdde9c71adea6a36703c806210eb1a20182057321'),
    ('a206edab9596abc73845', '366ff0731922f99f0869c5d5a2393e8f00362856630b442e101f859eab119e3ca748ec1a480d062185b37be12389761741c30f5e975c24b2960eccec2579c2e7'),
    ('b8e1d09e075621ece111', 'c536e7f23264e24a71d1b3d72a24124b035a62342ceea9a06a978633dde63d8d031e7706438bea46f3ee9e5d37b63a81691f110d9ff1a6f9af63a0ab2508f6ae'),
    ('c339d6c9d146f73cfdc5', '636de7911490b13560857cf7f226efa3dc8aa0974a05fc3c19d74a42d2021521ee330086267ea4c390df2d500bac87ada8461e69240f9eb5dff5c5803faf5d13'),
    ('9e9b205403ec3efe7232', '4de659cb1fa47861f5bb555477c2c4a6f3498374f9da4a2224f6a1dd866f57430d0d89577275aac113163ea3089fa6bee82f58c3fa0d29b2c1897ddd01adee3b'),
]
result = opener.open(url, data).read()
print(result)