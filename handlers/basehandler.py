import tornado.web
import hashlib
import time

class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler gonna to be used instead of RequestHandler
    """
    def set_current_user_token(self, user, token):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.set_secure_cookie("token", tornado.escape.json_encode(token))
        else:
            self.clear_cookie("user")
            self.clear_cookie("token")

    def get_current_user_token(self):
        u = self.get_secure_cookie("user")
        t = self.get_secure_cookie("token")
        if not u or not t:
            return None

        email = tornado.escape.json_decode(u)
        token = tornado.escape.json_decode(t)
        now=time.gmtime()
        gen_token = hashlib.sha1('%s/%d%d%d%d' % (email, now.tm_mon, now.tm_mday, now.tm_year, now.tm_hour)).hexdigest()
        if (email and token == gen_token):
            return email
        else:
            return None

    def write_error(self, status_code, **kwargs):
        if status_code in [403, 404, 500, 503]:
            self.write('You got an Error %s' % status_code)
        else:
            self.write('BOOM!')

class ApiErrorHandler(BaseHandler):
    def get(self, route):
        #self.render("index.html")
        self.write("API route %s not implemented" % (route))
