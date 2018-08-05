import tornado.web
import hashlib
import time
from basehandler import BaseHandler

class ApplicationHandler(BaseHandler):
    '''
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
    '''
    
    def logout(self):
        self.clear_cookie("user")
        self.clear_cookie("token")
        self.redirect(u"/")

    def index(self):
        if self.get_current_user_token() is None:
            self.render("login.html")
        else:
            self.redirect("/dashboard")

    def login(self):
        self.render("login.html")

    #@tornado.web.authenticated
    def dashboard(self):
        if self.get_current_user_token() is None:
            self.redirect('/login')
        else:
            user=self.get_current_user_token()
            u=self.application.admin.exists(user)
            self.render("dashboard.html", user=user, email='abcd', secret=u['secret'])

    def get(self, route):
        # Fetch appropriate handler
        if not hasattr(self, str(route)):
            self.redirect('/login')
            return
            #raise RouteNotFound(route)

        # Pass along the data and get a result
        handler = getattr(self, str(route))
        handler()

    def post(self, route):
        if (route == 'authdone'):
            email = self.get_argument("user", "")
            token = self.get_argument("token", "")
            now=time.gmtime()
            gen_token = hashlib.sha1('%s/%d%d%d%d' % (email, now.tm_mon, now.tm_mday, now.tm_year, now.tm_hour)).hexdigest()
            if token == gen_token:
                self.set_current_user_token(email, token)
            else:
                print('authdone: token error')
        else:
            route = route.replace('/', '_')
            # Fetch appropriate handler
            if not hasattr(self, str(route)):
                self.write("API route %s not implemented" % (route))
                return

            # Pass along the data and get a result
            handler = getattr(self, str(route))
            handler(route)
            return
