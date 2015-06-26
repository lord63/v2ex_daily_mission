# v2ex_daily_mission

[![Latest Version][1]][2]
[![The MIT License][3]][4]

## Intro：

模拟登录 v2ex 完成任务领钱 OvO

## Features

* python 2.7+/3.3+ support
* 支持 linux/windows
* 签到领钱
* 本地日志记录，查询
* 查询连续登录天数

## Install

    $ (sudo)pip install v2ex_daily_mission

## How to use：

在 `/usr/local/bin/` 目录下新建文件 `v2ex_config.json`, 像这样：

    {
        "username": "xxxx",
        "password": "xxxx",
        "log_directory": "/path/to/save/logfile/",
        "count": 5   # 查看默认的最近的情况的天数，可以自己设置
    }

完成任务得到钱：

    $ v2ex

查看最近的情况(默认天数在 v2ex_config.josn 的 count 中设置)：

    $ v2ex read

也可以通过参数来查看最近的情况

    $ v2ex read -c NUMBER

查看已经连续登录多少天

    $ v2ex last

通过 `v2ex -h` 和 `v2ex read -h` 获得使用帮助

建议将任务加入 `cron` 定时运行, 比如我的：

    12 19 * * * /usr/local/bin/v2ex

## Snapshots

首次签到:

    $ v2ex
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币
    Total:5439.0

如果你已经签到过了:

    $ v2ex
    You have completed the mission today.

本地日志查询最近签到领钱的情况(我的默认设置是 `"count": 5 `):

    $ v2ex read
    2014-07-27 19:12:03,902 [INFO] 20140727 的每日登录奖励 15 铜币    Total:5346.0
    2014-07-28 19:12:03,751 [INFO] 20140728 的每日登录奖励 28 铜币    Total:5374.0
    2014-07-29 19:12:03,750 [INFO] 20140729 的每日登录奖励 27 铜币    Total:5401.0
    2014-07-30 19:12:03,471 [INFO] 20140730 的每日登录奖励 12 铜币    Total:5413.0
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币    Total:5439.0

你当然也可以指定显示日志的数量:

    $ v2ex read -c 1
    2014-07-31 19:12:03,417 [INFO] 20140731 的每日登录奖励 26 铜币    Total:5439.0

查询你连续登录的天数:

    $ v2ex last
    已连续登录 54 天

## Reference：

* [1](http://www.v2ex.com/t/69166)
* [2](http://www.v2ex.com/t/80927)
* [3](http://www.v2ex.com/t/68549)

## License

MIT


[1]: http://img.shields.io/pypi/v/v2ex_daily_mission.svg
[2]: https://pypi.python.org/pypi/v2ex_daily_mission
[3]: http://img.shields.io/badge/license-MIT-yellow.svg
[4]: https://github.com/lord63/v2ex_daily_mission/LICENSE