from tornado.web import RequestHandler
from tornado import gen
from includes.options import OptionsFunc


class IndexHandler(RequestHandler):
    @gen.coroutine
    def prepare(self):
        self.func_option = OptionsFunc()
        self.company = yield self.func_option.get_option_by_name(name='company')
        self.argv = dict(company=self.company)

    @gen.coroutine
    def get(self):
        self.redirect('/admin/login')
        """
        argv = dict(title='首页')
        argv = dict(self.argv, **argv)
        self.render('index.html', **argv)
        """


class HelpHandler(RequestHandler):
    def get(self):
        self.redirect('/static/readme.html')
