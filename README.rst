v2ex\_daily\_mission
====================

|Latest Version| |Build Status|

::

            _____                 _       _ _                   _         _
           / __  \               | |     (_) |                 (_)       (_)
    __   __`' / /' _____  __   __| | __ _ _| |_   _   _ __ ___  _ ___ ___ _  ___  _ __
    \ \ / /  / /  / _ \ \/ /  / _` |/ _` | | | | | | | '_ ` _ \| / __/ __| |/ _ \| '_ \
     \ V / ./ /__|  __/>  <  | (_| | (_| | | | |_| | | | | | | | \__ \__ \ | (_) | | | |
      \_/  \_____/\___/_/\_\  \__,_|\__,_|_|_|\__, | |_| |_| |_|_|___/___/_|\___/|_| |_|
                                               __/ |
                                              |___/

基本简介：
-------

模拟登录 v2ex 完成任务领钱 OvO

功能和亮点
--------

-  Python 2.7+/3.3+ support
-  支持 Linux/Windows
-  签到领钱
-  本地日志记录，查询
-  查询连续登录天数

基本安装
-------

::

    $ (sudo)pip install v2ex_daily_mission

如何使用
-------

配置文件
~~~~~~~

你可以选择手动新建配置文件(Linux 用户: ``/usr/local/bin/v2ex_config.json``,
Windows 用户: ``C:\\PythonXX\\Scripts\\v2ex_config.json``)。

::

    {
        "username": "your_username",
        "password": "your_password",
        "log_directory": "/path/to/log_directory/"
    }

或者试试自带的子命令(可能需要 root 权限或者管理员权限)：

::

    $ v2ex init

按照提示输入用户名，密码和日志路径即可。 在设置日志文件路径时注意 Linux 和 Windows 下的目 录分隔符不一样，举个例子：

-  Linux: ``/home/lord63/code/v2ex_daily_mission/``
-  Windows: ``E:\\code\\v2ex_daily_mission\\``

生成的配置文件的默认地址， Linux 在 ``/usr/local/bin/v2ex_config.json``, Windows 用户在
``C:\\PythonXX\\Scripts\\v2ex_config.json``\ 。你也可以手动指定生成的配置文件的路径：

::

    $ v2ex init --directory /home/lord63/code/v2ex_daily_mission

开始使用
~~~~~~~

完成任务得到钱：

::

    $ v2ex sign

查看最近的日志情况(默认天数 5 )：

::

    $ v2ex read

也可以通过参数来查看最近的情况

::

    $ v2ex read -c NUMBER

查看已经连续登录多少天

::

    $ v2ex last

以上的是使用默认的配置文件，你也可以自己手动指定配置文件的地址，使用 ``--config`` 参数， 比如在 Linux 下：

::

    $ v2ex --config /home/lord63/v2ex_config.json sign

通过 ``v2ex -h`` 和各个子命令的帮助文档获得使用更为详细的使用帮助

Linux 用户建议将任务加入 ``cron`` 定时运行, 比如我的：

::

    12 19 * * * /usr/local/bin/v2ex sign

实际使用举例
----------

首次签到:

::

    $ v2ex sign
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币
    Total:5439.0

如果你已经签到过了:

::

    $ v2ex sign
    You have completed the mission today.

本地日志查询最近签到领钱的情况(默认设置是 5 ):

::

    $ v2ex read
    2014-07-27 19:12:03,902 [INFO] 20140727 的每日登录奖励 15 铜币    Total:5346.0
    2014-07-28 19:12:03,751 [INFO] 20140728 的每日登录奖励 28 铜币    Total:5374.0
    2014-07-29 19:12:03,750 [INFO] 20140729 的每日登录奖励 27 铜币    Total:5401.0
    2014-07-30 19:12:03,471 [INFO] 20140730 的每日登录奖励 12 铜币    Total:5413.0
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币    Total:5439.0

你当然也可以指定显示日志的数量:

::

    $ v2ex read -c 1
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币    Total:5439.0

查询你连续登录的天数:

::

    $ v2ex last
    已连续登录 54 天

Development
-----------

首先安装依赖，推荐使用 virtualenv:

::

    $ virtualenv venv
    $ . venv/bin/activate
    (venv)$ pip install -r dev-requirements.txt

安装开发版本下的 v2ex_daily_mission, 方便调试和测试:

::

    (venv)$ python setup.py develop

运行测试:

::

    (venv)$ make test

也可以使用 tox 在 python2.7, 3.3 和 3.4 运行测试：

::

    (venv)$ tox

License
-------

MIT

.. |Latest Version| image:: http://img.shields.io/pypi/v/v2ex_daily_mission.svg
   :target: https://pypi.python.org/pypi/v2ex_daily_mission
.. |Build Status| image:: https://travis-ci.org/lord63/v2ex_daily_mission.svg
   :target: https://travis-ci.org/lord63/v2ex_daily_mission
