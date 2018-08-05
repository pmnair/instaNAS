import tornado.web
import json
import hashlib
import time
import bcrypt

from basehandler import BaseHandler

class AdminApiHandler(BaseHandler):
    def register(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']

        try:
            secret = self.application.admin.add(user, passwd)
            now=time.gmtime()
            status = json.dumps({
                "Result": "Success",
                "Status": "User '%s' registered; account validation user sent. Please follow instructions in user to validate your account." % user,
                })
        except Exception as e:
            status = json.dumps({
                "Result": "Error",
                "Status": e.message,
                })

            #print(status)
        self.write(status)

    def auth_password(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']

        try:
            if self.application.admin.check_password(user, passwd):
                now=time.gmtime()
                token = hashlib.sha1('%s/%d%d%d%d' % (user, now.tm_mon, now.tm_mday, now.tm_year, now.tm_hour)).hexdigest()
                status = json.dumps({
                    "Result": "Success",
                    "Status": "User '%s' auth successful." % user,
                    "AuthToken": token,
                    "RefreshIntervalSec": 60,
                    })
            else:
                status = json.dumps({
                    "Result": "Error",
                    "Status": "Password incorrect for '%s'!" % user,
                    })
        except Exception as e:
            status = json.dumps({
                "Result": "Error",
                "Status": e.message,
                })

        #print(status)
        self.write(status)

    def auth_secret(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        secret = d['secret']

        try:
            if self.application.admin.check_secret(user, secret):
                now=time.gmtime()
                token = hashlib.sha1('%s/%d%d%d%d' % (user, now.tm_mon, now.tm_mday, now.tm_year, now.tm_hour)).hexdigest()
                status = json.dumps({
                    "Result": "Success",
                    "Status": "User '%s' auth successful." % user,
                    "AuthToken": token,
                    "RefreshIntervalSec": 60,
                    })
            else:
                status = json.dumps({
                    "Result": "Error",
                    "Status": "Secret incorrect for '%s'!" % user,
                    })
        except Exception as e:
            status = json.dumps({
                "Result": "Error",
                "Status": e.message,
                })

            #print(status)
        self.write(status)

    def delete(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']
        secret = d['secret']

        try:
            self.application.admin.delete(user, passwd, secret)
            status = json.dumps({
                "Result": "Success",
                "Status": "User '%s' deletion successful." % user,
                })
        except Exception as e:
            status = json.dumps({
                "Result": "Error",
                "Status": e.message,
                })

            #print(status)
        self.write(status)

    def update(self, route):
        d = json.loads(self.request.body)
        user = d['user']
        passwd = d['password']
        new_passwd = d['new_password']
        secret = d['secret']

        try:
            self.application.admin.update_password(user, passwd, new_passwd)
            status = json.dumps({
                "Result": "Success",
                "Status": "Update successful for user '%s'!" % user,
                })
        except Exception as e:
            status = json.dumps({
                "Result": "Error",
                "Status": e.message,
                })

            #print(status)
        self.write(status)

    def delete1(self, route):
        d = json.loads(self.request.body)
        user = d['user']

        user = self.application.db['admins'].find_one({'user': user})
        if user:
            self.application.db['admins'].remove({'user': user})
            status = json.dumps({
                "Result": "Success",
                "Status": "User '%s' deletion successful." % user,
                })
        else:
            status = json.dumps({
                "Result": "Error",
                "Status": "User '%s' not found!" % user,
                })
            self.write(status)

    def get(self, route):
        self.redirect('/index')

    def post(self, route):
        route = route.replace('/', '_')
        # Fetch appropriate handler
        if not hasattr(self, str(route)):
            status = json.dumps({
                "Status": "API route '%s' not implemented" % route,
                })
            self.write(status)
            return
        #raise RouteNotFound(route)

        # Pass along the data and get a result
        handler = getattr(self, str(route))
        handler(route)
