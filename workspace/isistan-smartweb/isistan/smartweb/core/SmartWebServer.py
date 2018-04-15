import sys
import argparse
import urllib
from twisted.web.resource import NoResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor, endpoints
from twisted.internet.defer import DeferredLock
from isistan.smartweb.core.SearchEngine import SearchEngine
from twisted.python import log

log.startLogging(sys.stdout)

__author__ = 'ignacio'


class SmartWeb(Resource):

    BASE_RESOURCE_LOCATION = '/isistan-smartweb/smartweb'
    PUBLISH_SERVICES_PARAMETER = 'service_list'

    def __init__(self, engine):
        assert not issubclass(engine, SearchEngine)
        self.isLeaf = True
        self._engine = engine
        self._lock = DeferredLock()
        self._services_path = self.BASE_RESOURCE_LOCATION + '/services'

    def _number_of_services_request(self, *args):
        request = args[0]
        request.write(str(self._engine.number_of_services()))
        request.finish()

    def _publish_services_request(self, *args, **kwargs):
        request = args[0]
        self._engine.publish_services(kwargs['service_list'].split(' '))
        request.write('services published')
        request.finish()

    def _find_request(self, *args):
        request = args[0]
        query = args[1]
        request.write(' '.join(self._engine.find(query)))
        request.finish()

    def render_GET(self, request):
        if request is not None and request.path != '/favicon.ico':
            if request.path == self._services_path or request.path == self._services_path + '/':
                pass
            elif request.path.startswith(self._services_path + '/'):
                query = request.path.split('/')[4]
                self._lock.run(self._find_request, request, urllib.unquote(query))
                return NOT_DONE_YET
            else:
                return NoResource().render(request)

    def render_POST(self, request):
        if request.path == self._services_path or request.path == self._services_path + '/':
            if self.PUBLISH_SERVICES_PARAMETER in request.args:
                deferred = self._lock.run(self._publish_services_request, request, service_list=request.args[self.PUBLISH_SERVICES_PARAMETER][0])
                deferred.addCallback(lambda *args: ('services published'))
                return NOT_DONE_YET
            else:
                request.setResponseCode(400)
                return self.PUBLISH_SERVICES_PARAMETER + ' POST parameter required'
        else:
            return NoResource().render(request)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-engine", help="loads a specific engine, default=WSQBESearchEngine", type=str, default='WSQBESearchEngine')
    parser.add_argument("-port", help="listen on a custom port, default=8080", type=int, default=8080)
    parser.add_argument("-conf", help="specifies a configuration file that will be passed to the engine, default=wsqbe_properties.cfg", 
    					type=str, default='wsqbe_properties.cfg')
    args = parser.parse_args()
    module_fullname = "isistan.smartweb.engine." + args.engine
    module = __import__(module_fullname, fromlist=[args.engine])
    engine = getattr(module, args.engine)()
    engine.load_configuration(args.conf)
    web_engine = SmartWeb(engine)
    reactor.listenTCP(args.port, Site(web_engine))
    reactor.run()

if __name__ == '__main__':
    run()



