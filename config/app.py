import os
from includes.ui_modules import NavModule

# 数据库配置
db_host = 'db'
db_port = 3306
db_name = 'openTest'
db_user = 'root'
db_password = '123456'
db_charset = 'utf8'
db_pool_size = 150
db_pool_recycle = 3600
db_timeout = 5

# 应用配置
app_port = 9090     # 应用默认端口
template_path = os.path.join(os.path.dirname(__file__), '../templates')
static_path = os.path.join(os.path.dirname(__file__), '../static')
login_url = '/admin/login'
ui_modules = {'nav': NavModule}
cookie_secret = 'SQYMzDHiShGCl1gx/e4g5HHS7Be1UkPpk7eJxklvKmE='
xsrf_cookie = True
debug = True

# 定时任务配置
cycle_time = 5    # 定时任务监控周期(秒)
