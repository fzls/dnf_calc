#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : equipment
# Date   : 2020/6/7 0007
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import collections
from collections import Counter
from math import floor

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
    set_code = int(get_set_name(equip))
    # 百变怪只能转化为1-35的套装内的装备
    if set_code > 35:
        return False
    # 百变怪不能转化为智慧产物
    if len(equip) == 8:
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


##装备
# 11 上衣  12 裤子   13 头肩 14 腰带 15 鞋子
# 21 手镯  22 项链   23 戒指
# 31 辅助装备 32 魔法石 33 耳环
def get_slot_index(equip):
    # eg. 31290	圣者-辅助装备中31表示该装备属于部位31=辅助装备
    return equip[0:2]


def get_set_name(equip):
    # eg. 31290	圣者-辅助装备中29表示该装备属于套装29=圣者
    return equip[2:4]


# 装备编号的最后一位表示是否是神话装备，eg：33341
def is_god(equip):
    return int(equip[-1]) == 1


not_set_list=['136','137','138','144','145','146','147','148','149']


def get_set_on(equips):
    """
    计算各个套装的装备数目
    @param equips: 装备搭配列表
    @type equips: list[str]
    @return: 形成的套装数目列表
    """
    set_on = []

    set_counter = Counter(["1" + str(get_set_name(equips[x])) for x in range(0, 11)])
    for set_code, cnt in set_counter.items():
        if cnt >1:
            set_on.append(set_code + str(floor(cnt*0.7)))
        if set_code == "141" and ('21390340' in equips or '31390540' in equips):
            set_on.append('1401')

    return set_on


# 计数器排序规则：次数多的在前面，同等次数下，套装序号小的放前面
def sort_counter_key(counter_item):
    return -counter_item[1], int(counter_item[0])


def get_readable_names(equip_index_to_realname, weapon, equips, huanzhuang_equips=[]):
    readable_names = []
    readable_names.append(equip_index_to_realname[weapon])

    # 智慧产物以外的套装信息
    set_list = ["1" + str(get_set_name(equips[x])) for x in range(0, 11) if get_set_name(equips[x]) not in not_set_list]
    for set_index, count in sorted(collections.Counter(set_list).most_common(), key=sort_counter_key):
        readable_names.append("{}-{}".format(equip_index_to_realname[set_index], count))

    # 智慧产物单独列出
    wisdom_indexs = [equips[x] for x in range(0, 11) if len(equips[x]) == 8]
    # 赤鬼的次元石改造五阶段词条：装备[青面修罗的面具]、[噙毒手套]中1种以上时，释放疯魔索伦之力。 - 攻击时，附加7%的伤害。
    if wisdom_indexs.count('32390650') == 1:
        if wisdom_indexs.count('21390340'):
            readable_names.append(equip_index_to_realname["1401"])
            wisdom_indexs.remove('32390650')
            wisdom_indexs.remove('21390340')
        elif wisdom_indexs.count('31390540') == 1:
            readable_names.append(equip_index_to_realname["1401"])
            wisdom_indexs.remove('32390650')
            wisdom_indexs.remove('31390540')
    for wisdom_index in wisdom_indexs:
        readable_names.append(equip_index_to_realname[wisdom_index])

    if len(huanzhuang_equips) != 0:
        readable_names.append("(之后为祝福切装)")
        for hz in huanzhuang_equips:
            readable_names.append(equip_index_to_realname[hz])

    return readable_names


# equip_indexes的顺序与上面的搜索顺序一致，这里需要调回来
def get_slot_names(equip_index_to_realname, equip_indexes):
    ordered_equip_indexes = list(equip_indexes)
    reverse_modify_slots_order_(ordered_equip_indexes)

    return [equip_index_to_realname[index] for index in ordered_equip_indexes]


# 根据各个槽位的装备编码列表获得各个槽位的装备编码与名称列表，方便查bug
# ex: [["11111", "11110"]] => [[("11111", "铁匠神话上衣"), ("11110", "铁匠上衣")]]
def get_equip_slots_with_name(equip_index_to_realname, items):
    res = []
    for slot_equip_indexs in items:
        res.append(tuple((equip_index, equip_index_to_realname[equip_index]) for equip_index in slot_equip_indexs))

    return res
