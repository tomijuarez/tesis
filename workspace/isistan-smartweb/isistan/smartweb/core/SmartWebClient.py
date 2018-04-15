import urllib
import urllib2

from isistan.smartweb.core.SearchEngine import SearchEngine
from isistan.smartweb.util.HttpUtils import HttpUtils

__author__ = 'ignacio'


class SmartWebClient(SearchEngine):

    BASE_RESOURCE_LOCATION = '/isistan-smartweb/smartweb'
    PUBLISH_SERVICES_PARAMETER = 'service_list'

    def __init__(self, server_address, server_port):
        self._server_address = server_address
        self._server_port = server_port
        self._server_url = 'http://' + self._server_address  + ':' + self._server_port
        self._services_path = self.BASE_RESOURCE_LOCATION + '/services'


    def publish_services(self, service_list):
                
        values = {
            self.PUBLISH_SERVICES_PARAMETER : ' '.join(service_list),
        }

        data = urllib.urlencode(values)
        req = urllib2.Request(self._server_url + self._services_path, data)
        print HttpUtils.http_request(req)

    def find(self, query):
        url = self._server_url + self._services_path +'/' + urllib.quote(query)
        return HttpUtils.http_request(url).split(' ')

    def publish(self, service):
        pass

    def unpublish(self, service):
        pass

    def number_of_services(self):
        pass