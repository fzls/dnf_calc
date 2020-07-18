#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : common
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import platform

if platform.system() == "Windows":
    import win32api
    import win32con


def notify_error(logger, message):
    if logger is not None:
        logger.error(message)
    if platform.system() == "Windows":
        win32api.MessageBox(0, message, "出错啦", win32con.MB_ICONWARNING)


encoding_error_str = "Found invalid character in key name: '#'. Try quoting the key name. (line 1 column 2 char 1)"

###########################################################
#                         工具函数                        #
###########################################################

# 格式化时间为比较美观的格式
def format_time(ftime):
    days, remainder = divmod(ftime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_str = ""
    if days > 0:
        remaining_time_str += "{}d".format(int(days))
    if days > 0 or hours > 0:
        remaining_time_str += "{:02}h".format(int(hours))
    if hours > 0 or minutes > 0:
        remaining_time_str += "{:02}m".format(int(minutes))
    remaining_time_str += "{:02.2f}s".format(seconds)

    return remaining_time_str


def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % tuple(rgb)
