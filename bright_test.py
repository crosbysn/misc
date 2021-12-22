import sys

res_user 		= 'lum-customer-c_6986a326-zone-qichacha'
res_pas			= 'k97wx2y50im1'
datacenter_user = 'lum-customer-c_6986a326-zone-qcc'
datacenter_pas 	= '1s3d20mmk9tb'

target_url = 'https://www.qcc.com/firm/f625a5b661058ba5082ca508f99ffe1b.html'

def bright_proxy(target_url):
    if sys.version_info[0]==2:
        import six
        from six.moves.urllib import request
        import random
        username = 'lum-customer-c_6986a326-zone-qcc'
        password = '1s3d20mmk9tb'

        port = 22225
        session_id = random.random()
        super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
            (username, session_id, password, port))
        proxy_handler = request.ProxyHandler({
            'http': super_proxy_url,
            'https': super_proxy_url,
        })
        opener = request.build_opener(proxy_handler)
        print('Performing request')
        print(opener.open(target_url).read())
    if sys.version_info[0]==3:
        import urllib.request
        import random
        username = res_user
        password = res_pas
        port = 22225
        session_id = random.random()
        super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
            (username, session_id, password, port))
        proxy_handler = urllib.request.ProxyHandler({
            'http': super_proxy_url,
            'https': super_proxy_url,
        })
        opener = urllib.request.build_opener(proxy_handler)
        print('Performing request')
        print(opener.open(target_url).read())
bright_proxy(target_url)

