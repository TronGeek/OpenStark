from handlers.admin_base import BaseHandler
from tornado import gen


# 登录操作类
class LoginHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        username = self.get_argument('username', default='').strip()
        email = self.get_argument('email', default='').strip()
        password = self.get_argument('password', default='123456').strip()
        user = yield self._login_or_register(username=username, password=password, email=email)
        if user:
            self.redirect('/admin/dashboard')
        else:
            self.redirect('/admin/register')

    @gen.coroutine
    def post(self):
        username = self.get_argument('username', default='').strip()
        email = self.get_argument('email', default='').strip()
        password = self.get_argument('password', default='123456').strip()
        user = yield self._login_or_register(username=username, email=email, password=password)
        if user:
            self.redirect('/admin/dashboard')
        else:
            self.redirect('/admin/register')
