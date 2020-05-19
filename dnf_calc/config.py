#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : config
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

import toml

from dnf_calc import notify_error, logger

g_config = {}


# 读取程序config
def load_config(config_path = "config.toml"):
    global g_config
    try:
        g_config = toml.load(config_path)
    except FileNotFoundError as error:
        notify_error(logger, "未找到{}文件，是否直接在压缩包中打开了？".format(config_path))
        exit(0)
    logger.info("config loaded")
    logger.debug("config={}".format(g_config))


def config():
    return g_config
