#!/usr/bin/python

import os
import pymongo
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import base64
import uuid

from handlers.basehandler import *
from handlers.applicationhandler import *
from handlers.adminapihandler import *
from handlers.sysapihandler import *
from handlers.userapihandler import *
from handlers.shareapihandler import *
from handlers.mountapihandler import *
from handlers.driveapihandler import *

from data.admin import *
from data.system import *
from data.user import *
from data.share import *
from data.mount import *
from data.drives import *

SERVER_IP='0.0.0.0'
SERVER_PORT=8080
MONGO_URL='mongodb://localhost:27017/'

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/api/drive/(.*)', DriveApiHandler),
            (r'/api/mount/(.*)', MountApiHandler),
            (r'/api/share/(.*)', ShareApiHandler),
            (r'/api/sys/(.*)', SysApiHandler),
            (r'/api/user/(.*)', UserApiHandler),
            (r'/api/admin/(.*)', AdminApiHandler),
            (r'/(.*)', ApplicationHandler),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret":    base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            #'xsrf_cookies': True,
            'debug': True,
            'log_file_prefix': "tornado.log",
        }

        tornado.web.Application.__init__(self, handlers, **settings)
        self.dbconn = pymongo.MongoClient(MONGO_URL)
        self.admin = Admin(self.dbconn['insta-nas-db'])
        self.sys = System()
        self.user = User()
        self.share = Share()
        self.mount = Mount()
        self.drives = Drives(self.mount)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(SERVER_PORT, SERVER_IP)
    tornado.ioloop.IOLoop.instance().start()
