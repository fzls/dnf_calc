#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : common
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import win32api
import win32con


def notify_error(logger, message):
    if logger is not None:
        logger.error(message)
    win32api.MessageBox(0, message, "出错啦", win32con.MB_ICONWARNING)