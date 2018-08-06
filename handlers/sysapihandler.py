import os
import sys
import glob
import signal
import logging
import pyudev
import platform
import subprocess
import json

from basehandler import BaseHandler

class SysApiHandler(BaseHandler):
    def info(self, route):
        self.application.sys.refresh()
        status = json.dumps({
            "Hostname": self.application.sys.hostname,
            "OS": self.application.sys.os_info(),
            "CPU": self.application.sys.cpu(),
            "Uptime": self.application.sys.uptime(),
            })
        #print(status)
        self.write(status)

    def hostname_set(self, route):
        d = json.loads(self.request.body)
        name = d['name']
        if self.application.sys.change_hostname(self.application.sys.hostname, name):
            status = "Success: new hostname is {0}".format(name)
        else:
            status = "Error: hostname change failed!"
        resp = json.dumps({
            "Status": status,
            })
        #print(resp)
        self.write(resp)

    def get(self, route):
        self.redirect('/index')

    def post(self, route):
        if self.get_current_user_token() is None:
            self.render("login.html")
        else:
	        route = route.replace('/', '_')
	        # Fetch appropriate handler
	        if not hasattr(self, str(route)):
	            status = json.dumps({
	                "Status": "API route sys/'%s' not implemented" % route,
	                })
	            self.write(status)
	            return
	        #raise RouteNotFound(route)

	        # Pass along the data and get a result
	        handler = getattr(self, str(route))
	        handler(route)
