#!/usr/bin/env python3
# coding: utf-8

from GroupHelperClass import GroupHelper
import json
import time


def main():
    bot = GroupHelper(token=json.load(open(".bot"))['token'])

    while True:
        bot.check_update()
        time.sleep(1)


if __name__ == '__main__':
    main()