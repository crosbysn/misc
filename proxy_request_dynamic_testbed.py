
import sys
import eventlet

import random
import socket
import urllib.request

def proxy_request(target_url):
    username = 'lum-customer-c_6986a326-zone-qichacha-route_err-pass_dyn'
    password = 'k97wx2y50im1'
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-country-de-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))

    opener = urllib.request.build_opener(proxy_handler)
    print(opener.open(target_url).read())
    print(failurepoint)