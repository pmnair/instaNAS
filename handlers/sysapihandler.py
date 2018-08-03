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
        if self.get_current_user_token() is None:
            self.render("login.html")
        else:
            status = json.dumps({
                "Hostname": self.application.sys.hostname,
                "OS": self.application.sys.os_info(),
                "CPU": self.application.sys.cpu(),
                "Uptime": self.application.sys.uptime(),
                })
        print(status)
        self.write(status)

    def get(self, route):
        self.redirect('/index')

    def post(self, route):
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
'''
def list_drives():
        udev_ctx = pyudev.Context()
        for disk in udev_ctx.list_devices(subsystem='block', DEVTYPE='disk'):
                #pprint(disk)
                print(disk.device_node)
                if 'ID_FS_TYPE' in disk:
                        print("  " + disk.get('ID_FS_TYPE'))
                for part in disk.children:
                        #pprint(part)
                        print("  " + part.device_node)
                        if 'ID_FS_TYPE' in part:
                                print("    " + part.get('ID_FS_TYPE'))
                                print(os.path.ismount(part.device_node))
'''
