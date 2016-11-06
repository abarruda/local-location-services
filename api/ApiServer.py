from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from api import app
from api import config

api_port = config.get('api', 'API_PORT')

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(api_port)
enable_pretty_logging()
print "Local Location Services API started."
IOLoop.instance().start()