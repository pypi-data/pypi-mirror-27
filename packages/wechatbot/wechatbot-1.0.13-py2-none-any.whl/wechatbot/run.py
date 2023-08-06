# -*- coding:utf-8 -*-
import time

from tools import now
from ping import MyBot

bot = MyBot()


def worker():
    while True:
        bot.sync_host_check()
        check_time = now()
        bot.sync_check()
        msg = bot.sync()
        bot.handle_msg(msg)
        check_time = now() - check_time
        if check_time < 1:
            time.sleep(1 - check_time)
            bot.save_snapshot()
        continue


if __name__ == '__main__':
    bot.login_wechat()
    worker()
