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

class UserApiHandler(BaseHandler):
    def list(self, route):
        status = json.dumps({
            "Users": self.application.user.list(),
        })
        print(status)
        self.write(status)

    def add(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']

        if self.application.user.exists(user):
            status = "Error: user '{0}' exists".format(user)
        else:
            if self.application.user.add(user, passwd, home="/home/{0}".format(user)):
                status = "Success: User '{0}' added".format(user)
            else:
                status = "Error: User '{0}' add failed!".format(user)
                resp = json.dumps({
                    "Status": status,
                })
                print(resp)
                self.write(resp)

    def delete(self, route):
        d = json.loads(self.request.body)
        user = d['user']

        if not self.application.user.exists(user):
            status = "Error: user '{0}' does not exist".format(user)
        else:
            if self.application.user.delete(user):
                status = "Success: User '{0}' deleted".format(user)
            else:
                status = "Error: User '{0}' delete failed!".format(user)
                resp = json.dumps({
                    "Status": status,
                })
                print(resp)
                self.write(resp)

    def update(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']

        if not self.application.user.exists(user):
            status = "Error: user '{0}' does not exist".format(user)
        else:
            if self.application.user.update(user, passwd):
                status = "Success: User '{0}' updated".format(user)
            else:
                status = "Error: User '{0}' update failed!".format(user)
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
