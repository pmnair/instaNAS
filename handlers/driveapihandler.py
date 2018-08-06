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

class DriveApiHandler(BaseHandler):
    def mount(self, route):
        d = json.loads(self.request.body)
        dev = d['device']
        path = d['path']
        if self.application.drives.mount(dev, path):
            status = "Success: Drive mounted!"
        else:
            status = "Success: Drive mount failed!"
        resp = json.dumps({
            "Status": status,
            })
        #print(resp)
        self.write(resp)

    def unmount(self, route):
        d = json.loads(self.request.body)
        dev = d['device']

        if self.application.drives.unmount(dev):
            status = "Success: Drive unmounted!"
        else:
            status = "Error: Drive unmount failed!"
        resp = json.dumps({
            "Status": status,
            })
        #print(resp)
        self.write(resp)

    def list(self, route):
        status = json.dumps({
            "Drives": self.application.drives.list(),
            })
        #print(status)
        self.write(status)

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
