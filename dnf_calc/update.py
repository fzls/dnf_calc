#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : update
# Date   : 2020/6/7 0007
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

import random
import re
import tkinter.messagebox
import webbrowser
from datetime import datetime

import requests

from dnf_calc import config, logger
from .version import *


# 3.2.2 => [3, 2, 2]
def version_to_version_int_list(version):
    return [int(subv) for subv in version.split('.')]


# [3, 2, 2] => 3.2.2
def version_int_list_to_version(version_int_list):
    return '.'.join([str(subv) for subv in version_int_list])


# 获取最新版本号与下载网盘地址
def get_latest_version_and_netdisk_link_passcode():
    # 获取github本项目的readme页面内容
    readme_html_text = requests.get(config().readme_page).text
    # 从更新日志中提取所有版本信息
    versions = re.findall("(?<=[vV])[0-9.]+(?=\s+\d+\.\d+\.\d+)", readme_html_text)
    # 找出其中最新的那个版本号
    latest_version = version_int_list_to_version(max(version_to_version_int_list(ver) for ver in versions))

    # 从readme中提取最新网盘信息
    netdisk_address_matches = re.findall('链接: <a[\s\S]+?rel="nofollow">(?P<link>.+?)<\/a> 提取码: (?P<passcode>[a-zA-Z0-9]+)', readme_html_text, re.MULTILINE)
    # 先选取首个网盘链接作为默认值
    netdisk_link = netdisk_address_matches[0][0]
    netdisk_passcode = netdisk_address_matches[0][1]
    # 然后随机从仍有效的网盘链接中随机一个作为最终结果
    random.seed(datetime.now())
    random.shuffle(netdisk_address_matches)
    for match in netdisk_address_matches:
        if not is_shared_content_blocked(match[0]):
            netdisk_link = match[0]
            netdisk_passcode = match[1]
            break

    logger.info("netdisk_address_matches={}, selected=({}, {})".format(netdisk_address_matches, netdisk_link, netdisk_passcode))

    return latest_version, netdisk_link, netdisk_passcode


# 是否需要更新
def need_update(current_version, latest_version):
    return version_to_version_int_list(current_version) < version_to_version_int_list(latest_version)


# 访问网盘地址，确认分享是否被系统干掉了- -
def is_shared_content_blocked(share_netdisk_addr: str) -> bool:
    # 切换蓝奏云，暂时应该不会被屏蔽了- -
    return False


# 启动时检查是否有更新
def check_update_on_start():
    try:
        if not config().check_update_on_start:
            logger.warning("启动时检查更新被禁用，若需启用请在config.toml中设置")
            return

        latest_version, netdisk_link, netdisk_passcode = get_latest_version_and_netdisk_link_passcode()
        if need_update(now_version, latest_version):
            logger.info("当前版本为{}，已有最新版本{}".format(now_version, latest_version))
            ask_update = tkinter.messagebox.askquestion('更新', "当前版本为{}，已有最新版本{}. 你需要更新吗?".format(now_version, latest_version))
            if ask_update == 'yes':
                if not is_shared_content_blocked(netdisk_link):
                    webbrowser.open(netdisk_link)
                    tkinter.messagebox.showinfo("蓝奏云网盘提取码", "蓝奏云网盘提取码为： {}".format(netdisk_passcode))
                else:
                    # 如果分享的网盘链接被系统屏蔽了，写日志并弹窗提示
                    logger.warning("网盘链接={}又被系统干掉了=-=".format(netdisk_link))
                    webbrowser.open("https://github.com/fzls/dnf_calc/releases")
                    tkinter.messagebox.showerror("不好啦", (
                        "分享的网盘地址好像又被系统给抽掉了呢=。=先暂时使用github的release页面下载吧0-0\n"
                        "请稍作等待~ 风之凌殇看到这个报错后会尽快更新网盘链接的呢\n"
                        "届时再启动程序将自动获取到最新的网盘地址呢~"
                    ))
            else:
                tkinter.messagebox.showinfo("取消启动时自动检查更新方法", "如果想停留在当前版本，不想每次启动都弹出前面这个提醒更新的框框，可以前往config.toml，将check_update_on_start的值设为false即可")
        else:
            logger.info("当前版本{}已是最新版本，无需更新".format(now_version))
    except Exception as err:
        logger.error("更新版本失败, 错误为{}".format(err))
