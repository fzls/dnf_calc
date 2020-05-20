#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : config
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

import toml
import logging

from dnf_calc import notify_error, logger, consoleHandler

g_config = {}


# 读取程序config
def load_config(config_path = "config.toml"):
    global g_config
    try:
        g_config = toml.load(config_path)
    except FileNotFoundError as error:
        notify_error(logger, "未找到{}文件，是否直接在压缩包中打开了？".format(config_path))
        exit(0)
    set_log_level(g_config)
    logger.info("config loaded")
    logger.debug("config={}".format(g_config))

log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

def set_log_level(config):
    consoleHandler.setLevel(log_level_map[config["log_level"]])

def config():
    return g_config
