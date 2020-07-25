#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : ui_const
# Date   : 2020/5/24 0024
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
from dnf_calc import from_rgb

# 目前可升级的工作服数目
txt_can_upgrade_work_unifrom_nums = [
    '材料够升级零件', '材料够升级一件', '材料够升级两件', '材料够升级三件', '材料够升级四件', '材料够升级五件',
    '材料够升级六件', '材料够升级七件', '材料够升级八件', '材料够升级九件', '材料够升级十件', '材料够升级十一件',
]
# 预先将升级工作服数目的字符串与对应数目映射
can_upgrade_work_unifrom_nums_str_2_int = {}
for idx, txt in enumerate(txt_can_upgrade_work_unifrom_nums):
    can_upgrade_work_unifrom_nums_str_2_int[txt] = idx

# 目前最多可跨界的装备数目
txt_can_transfer_nums = [
    '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', '10', '11',
]
# 预先将目前最多可跨界的装备数目与对应数目映射
can_transfer_nums_str_2_int = {}
for idx, txt in enumerate(txt_can_transfer_nums):
    can_transfer_nums_str_2_int[txt] = idx

# 是否默认将普雷传说加入备选
txt_not_use_pulei_legend_by_default = "不加入备选池"
txt_use_pulei_legend_by_default = "加入备选池"

speed_quick = '快速'
speed_middle = '中速'
speed_middle_not_prefer_god = '中速(不偏好神话)'
speed_slow = '慢速'
speed_super_slow = '超慢速'

speeds = [
    speed_quick,
    speed_middle,
    speed_middle_not_prefer_god,
    speed_slow,
    speed_super_slow
]
