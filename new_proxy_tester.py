
import sys
import eventlet
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
if sys.version_info[0]==3:
    from eventlet.green.urllib import request
import random
import socket
import urllib

def proxy_request(target_url, firm_string="NULL", username="lum-customer-c_6986a326-zone-qichacha", password="k97wx2y50im1"):
    super_proxy = socket.gethostbyname('zproxy.lum-superproxy.io')
    class SingleSessionRetriever:

        country_url_list = [
            "http://%s-country-tm-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-de-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-ar-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-my-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-gb-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-ge-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-vn-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-in-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-ie-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-ae-session-%s:%s@"+super_proxy+":%d",
            "http://%s-country-ag-session-%s:%s@"+super_proxy+":%d",
        ]
        url = country_url_list[random.randint(0, len(country_url_list) -1)]
        
        url = "http://%s-session-%s:%s@"+super_proxy+":%d" #comment this out  if you want to limit to countries above. Seems to prefer US ips, but unlcear if qcc is blocking those better. 

        port = 22225

        def __init__(self, username, password, requests_limit, failures_limit):
            self._username = username
            self._password = password
            self._requests_limit = requests_limit
            self._failures_limit = failures_limit
            self._reset_session()

        def _reset_session(self):
            session_id = random.random()
            proxy = SingleSessionRetriever.url % (self._username, session_id, self._password,
                                                  SingleSessionRetriever.port)
            proxy_handler = request.ProxyHandler({'http': proxy, 'https': proxy})
            self._opener = request.build_opener(proxy_handler)
            self._opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko')]
            self._requests = 0
            self._failures = 0

        def retrieve(self, url, timeout):
            while True:
                if self._requests == self._requests_limit:
                    self._reset_session()
                self._requests += 1
                try:
                    timer = eventlet.Timeout(timeout)
                    if firm_string =="NULL":
                        result = self._opener.open(url).read()
                    else:
                        values = {"keyNo": firm_string}
                        data = urllib.parse.urlencode(values).encode("utf-8")
                        result = self._opener.open(url, data).read()
                    timer.cancel()
                    return result
                except:
                    timer.cancel()
                    self._failures += 1
                    if self._failures == self._failures_limit:
                        self._reset_session()


    class MultiSessionRetriever:

        def __init__(self, username, password, session_requests_limit, session_failures_limit):
            self._username = username
            self._password = password
            self._sessions_stack = []
            self._session_requests_limit = session_requests_limit
            self._session_failures_limit = session_failures_limit

        def retrieve(self, urls, timeout, parallel_sessions_limit, callback):
            pool = eventlet.GreenPool(parallel_sessions_limit)
            for url, body in pool.imap(lambda url: self._retrieve_single(url, timeout), urls):
                callback(url, body)
            return body

        def _retrieve_single(self, url, timeout):
            if self._sessions_stack:
                session = self._sessions_stack.pop()
            else:
                session = SingleSessionRetriever(self._username, self._password,
                                                 self._session_requests_limit, self._session_failures_limit)
            body = session.retrieve(url, timeout)
            self._sessions_stack.append(session)
            return url, body

    def output(url, body):
        pass
    n_total_req = 1
    req_timeout = 10
    n_parallel_exit_nodes = 10
    switch_ip_every_n_req = 5
    max_failures = 1

    returned_page = MultiSessionRetriever(username, password, switch_ip_every_n_req, max_failures).retrieve(
        [target_url] * n_total_req, req_timeout, n_parallel_exit_nodes, output)
    returned_page = returned_page.decode('utf-8')
    return returned_page

