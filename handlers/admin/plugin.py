from handlers.admin_base import BaseHandler, authenticated_async
from handlers.admin.mock import MockHandler
from tornado import gen
from tornado.web import escape, app_log as log
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from includes.functions import Function
from includes.test_runner import TestRunner
from munch import munchify
from QTLibrary import QTLibrary
import json
import random
import time


class PluginHandler(BaseHandler):
    @authenticated_async
    @gen.coroutine
    def get(self, op='user_data'):
        mock = MockHandler()
        if op == 'loan_mock':
            data = mock.loan()
            data = dict(loan_mock=data)
            return self.return_json(data)
        province = {
            '11': '北京市',
            '12': '天津市',
            '13': '河北省',
            '14': '山西省',
            '15': '内蒙古自治区',
            '21': '辽宁省',
            '22': '吉林省',
            '23': '黑龙江省',
            '31': '上海市',
            '32': '江苏省',
            '33': '浙江省',
            '34': '安徽省',
            '35': '福建省',
            '36': '江西省',
            '37': '山东省',
            '41': '河南省',
            '42': '湖北省',
            '43': '湖南省',
            '44': '广东省',
            '45': '广西壮族自治区',
            '46': '海南省',
            '50': '重庆市',
            '51': '四川省',
            '52': '贵州省',
            '53': '云南省',
            '54': '西藏自治区',
            '61': '陕西省',
            '62': '甘肃省',
            '63': '青海省',
            '64': '宁夏回族自治区',
            '65': '新疆维吾尔自治区'
        }
        data_gen = QTLibrary()
        banks = [dict(name="招商银行股份有限公司北京分行  ", start=6214830, end=6214832, n=9),
                 dict(name="中国工商银行总行营业部", start=6222020, end=6222022, n=12),
                 dict(name="中国建设银行北京新华支行", start=6227000, end=6227002, n=12)]
        bank = random.choice(banks)
        params = dict(mobile='{}{}'.format(random.choice(['13', '14', '15', '16', '17', '18', '19']),
                                           random.randint(100000000, 999999999)), name=data_gen.gen_name(),
                      id_card=data_gen.gen_idcard(maxAge=int(
                          (time.time() - time.mktime(time.strptime('1970-01-02', '%Y-%m-%d')))/3600/24/365)),
                      bank_card=str(random.randint(bank['start'], bank['end'])) + data_gen.gen_nums(bank['n']),
                      bank_name=bank['name'],
                      email='{}@automation.test'.format(''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6))))
        params['birthday'] = time.strftime('%Y-%m-%d', time.strptime(params['id_card'][6:-4], '%Y%m%d'))
        params['age'] = int((time.time() - time.mktime(time.strptime(params['birthday'], '%Y-%m-%d')))/3600/24/365)
        params['sex'] = '男' if int(params['id_card'][-2]) % 2 != 0 else '女'
        params['origin'] = province[params['id_card'][0:2]]
        params['hosts'], count = yield self.setting.get_settings_list(pid=30, s_type='host', limit=None)
        for host in params['hosts']:
            host['ip'] = json.loads(host.value)['ip']
        params = munchify(params)
        argv = dict(title='测试数据构造工具', op=op, params=params)
        argv = dict(self.argv, **argv)
        self.render('admin/plugin.html', **argv)


class RunTests(object):
    executor = ThreadPoolExecutor(50)

    def __init__(self):
        self.func = Function()

    @run_on_executor
    def exec_shell(self, host='localhost', port=22, username='root', password='', shell=''):
        return self.func.exec_shell(host=host, port=port, username=username, password=password, shell=shell)
