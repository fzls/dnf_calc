#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : equipment
# Date   : 2020/6/7 0007
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
from .const import *


def modify_slots_order(items, not_select_items, work_uniforms_items, transfer_slots_equips):
    # 所有已选装备
    modify_slots_order_(items)
    # 百变怪的各部位可选装备需要与上面的部位顺序一致
    modify_slots_order_(not_select_items)
    # 可升级得到的各部位工作服
    modify_slots_order_(work_uniforms_items)
    # 跨界的备选装备
    modify_slots_order_(transfer_slots_equips)


def modify_slots_order_(slots):
    # 默认槽位顺序为11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33
    # 这种情况下，神话分布在第一位、第六位、第十一位，由于不能同时搭配两个神话，会导致额外多计算很多搭配
    # hack: 优化：由于装备顺序不影响最终计算结果，所以把神话装备先放到前面，那么剪枝可以更高效
    #   所有已选装备、百变怪各部位可选装备、各部位工作服的顺序需要一致，比如第一个是鞋、头肩、腰带，则其余俩也要是这个顺序

    slots[0], slots[1], slots[2], slots[3], slots[4], slots[5], slots[6], slots[7], slots[8], slots[9], slots[10] = \
        slots[0], slots[5], slots[10], slots[1], slots[2], slots[3], slots[4], slots[6], slots[7], slots[8], slots[9]


def reverse_modify_slots_order_(slots):
    # 上面的_modify_slots_order的逆操作，调整后会变回默认顺序11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33
    slots[0], slots[5], slots[10], slots[1], slots[2], slots[3], slots[4], slots[6], slots[7], slots[8], slots[9] = \
        slots[0], slots[1], slots[2], slots[3], slots[4], slots[5], slots[6], slots[7], slots[8], slots[9], slots[10]


weapon_rules = [
    {
        "job_names": [
            "(奶系)神思者",
            "(奶系)炽天使",
        ],
        "valid_weapons": [
            "111001",  # 夜语黑瞳
            "111043",  # 十字架-圣者的慈悲
            "111044",  # 十字架-闪耀的神威
        ],
    },

    {
        "job_names": [
            "(奶系)冥月女神",
        ],
        "valid_weapons": [
            "111001",  # 夜语黑瞳
            "111041",  # 扫把-世界树之精灵
            "111042",  # 扫把-纯白的祈祷
        ],
    },
    # 其他职业的暂时没空加，有兴趣的可以自行添加
]


# is_shuchu_job = job_name not in ["(奶系)神思者", "(奶系)炽天使", "(奶系)冥月女神"]
def check_weapons(job_name, weapon_indexs):
    for rule in weapon_rules:
        if job_name in rule["job_names"]:
            for weapon in weapon_indexs:
                if weapon not in rule["valid_weapons"]:
                    return False

    return True


# 获取最后一个拥有神话的装备槽位的下标，以计算时的装备槽位顺序为准。若未找到，则返回-1。在搜索时，判断后续是否可能出现神话装备，可以通过判断下标是否小于等于该值
def get_last_god_slot(items):
    for slot in range(10, -1, -1):
        for equip in items[slot]:
            if is_god(equip):
                return slot

    return -1


# 百变怪是否可以转换成该装备
def can_convert_from_baibianguai(equip):
    # 百变怪不能转换为神话装备
    if is_god(equip):
        return False
    # 百变怪不能转化为工作服
    if equip in work_uniforms:
        return False
    # 百变怪不能转化为智慧产物
    if equip in the_product_of_wisdoms:
        return False
    # 百变怪不能转化为传说、普雷
    if is_legend(equip) or is_pulei(equip):
        return False

    return True


# 36套装为传说
def is_legend(equip):
    return get_set_name(equip) == "36"


# 37为普雷首饰，38为普雷特殊
def is_pulei(equip):
    return get_set_name(equip) in ["37", "38"]


def get_set_name(equip):
    # eg. 31290	圣者-辅助装备中29表示该装备属于套装29=圣者
    return equip[2:4]


# 装备编号的最后一位表示是否是神话装备，eg：33341
def is_god(equip):
    return int(equip[-1]) == 1
