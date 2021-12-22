
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


def proxy_request(target_url, firm_string="NULL", use_datacenter=True):

    use_datacenter = False #set to false to use residential
    res_user = 'lum-customer-c_6986a326-zone-qichacharoute_err-pass_dyn'
    res_password = 'k97wx2y50im1'
    center_user = 'lum-customer-c_6986a326-zone-qccroute_err-pass_dyn'
    center_password = '1s3d20mmk9tb'
    class SingleSessionRetriever:
        if use_datacenter:
            username = center_user
            password = center_password
        else:
            username = res_user
            password = res_password

        session_id = random.random()
        port = 22225

        def __init__(self, username, password, requests_limit, failures_limit):
            self._username = username
            self._password = password
            self._requests_limit = requests_limit
            self._failures_limit = failures_limit
            self._reset_session()

        def _reset_session(self):
            session_id = random.random()
            proxy = ('http://%s-country-de-session-%s:%s@zproxy.lum-superproxy.io:%d' % (self._username, session_id, self._password,
                                                  SingleSessionRetriever.port))
            proxy_handler = request.ProxyHandler({'http': proxy, 'https': proxy})
            self._opener = request.build_opener(proxy_handler)
            self._opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
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
            return(body)


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
    req_timeout = 1
    n_parallel_exit_nodes = 1
    switch_ip_every_n_req = 1
    max_failures = 2

    returned_page = MultiSessionRetriever('lum-customer-c_6986a326-zone-qichacharoute_err-pass_dyn', 'k97wx2y50im1', switch_ip_every_n_req, max_failures).retrieve(
        [target_url] * n_total_req, req_timeout, n_parallel_exit_nodes, output)
    returned_page = returned_page.decode('utf-8')
    return returned_page

