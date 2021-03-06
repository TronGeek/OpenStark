from tornado.web import RequestHandler, app_log as log
from tornado import gen, httpclient, httputil
from modules.setting import SettingModule
from modules.user import UserModule
from modules.project import ProjectModule
from modules.option import OptionModule
from includes.functions import Function
from includes.options import OptionsFunc
import json
import functools
import time


# 异步用户认证
def authenticated_async(f):
    @functools.wraps(f)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        self._auto_finish = False
        self.current_user = yield self.get_current_user_async()
        if not self.current_user and self.request.uri.find('/admin/plugin') < 0:
            if self.request.method == 'GET':
                self.redirect(self.get_login_url())
            else:
                self.send_error(403)
        else:
            f(self, *args, **kwargs)
    return wrapper


class BaseHandler(RequestHandler):
    """
    后台管理父类，后台相关handlers继承本类
    """
    current_user = None

    # 初始化方法
    @gen.coroutine
    def prepare(self):
        self.func = Function()
        self.user = UserModule()
        self.project = ProjectModule()
        self.setting = SettingModule()
        self.option = OptionModule()
        self.func_option = OptionsFunc()
        self.company = yield self.func_option.get_option_by_name(name='company')
        self.limit = yield self.func_option.get_option_by_name(name='page_limit')
        self.company = self.company if self.company else 'BST开源测试平台'
        self.argv = dict(company=self.company)

    # 获取当前用户信息
    @gen.coroutine
    def get_current_user_async(self):
        user = self.get_secure_cookie('BSTSESSION', None)
        if user is not None:
            if isinstance(user, bytes):
                user = user.decode('utf8', errors='ignore')
            username = user
            user = yield self.user.get_user_info(email_or_username=username)
            if not user:
                self.clear_cookie('BSTSESSION')
                user = yield self._login_or_register(username=username)
        else:
            user = None
        return user

    # 接口返回json格式字符串
    def return_json(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, ensure_ascii=False)
        self.set_header('Content-Type', 'application/json')
        self.write(msg)
        self.finish()

    @gen.coroutine
    def _login_or_register(self, username='', email='', password='123456'):
        self.clear_cookie('BSTSESSION')
        if (username == '' and email == '') or password == '':
            return None
        username = email if email != '' else username
        user = yield self.user.get_user_info(username)
        if not user:
            if not self.func.check_string(username, 'email'):
                return None
            else:
                result, msg = yield self.user.register_user(username, password)
                if result:
                    self.set_secure_cookie('BSTSESSION', username, 1)
                    user = yield self.user.get_user_info(username)
                    return user
                else:
                    return None
        if user.password == self.func.encode_password(password) and user.status == 1:
            self.user.edit_user(username, last_login_time=time.strftime('%Y-%m-%d %H:%M:%S'))
            self.set_secure_cookie('BSTSESSION', user.email, 1)
        return user

