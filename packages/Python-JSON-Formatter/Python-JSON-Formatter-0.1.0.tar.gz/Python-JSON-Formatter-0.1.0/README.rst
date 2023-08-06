Python JSON Formatter
======================

A log formatter for python logging. Based on https://github.com/marselester/json-log-formatter

做了如下更改: message改为logmsg字段, 额外添加了logcreated, logname, loglevel字段

安装
----

使用pip安装::

    pip install Python-JSON-Formatter


使用
----

例如下面的代码::

    logger = logging.getLogger('test')
    logger.warn('logger test', extra={'t': datetime.datetime.now().isoformat()})

产生如下格式日志(已格式化，实际一行一条日志)::

    {
      "t": "2017-11-29T14:53:14.981141",
      "logmsg": "logger test",
      "logcreated": 1511938394.9812107,
      "logname": "test",
      "loglevel": "WARNING"
    }
    {
      "t": "2017-11-29T14:53:15.949140",
      "logmsg": "logger test",
      "logcreated": 1511938395.9492354,
      "logname": "test",
      "loglevel": "WARNING"
    }
