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

class ShareApiHandler(BaseHandler):
    def list(self, route):
        shares = []
        l = self.application.share.list()
        for s in l:
            share = self.application.share.info(s)
            shares.append(share)

        status = json.dumps({
            "Shares": shares,
            })
        print(status)
        self.write(status)

    def add(self, route):
        d = json.loads(self.request.body)
        name = d['name']
        path = d['path']
        user = d['user']
        rd = d['read']
        wr = d['write']
        if self.application.share.add(name, path, user, rd=rd, wr=wr):
            status = "Success: share '{0}' added".format(name)
        else:
            status = "Error: share '{0}' add failed!".format(name)
        resp = json.dumps({
            "Status": status,
            })
        print(resp)
        self.write(resp)

    def delete(self, route):
        d = json.loads(self.request.body)
        name = d['name']
        if self.application.share.delete(name):
            status = "Success: share '{0}' deleted".format(name)
        else:
            status = "Error: share '{0}' delete failed!".format(name)
        resp = json.dumps({
            "Status": status,
            })
        print(resp)
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
