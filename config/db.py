import tormysql
import pymysql
import config.app as app_cfg
from tornado.log import app_log as log
from tornado.web import gen


# 创建数据库连接池
pool = tormysql.helpers.ConnectionPool(
    max_connections=app_cfg.db_pool_size,
    idle_seconds=app_cfg.db_pool_recycle,
    wait_connection_timeout=app_cfg.db_timeout,
    host=app_cfg.db_host,
    port=app_cfg.db_port,
    user=app_cfg.db_user,
    passwd=app_cfg.db_password,
    db=app_cfg.db_name,
    charset=app_cfg.db_charset,
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


# 初始化数据库
@gen.coroutine
def init_db():
    sql = """
CREATE TABLE IF NOT EXISTS `t_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_options_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `t_projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user` text,
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_projects_name` (`name`),
  KEY `ix_t_projects_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `t_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` int(11) NOT NULL,
  `type` varchar(20) NOT NULL COMMENT 'url 接口、crypt 加解密、host 环境、job 任务、list 用例、suite 测试集、log 日志、param 参数、report 报告',
  `name` varchar(1000) NOT NULL,
  `value` longtext NOT NULL,
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常, job[0 计划中, 1 排队中, 2 测试中, 3 已完成, 4 暂停, 5 异常]',
  `sort` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `project` (`project`),
  KEY `ix_t_settings_type` (`type`),
  KEY `ix_t_settings_status` (`status`),
  CONSTRAINT `t_settings_ibfk_1` FOREIGN KEY (`project`) REFERENCES `t_projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `t_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  `nickname` varchar(50) DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `registerTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastLoginTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role` smallint(6) NOT NULL DEFAULT '2' COMMENT '0 超级管理员, 1 管理员, 2 普通用户',
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '0 禁用, 1 正常',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_t_users_email` (`email`),
  UNIQUE KEY `ix_t_users_username` (`username`),
  KEY `ix_t_users_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    tx = yield pool.begin()
    try:
        log.info('初始化数据库SQL:\n{}'.format(sql))
        for s in sql.split(';'):
           s.strip() and (yield tx.execute(s))
    except pymysql.Error as e:
        yield tx.rollback()
        log.error('初始化数据库失败#{}'.format(e))
    else:
        yield tx.commit()
        log.info('初始化数据库成功')
