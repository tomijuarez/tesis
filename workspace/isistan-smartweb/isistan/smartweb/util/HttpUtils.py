import urllib2


class HttpUtils:

    @staticmethod
    def http_request(url):
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        return opener.open(url).read()
