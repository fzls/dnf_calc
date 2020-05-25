#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : setting
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

import yaml
import yaml.parser

from dnf_calc import notify_error, logger

###########################################################
#                        读取自定义配置                    #
###########################################################

g_setting = {}

default_settings = [
    {"name": "styles", "path": "setting/styles.yaml"},  # 称号的配置表
    {"name": "creatures", "path": "setting/creatures.yaml"},  # 宠物的配置表
    {"name": "account_other_bonus_attributes", "path": "setting/account_other_bonus_attributes.yaml"},  # 其余特色的配置表
]


# 读取配置表
def load_settings(settings=None):
    if settings is None:
        settings = default_settings

    global g_setting
    g_setting = {}

    for setting in settings:
        with open(setting["path"], "r", encoding="utf-8") as setting_file:
            try:
                g_setting[setting["name"]] = yaml.load(setting_file, Loader=yaml.FullLoader)
            except yaml.parser.ParserError as error:
                notify_error(logger, "配置表={}的格式有问题，具体问题请看下面的报错中的line $行数$ column $列数$来定位\n错误信息：{}\n".format(setting["name"], error))
                exit(0)

    logger.info("setting loaded")
    # logger.debug("setting={}".format(g_setting))


def all_settings():
    return g_setting

# 获取配置表setting_name中名称为item_name的条目
def get_setting(setting_name, item_name):
    if g_setting[setting_name] is not None:
        for setting in g_setting[setting_name]:
            if item_name in setting["names"]:
                return setting

    return None


def merge_arrays(arrays):
    merged = []
    for array in arrays:
        merged.extend(array)
    return merged


# 称号列表
def styles():
    return merge_arrays(style["names"] for style in g_setting["styles"])


# 宠物列表
def creatures():
    return merge_arrays(creature["names"] for creature in g_setting["creatures"])
