#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : setting
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import multiprocessing
import numbers
import os
import sys

import yaml
import yaml.parser

from dnf_calc import notify_error, logger
from .const import *

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
        try:
            with open(setting["path"], "r", encoding="utf-8") as setting_file:
                g_setting[setting["name"]] = yaml.load(setting_file, Loader=yaml.FullLoader)
        except FileNotFoundError as error:
            notify_error(logger, "没找到配置表={}，你是否直接在压缩包中打开了？\n错误信息：{}\n".format(setting["name"], error))
            sys.exit(0)
        except UnicodeDecodeError as error:
            notify_error(logger, "配置表={}的编码格式有问题，应为utf-8，如果使用系统自带记事本的话，请下载vscode或notepad++等文本编辑器\n错误信息：{}\n".format(setting["name"], error))
            sys.exit(0)
        except Exception as error:
            notify_error(logger, "配置表={}的格式有问题，具体问题请看下面的报错中的line $行数$ column $列数$来定位\n错误信息：{}\n".format(setting["name"], error))
            sys.exit(0)

    ok, msg = check_settings(g_setting)
    if not ok:
        notify_error(logger, "配置表填写有误：\n{}".format(msg))
        sys.exit(0)

    if multiprocessing.current_process().name == "MainProcess":
        logger.info("setting loaded")
        logger.debug("setting={}".format(g_setting))


class CheckItem:
    def __init__(self, name, valid_list):
        self.name = name
        self.valid_list = valid_list


fixup_check_list = [
    CheckItem("deal_equip_fixup", deal_entry_index_to_name),
    CheckItem("buf_equip_fixup", buf_entry_index_to_name),
    CheckItem("huanzhuang_slot_fixup", buf_entry_index_to_name),
]


def check_settings(setting_map):
    # 检查每一个词条是否都合法
    for setting_name, settings in setting_map.items():
        for setting in settings:
            # 检查基础配置条目
            if "entries" in setting and setting["entries"] is not None:
                for entry in setting["entries"]:
                    ok, msg = check_setting_entry(entry, "entries", entry_name_to_indexes, False)
                    if not ok:
                        return ok, msg

            # 检查装备补正与换装部位补正等
            for check_item in fixup_check_list:
                if check_item.name in setting and setting[check_item.name] is not None:
                    for equip_or_slot_index, entries in setting[check_item.name].items():
                        for entry in entries:
                            ok, msg = check_setting_entry(entry, check_item.name, check_item.valid_list, True)
                            if not ok:
                                return ok, msg

    return True, ""


def check_setting_entry(entry, setting_name, valid_entry_list, need_eval_before_check):
    # 每个词条项需要是一个字典，且只有一个元素，key为词条名，value为词条数值
    if type(entry) is not dict:
        return False, (
            "特色词条应该是一个字典，不应该是{}\n"
            "有问题的词条为：{}\n"
            "注意：词条名与值之间要有空格空开，如A:B不合法，A: B和A:   B都是可以的"
        ).format(type(entry), entry)

    # 检查词条格式
    if len(entry) != 1:
        return False, (
            "特色词条字典只能有一个元素\n"
            "有问题的词条为：{}\n"
            "- A: B # 这样是ok的\n"
            "- A1: B1\n"
            "  A2: B2 # 像这样词条有多个key value是不支持的，请按照其他词条的示例格式来填写"
        ).format(entry)

    # 检查词条内容
    for name, value in entry.items():
        # 检查词条是否在支持的列表集合中
        if need_eval_before_check:
            try:
                index = eval(name)
            except:
                index = -1
            if index not in valid_entry_list:
                return False, (
                    "子配置项{}中的某个词条名不合法，请确定词条【{}】在dnf_calc/const.py中列举的词条名称变量集合中，形如index_buf_xxx, index_deal_xxx\n"
                    "有问题的词条为：{}"
                ).format(setting_name, name, entry)
        else:
            if name not in valid_entry_list:
                return False, (
                    "词条名不合法，请确定词条【{}】在配置文件开头列出的词条集合中\n"
                    "有问题的词条为：{}"
                ).format(name, entry)

        # 检查词条值是否是合法的表达式
        try:
            entry_value = eval(str(value))
            if not isinstance(entry_value, numbers.Number):
                raise TypeError("词条计算值最终结果应该为数字，而不是{}".format(type(entry_value)))
        except Exception as error:
            return False, (
                "词条的值有问题，请检查对应词条\n"
                "出错的词条与其值为：{}: {}\n"
                "注意只能是四则表达式或数字，请仔细检查配置表，确认是否将注释也加到双引号中了\n"
                "具体错误信息如下：\n"
                "{}"
            ).format(name, value, error)

    return True, ""


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


if __name__ == '__main__':
    os.chdir("..")
    load_settings()
