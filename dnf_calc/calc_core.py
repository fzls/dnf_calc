#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File      : calc_core
# DateTime  : 2020/6/7 0007 8:25
# Author    : Chen Ji
# Email     : fzls.zju@gmail.com
# -------------------------------
import copy
import itertools
import random
from math import floor
from typing import List

from .data_struct import CalcStepData, BlessHuanZhuang, BlessHuanZhuangStep
from .equipment import *
from .logic import *
from .parallel_dfs import max_inc_values, calc_equip_value


def process_deal(step: CalcStepData):
    data = step.calc_data

    equips = data.selected_combination
    set_on = get_set_on(equips)

    for wep_num in data.weapon_indexs:
        #################################计算附带各种加成后，当前搭配的各个词条属性#################################

        # 武器、装备列表
        calc_wep = (wep_num,) + tuple(equips)
        # 加上适用的套装属性列表
        for_calc = tuple(set_on) + calc_wep

        # 拷贝一份加上输出职业的国服特色数值后的基础数据
        base_array = data.base_array_with_deal_bonus_attributes.copy()
        # 获取加成后的技攻
        skiper = base_array[index_deal_extra_percent_skill_attack_power]
        # 计算加算词条和乘算词条最终值
        for idx in range(len(for_calc)):
            # 获取装备属性
            cut = data.opt_one.get(for_calc[idx])
            # 加算
            base_array = base_array + cut
            # 乘算部分
            skiper = multiply_entry(skiper, cut[index_deal_extra_percent_skill_attack_power])

        # 为乘算的词条赋最终值
        base_array[index_deal_extra_percent_skill_attack_power] = skiper  # 技能攻击力 +X%

        #################################计算各种特殊条件触发的属性#################################
        fix_base_array_for_equip_or_set_requirement(base_array, equips, set_on)

        #################################核心计算公式#################################

        real_bon = (base_array[index_deal_extra_percent_addtional_damage] +  # 攻击时，附加X%的伤害，也就是白字
                    base_array[index_deal_extra_percent_elemental_damage] *  # 攻击时，附加X%的属性伤害
                    (base_array[index_deal_extra_all_element_strength] * 0.0045 + 1.05))  # 所有属性强化+X
        actlvl = ((base_array[index_deal_extra_active_second_awaken_skill] +  # 二觉主动技能
                   base_array[index_deal_extra_active_skill_lv_1_45] * data.job_lv1 +  # 1_45主动技能
                   base_array[index_deal_extra_active_skill_lv_50] * data.job_lv2 +  # 50主动技能
                   base_array[index_deal_extra_active_skill_lv_60_80] * data.job_lv3 +  # 60_80主动技能
                   base_array[index_deal_extra_active_skill_lv_85] * data.job_lv4 +  # 85主动技能
                   base_array[index_deal_extra_active_skill_lv_95] * data.job_lv5 +  # 95主动技能
                   base_array[index_deal_extra_active_skill_lv_100] * data.job_lv6  # 100主动技能
                   ) / 100 + 1)
        paslvl = (((100 + base_array[index_deal_extra_passive_transfer_skill] * data.job_pas0) / 100) *  # 增加转职被动的等级
                  ((100 + base_array[index_deal_extra_passive_first_awaken_skill] * data.job_pas1) / 100) *  # 增加一绝被动的等级
                  ((100 + base_array[index_deal_extra_passive_second_awaken_skill] * data.job_pas2) / 100) *  # 增加二觉被动的等级
                  ((100 + base_array[index_deal_extra_passive_third_awaken_skill] * data.job_pas3) / 100)  # 增加三觉被动的等级
                  )
        damage = ((base_array[index_deal_extra_percent_attack_damage] / 100 + 1) *  # 攻击时额外增加X%的伤害增加量
                  (base_array[index_deal_extra_percent_crit_damage] / 100 + 1) *  # 暴击时，额外增加X%的伤害增加量
                  (real_bon / 100 + 1) *  # 白字与属强的最终综合值
                  (base_array[index_deal_extra_percent_final_damage] / 100 + 1) *  # 最终伤害+X%
                  (base_array[index_deal_extra_percent_physical_magical_independent_attack_power] / 100 + 1) *  # 物理/魔法/独立攻击力 +X%
                  (base_array[index_deal_extra_percent_strength_and_intelligence] / 100 + 1) *  # 力智+X%
                  (base_array[index_deal_extra_all_element_strength] * 0.0045 + 1.05) *  # 所有属性强化+X
                  (base_array[index_deal_extra_percent_continued_damage] / 100 + 1) *  # 发生持续伤害5秒，伤害量为对敌人造成伤害的X%
                  (skiper / 100 + 1) *  # 技能攻击力 +X%
                  (base_array[index_deal_extra_percent_special_effect] / 100 + 1) *  # 特殊词条，作者为每个特殊词条打了相应的强度百分比分，如一叶障目对忍者一些技能的特殊改变被认为可以强化9%，守护的抉择（歧路鞋）的护石增强词条被认为可以增强21%
                  actlvl * paslvl *  # 主动技能与被动技能的影响
                  ((54500 + 3.31 * base_array[index_deal_strength_and_intelligence]) / 54500) *  # 力智
                  ((4800 + base_array[index_deal_physical_magical_independent_attack_power]) / 4800) *  # 物理/魔法/独立攻击力
                  (1 + data.cool_on * base_array[index_deal_cool_correction] / 100) /  # 冷却矫正系数，每冷却1%，记0.35这个值
                  (1.05 + 0.0045 * int(data.ele_skill)))  # 最后除去逆校正初始属强的影响

        #################################准备排行数据#################################

        base_array[index_deal_extra_percent_addtional_damage] = real_bon
        not_owned_equips = [uwu for uwu in data.upgrade_work_uniforms]
        for equip in data.transfered_equips:
            not_owned_equips.append(equip)

        save_data = [calc_wep, base_array, data.baibianguai, tuple(not_owned_equips)]

        unique_index = random.random()
        data.minheap_queues[0].put((damage, unique_index, copy.deepcopy(save_data)))


def fix_base_array_for_equip_or_set_requirement(base_array, equips, set_on):
    # 吞噬愤怒二件套或三件套
    if "1311" in set_on or "1312" in set_on:
        # 如果拥有吞噬愤怒神话上衣，则疯狂Buff效果会变为1.5倍
        if "11311" in equips:
            base_array[index_deal_extra_percent_attack_speed] += 5
            base_array[index_deal_extra_percent_moving_speed] += 5
    # 水果三件套或五件套
    if "1082" in set_on or "1083" in set_on:
        # 若同时拥有裤子12080和鞋子15080，则额外加成5%移速
        if "12080" in equips and "15080" in equips:
            base_array[index_deal_extra_percent_moving_speed] += 5
    # 坎坷命运: 神话上衣（11301）、上衣（11300）、项链（22300）、辅助装备（31300）
    if "1301" in set_on or "1302" in set_on:
        def giveback_speed():
            # 默认data表中将对应减速效果都应用了，所以这里判断对应条件是否不成立，然后补回来
            # 攻速+1%
            base_array[index_deal_extra_percent_attack_speed] += 1
            # 移速+1%
            base_array[index_deal_extra_percent_moving_speed] += 1
            # 释放速度+1.5%
            # 暂不支持该词条

        # 神话上衣
        if "11301" in equips:
            # 未装备悲痛者项链时
            if "22300" not in equips:
                # 回滚以应用词条：三攻-10%
                base_array[index_deal_extra_percent_physical_magical_independent_attack_power] += 10
                # 回滚以应用词条：攻击时，附加10%的伤害
                base_array[index_deal_extra_percent_addtional_damage] -= 10
            # 未装备悲情者遗物时
            if "31300" not in equips:
                # 回滚以应用词条：三攻-10%
                base_array[index_deal_extra_percent_physical_magical_independent_attack_power] += 10
                # 回滚以应用词条：攻击时，附加10%的伤害
                base_array[index_deal_extra_percent_addtional_damage] -= 10
        # 上衣
        if "11300" in equips:
            # 未装备悲痛者项链时
            if "22300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
            # 未装备悲情者遗物时
            if "31300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
        # 项链
        if "22300" in equips:
            # 未装备地狱边缘上衣时
            if "11300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
            # 未装备悲情者遗物时
            if "31300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
        # 辅助装备
        if "31300" in equips:
            # 未装备地狱边缘上衣时
            if "11300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
            # 未装备悲痛者项链时
            if "22300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
        # 二件套
        if "1301" in set_on or "1302" in set_on:
            # 未装备地狱边缘上衣时
            if "11300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
        # 三件套
        if "1302" in set_on:
            # 未装备地狱边缘上衣时
            if "11300" not in equips:
                # 回滚以应用词条：攻速-1%；移速-1%；释放速度-1.5%
                giveback_speed()
    # 能量的主宰装备，若拥有能量耳环或能量神话耳环
    if '33230' in equips or '33231' in equips:
        # 若不同时拥有能量辅助装备，则减去10%力智加成
        if '31230' not in equips:
            base_array[index_deal_extra_percent_addtional_damage] -= 10
        # 如不同时拥有能量魔法石，则减去40点全属性属强
        if '32230' not in equips:
            base_array[index_deal_extra_all_element_strength] -= 40
    # 特殊处理天命无常套装
    if '15340' in equips or '23340' in equips or '33340' in equips or '33341' in equips:
        # 若只有散件
        if '1341' not in set_on and '1342' not in set_on:
            # 天命鞋子，在两件套时，点数为双数增加40点属强，期望为20，若为散件则减去该属性
            if '15340' in equips:
                base_array[index_deal_extra_all_element_strength] -= 20
            # 天命戒指，在两件套时，点数大于2额外增加12%伤害，期望为10%（ps：原作者给，我觉得应该应该是4/6*12=8%?）
            elif '23340' in equips:  # 天命无常-戒指-命运的捉弄
                base_array[index_deal_extra_percent_attack_damage] -= 10
            # 天命耳环，在两件套时，点数为6时增加30%最终伤害，期望为5%
            elif '33340' in equips:
                base_array[index_deal_extra_percent_final_damage] -= 5  #
            # 天命神话耳环，在两件套时，点数为6时增加30%最终伤害，其中点数为1时重新投色子，期望为6%
            else:
                base_array[index_deal_extra_all_element_strength] -= 4  # ele=4
                base_array[index_deal_extra_percent_attack_damage] -= 2  # damper=2
                base_array[index_deal_extra_percent_final_damage] -= 1  # allper=6
                base_array[index_deal_extra_percent_strength_and_intelligence] -= 1.93  # staper=15
    # 铁匠神话上衣
    if '11111' in equips:
        # 铁匠三件套或铁匠五件套
        if '1112' in set_on or '1113' in set_on:
            base_array[index_deal_cool_correction] += 10
    # 大祭司神话对其他装备的增幅额外+50%
    if "11011" in equips:
        # 下装的天之恩宠为增加20全属性抗性
        if "12010" in equips:
            base_array[index_deal_extra_dark_resistance] += 10
        # 鞋的天之恩宠为增加12%移速
        if "15010" in equips:
            base_array[index_deal_extra_percent_moving_speed] += 6
        # 腰带的天之恩宠为增加12%攻速
        if "14010" in equips:
            base_array[index_deal_extra_percent_attack_speed] += 6
    # 呐喊神话手镯对二件套的加速效果额外增幅一倍
    if "1261" in set_on or "1262" in set_on:
        if "21261" in equips:
            # 额外增加攻速12%
            base_array[index_deal_extra_percent_attack_speed] += 12
            # 额外增加移速12%
            base_array[index_deal_extra_percent_moving_speed] += 12
    ################################大幽魂和军神最后处理，且大幽魂要在前面######################################
    # 大幽魂系列
    # ps：必须在军神之前处理，因为套装效果可能会影响移速
    dr = base_array[index_deal_extra_dark_resistance]  # 当前总暗抗

    def get_delta(dark_resistance, dark_resistance_step, attr_step, attr_max):
        """
        计算当暗抗值为dark_resistance，对于形如【每dark_resistance_step点暗属性抗性，增加attr_step的xxx词条。（最多增加attr_max）】的词条，需要补正（减去）的xxx词条
        @param dark_resistance: 总暗抗
        @param dark_resistance_step: 每多少点暗抗计算一次xxx词条
        @param attr_step: 每次计算多少点xxx词条
        @param attr_max: 最多计算多少点xxx词条
        @return:
        """
        return attr_max - min(dark_resistance // dark_resistance_step * attr_step, attr_max)

    # 深渊上衣11280、深渊神话上衣11281
    if "11280" in equips or "11281" in equips:
        # 每10点暗属性抗性，增加7 % 的最终伤害。（最多增加35 %）
        base_array[index_deal_extra_percent_final_damage] -= get_delta(dr, 10, 7, 35)
    # 深渊项链22280
    if "22280" in equips:
        # 每13点暗属性抗性，增加10%的力量和智力。（最多增加40%）
        base_array[index_deal_extra_percent_strength_and_intelligence] -= get_delta(dr, 13, 10, 40)
    # 深渊辅助装备31280
    if "31280" in equips:
        # 每7点暗属性抗性，增加6%的物理、魔法、独立攻击力。（最多增加42%）
        base_array[index_deal_extra_percent_physical_magical_independent_attack_power] -= get_delta(dr, 7, 6, 42)
    # 深渊2件套1281
    if "1281" in set_on or "1282" in set_on:
        # 每28点暗属性抗性，所有职业lv1~48所有技能Lv+1（特性技能除外；最多叠加2次）
        base_array[index_deal_extra_passive_transfer_skill] -= get_delta(dr, 28, 1, 2)
        base_array[index_deal_extra_passive_first_awaken_skill] -= get_delta(dr, 28, 1, 2)
        base_array[index_deal_extra_active_skill_lv_1_45] -= get_delta(dr, 28, 1, 2)
    # 深渊3件套1282
    if "1282" in set_on:
        # 每30点暗属性抗性，所有职业Lv60~80所有技能Lv +1（特性技能除外，最多叠加2次）
        base_array[index_deal_extra_active_skill_lv_60_80] -= get_delta(dr, 30, 1, 2)
        # 暗属性抗性高于61时，所有职业Lv50、Lv80、Lv100所有技能Lv +1（特性技能除外）
        if dr < 61:
            base_array[index_deal_extra_active_skill_lv_50] -= 1
            base_array[index_deal_extra_active_skill_lv_85] -= 1
            base_array[index_deal_extra_active_skill_lv_100] -= 1
    # 黑魔法下装12240
    if "12240" in equips:
        # 每14点暗属性抗性，攻击时额外增加7%的伤害增加量。（最多增加35%）
        base_array[index_deal_extra_percent_attack_damage] -= get_delta(dr, 14, 7, 35)
    # 黑魔法手镯21240、黑魔法神话手镯21241
    if "21240" in equips or "21241" in equips:
        # 每18点暗属性抗性，增加7%的最终伤害（最多增加28%）
        base_array[index_deal_extra_percent_final_damage] -= get_delta(dr, 18, 7, 28)
        # 每18点暗属性抗性，增加10点所有属性强化（最多增加40点）
        base_array[index_deal_extra_all_element_strength] -= get_delta(dr, 18, 10, 40)
    # 黑魔法魔法石32240
    if "32240" in equips:
        # 每10点暗属性抗性，暴击时额外增加5 % 的伤害增加量。（最多增加35 %）
        base_array[index_deal_extra_percent_crit_damage] -= get_delta(dr, 10, 5, 35)
        # 每10点暗属性抗性，增加1 % 的技能攻击力。（最多增加7 %）
        base_array[index_deal_extra_percent_skill_attack_power] -= get_delta(dr, 10, 1, 7)
    # 黑魔法2件套1241
    if "1241" in set_on or "1242" in set_on:
        # 暗属性抗性高于76时，攻击时额外增加12%的伤害增加量
        if dr < 76:
            base_array[index_deal_extra_percent_attack_damage] -= 12
        # 暗属性抗性高于76时，技能攻击力+10%
        if dr < 76:
            base_array[index_deal_extra_percent_skill_attack_power] -= 10
    # 黑魔法3件套1242
    if "1242" in set_on:
        # 每16点暗属性抗性，增加2%的物理、魔法暴击率。（最多增加10%）
        base_array[index_deal_extra_percent_magic_physical_crit_rate] -= get_delta(dr, 16, 2, 10)
        # 暗属性抗性高于81时，攻击时附加13%的属性伤害。（以自身攻击属性中最高属性伤害为准）
        if dr < 81:
            base_array[index_deal_extra_percent_elemental_damage] -= 13
    # 求道者鞋15320
    if "15320" in equips:
        # 每3点暗属性抗性，增加14点所有属性强化。(最多增加70点)
        base_array[index_deal_extra_all_element_strength] -= get_delta(dr, 3, 14, 70)
        # 暗属性抗性高于16时，所有职业Lv1-100所有技能Lv+1(特性技能除外、Lv95技能除外)
        if dr < 16:
            base_array[index_deal_extra_passive_transfer_skill] -= 1
            base_array[index_deal_extra_passive_first_awaken_skill] -= 1
            base_array[index_deal_extra_passive_second_awaken_skill] -= 1
            base_array[index_deal_extra_active_skill_lv_1_45] -= 1
            base_array[index_deal_extra_active_skill_lv_50] -= 1
            base_array[index_deal_extra_active_skill_lv_60_80] -= 1
            base_array[index_deal_extra_active_skill_lv_85] -= 1
            base_array[index_deal_extra_active_skill_lv_100] -= 1
    # 求道者戒指23320
    if "23320" in equips:
        # 每4点暗属性抗性，暴击时额外增加10%的伤害增加。（最多增加40%）
        base_array[index_deal_extra_percent_crit_damage] -= get_delta(dr, 4, 10, 40)
    # 求道者耳环33320、求道者神话耳环33321
    if "33320" in equips or "33321" in equips:
        # 每3点暗属性抗性，增加7%的最终伤害。（最多增加42%）
        base_array[index_deal_extra_percent_final_damage] -= get_delta(dr, 3, 7, 42)
    # 求道者2件套1321
    if "1321" in set_on or "1322" in set_on:
        # 暗属性抗性高于21点时，增加10%的最终伤害
        if dr < 21:
            base_array[index_deal_extra_percent_final_damage] -= 10
        # 暗属性抗性高于21点时，攻击时附加10%的伤害。
        if dr < 21:
            base_array[index_deal_extra_percent_addtional_damage] -= 10
    # 求道者3件套1322
    if "1322" in set_on:
        # 每7点暗属性抗性，增加4%的技能攻击力。（最多增加16%）
        base_array[index_deal_extra_percent_skill_attack_power] -= get_delta(dr, 7, 4, 16)
        # 每7点暗属性抗性，增加10点所有属性强化。（最大增加40点）
        base_array[index_deal_extra_all_element_strength] -= get_delta(dr, 7, 10, 40)
        # 每9点暗属性抗性，增加5%的攻击速度和移动速度。（最多增加15%）
        base_array[index_deal_extra_percent_attack_speed] -= get_delta(dr, 9, 5, 15)
        base_array[index_deal_extra_percent_moving_speed] -= get_delta(dr, 9, 5, 15)
        # 每13点暗属性抗性，增加10%的施放速度。（最多增加20%）
        # ps: 暂无对应词条
    # 军神系列
    # 拥有军神耳环，且不拥有军神辅助装备
    if "33200" in equips and "31200" not in equips:
        # 减去10%力智加成
        base_array[index_deal_extra_percent_strength_and_intelligence] -= 10
        # 减去10%移速
        base_array[index_deal_extra_percent_moving_speed] -= 10
    # 军神二件套且拥有军神-魔法石-军神的庇护宝石32200，说明遗书31200和古怪耳环33200（心之所念33201）不同时存在，减去5%的爆伤，10%移速，5%攻速
    if "1201" in set_on and "32200" in equips:
        base_array[index_deal_extra_percent_crit_damage] -= 5
        base_array[index_deal_extra_percent_moving_speed] -= 10
        base_array[index_deal_extra_percent_attack_speed] -= 5
    # 如果拥有军神的遗书31200（辅助装备）和军神的古怪耳环33200（非神话）（耳环），则将与神话的二件套差异补正
    if "31200" in equips and "33200" in equips:
        base_array[index_deal_extra_percent_moving_speed] -= 5
        base_array[index_deal_extra_percent_attack_speed] -= 5
    # 军神3件套-根据角色移动速度，获得以下效果。
    # - 40%以下-[0,40%)：力量、智力 +2%
    # - 40%~60%-[40%, 60%)：力量、智力 +4%
    # - 60%~80%-[60%, 80%)：力量、智力 +6%
    # - 80%~100%-[80%, 100%)：力量、智力 +8%
    # - 100%~120%-[100%, 120%)：力量、智力 +10%
    # - 120%以上-[120%, inf)：力量、智力 +10%；攻击速度 +10%；施放速度 +15%
    if "1202" in set_on:
        moving_speed = base_array[index_deal_extra_percent_moving_speed]

        if moving_speed < 120:
            base_array[index_deal_extra_percent_attack_speed] -= 10

        delta = 0
        if moving_speed < 40:
            delta = 10 - 2
        elif 40 <= moving_speed < 60:
            delta = 10 - 4
        elif 60 <= moving_speed < 80:
            delta = 10 - 6
        elif 80 <= moving_speed < 100:
            delta = 10 - 8
        base_array[index_deal_extra_percent_strength_and_intelligence] -= delta


def process_buf(step: CalcStepData):
    data = step.calc_data

    taiyang_equips = data.selected_combination
    bless_huanzhuang_list = [
        BlessHuanZhuang(data.selected_combination, [], None, [], [])
    ]
    if step.calc_data.huan_zhuang.enable:
        bless_huanzhuang_list.extend(get_bless_huanzhuang_equips_list(step))

    for wep_num in data.weapon_indexs:
        #################################计算附带各种加成后，当前搭配的各个词条属性#################################

        # 武器、装备列表
        taiyang_calc_wep = (wep_num,) + tuple(taiyang_equips)
        # 加上适用的套装属性列表
        taiyang_for_calc = tuple(get_set_on(taiyang_equips)) + taiyang_calc_wep

        # 计算太阳装的属性
        _, taiyang_score, taiyang_mianban, _, taiyang_overview, first_awaken_passive_overview, \
        first_awaken_increase_physical_and_mental_strength_or_intelligence, taiyang_final_increase_strength_and_intelligence, _, _ \
            = calc_buf(data, taiyang_for_calc, False)

        not_owned_equips = [uwu for uwu in data.upgrade_work_uniforms]
        for equip in data.transfered_equips:
            not_owned_equips.append(equip)

        for bless_huanzhuang in bless_huanzhuang_list:
            # 武器、装备列表
            bless_calc_wep = (wep_num,) + tuple(bless_huanzhuang.equips)
            # 加上适用的套装属性列表
            bless_for_calc = tuple(get_set_on(bless_huanzhuang.equips)) + bless_calc_wep

            huanzhuang_slot_fixups = []
            # 获取换装槽位配置的槽位补正信息
            for hz in bless_huanzhuang.huanzhuang_equips:
                slot_index = get_slot_index(hz)
                if slot_index in step.calc_data.huanzhuang_slot_fixup:
                    huanzhuang_slot_fixups.append(step.calc_data.huanzhuang_slot_fixup[slot_index])

            # 计算buf装的属性
            bless_score, _, _, bless_overview, _, _, \
            _, _, bless_final_increase_strength_and_intelligence, bless_final_increase_attack_power_average \
                = calc_buf(data, bless_for_calc, True, huanzhuang_slot_fixups)

            # 奶妈/奶萝增加站街预估
            if data.job_name != "(奶系)神思者":
                bless_overview += " 站街面板 = {street_intelligence}".format(
                    street_intelligence=int(taiyang_mianban) - data.const.naima_nailuo_mianban_delta
                )

            #################################准备排行数据#################################
            # 3 综合得分
            total_score = ((15000 + first_awaken_increase_physical_and_mental_strength_or_intelligence + taiyang_final_increase_strength_and_intelligence + bless_final_increase_strength_and_intelligence) / 250 + 1) \
                          * (2650 + bless_final_increase_attack_power_average)

            # 统计数据
            all_score_str = "{}/{}/{}".format(
                int(bless_score / 10),
                int(taiyang_score / 10),
                int(total_score / 10),
            )
            baibianguai = data.baibianguai
            if bless_huanzhuang.baibianguai is not None:
                baibianguai = bless_huanzhuang.baibianguai
            noe = not_owned_equips.copy()
            noe.extend(bless_huanzhuang.upgrade_work_uniforms)
            noe.extend(bless_huanzhuang.transfered)
            total_increase_strength_and_intelligence = taiyang_final_increase_strength_and_intelligence + bless_final_increase_strength_and_intelligence
            total_increase_attack_power_average = bless_final_increase_attack_power_average
            save_data = [taiyang_calc_wep, [bless_overview, taiyang_overview, first_awaken_passive_overview, all_score_str, total_increase_strength_and_intelligence, total_increase_attack_power_average],
                         baibianguai, tuple(noe), bless_huanzhuang.huanzhuang_equips]

            # 加入排序
            unique_index = random.random()
            data.minheap_queues[0].put((bless_score, unique_index, copy.deepcopy(save_data)))
            data.minheap_queues[1].put((taiyang_score, unique_index, copy.deepcopy(save_data)))
            data.minheap_queues[2].put((total_score, unique_index, copy.deepcopy(save_data)))
            data.minheap_queues[3].put((taiyang_mianban, unique_index, copy.deepcopy(save_data)))


def calc_buf(data, for_calc, is_bless, huanzhuang_slot_fixups=None):
    # 拷贝一份加上奶系职业的国服特色数值后的基础数据
    base_array = data.base_array_with_buf_bonus_attributes.copy()
    if is_bless:
        # 如果当前是计算祝福的数值，则将祝福的补正数值叠加到对应属性上
        base_array[index_buf_physical_and_mental_strength] += base_array[index_buf_fixup_bless_physical_and_mental_strength]
        base_array[index_buf_intelligence] += base_array[index_buf_fixup_bless_intelligence]
        base_array[index_buf_bless_lv30] += base_array[index_buf_fixup_bless_skill_lv]

        for hz_slot_fixup in huanzhuang_slot_fixups:
            base_array += hz_slot_fixup

    # 获取一些需要乘算的百分比增益初始值
    bless_extra_percent_strength_and_intelligence = base_array[index_buf_bless_extra_percent_strength_and_intelligence]  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%
    bless_extra_percent_physical_attack_power = base_array[index_buf_bless_extra_percent_physical_attack_power]  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]物理攻击力增加量 +X%
    bless_extra_percent_magical_attack_power = base_array[index_buf_bless_extra_percent_magical_attack_power]  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]魔法攻击力增加量 +X%
    bless_extra_percent_independent_attack_power = base_array[index_buf_bless_extra_percent_independent_attack_power]  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]独立攻击力增加量 +X%
    taiyang_extra_percent_strength_and_intelligence = base_array[index_buf_taiyang_extra_percent_strength_and_intelligence]  # [天启之珠]、[圣光天启]、[开幕！人偶剧场]力量、智力增加量 +X%
    # 计算加算词条和乘算词条最终值
    for idx in range(len(for_calc)):
        # 获取装备属性
        cut = data.opt_buf.get(for_calc[idx])
        if cut is None:
            # note: 奶系职业的智慧产物尚未加入，原作者最新版加入了部分，下次有空补一下
            continue
        # 加算
        base_array = base_array + cut
        # 乘算部分
        bless_extra_percent_strength_and_intelligence = multiply_entry(bless_extra_percent_strength_and_intelligence, cut[index_buf_bless_extra_percent_strength_and_intelligence])
        bless_extra_percent_physical_attack_power = multiply_entry(bless_extra_percent_physical_attack_power, cut[index_buf_bless_extra_percent_physical_attack_power])
        bless_extra_percent_magical_attack_power = multiply_entry(bless_extra_percent_magical_attack_power, cut[index_buf_bless_extra_percent_magical_attack_power])
        bless_extra_percent_independent_attack_power = multiply_entry(bless_extra_percent_independent_attack_power, cut[index_buf_bless_extra_percent_independent_attack_power])
        taiyang_extra_percent_strength_and_intelligence = multiply_entry(taiyang_extra_percent_strength_and_intelligence, cut[index_buf_taiyang_extra_percent_strength_and_intelligence])
    # 为乘算的词条赋最终值
    base_array[index_buf_bless_extra_percent_strength_and_intelligence] = bless_extra_percent_strength_and_intelligence  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]力量、智力增加量 +X%
    base_array[index_buf_bless_extra_percent_physical_attack_power] = bless_extra_percent_physical_attack_power  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]物理攻击力增加量 +X%
    base_array[index_buf_bless_extra_percent_magical_attack_power] = bless_extra_percent_magical_attack_power  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]魔法攻击力增加量 +X%
    base_array[index_buf_bless_extra_percent_independent_attack_power] = bless_extra_percent_independent_attack_power  # [荣誉祝福]、[勇气祝福]、[禁忌诅咒]独立攻击力增加量 +X%
    base_array[index_buf_taiyang_extra_percent_strength_and_intelligence] = taiyang_extra_percent_strength_and_intelligence  # [天启之珠]、[圣光天启]、[开幕！人偶剧场]力量、智力增加量 +X%

    # 保证各个技能的等级不超过上限
    def get_skill_level_data(skill_name, buff_index, base_level=0):
        # 获取该等级的额外附加上限
        max_level = max_skill_level_map[skill_name]

        # 保证等级不超过该上限
        level = int(min(max_level, base_array[buff_index] + base_level))
        return data.opt_buflvl.get(skill_name)[level]

    #################################核心计算公式#################################
    if data.job_name == "(奶系)神思者":
        # 祝福增加的三攻
        bless_increase_attack_power = get_skill_level_data('hol_b_atta', index_buf_bless_lv30)
        # 守护恩赐（15级）和守护徽章（25级）增加的体力、精神数值（祝福）
        passive_lv15_lv25_increase_physical_and_mental_strength_bless = get_skill_level_data('pas0', index_buf_job_passive_lv15, data.base_job_passive_lv15_bless) \
                                                                        + get_skill_level_data('hol_pas0_1', index_buf_naiba_protect_badge_lv25)
        # 守护恩赐（15级）和守护徽章（25级）增加的体力、精神数值（太阳）
        passive_lv15_lv25_increase_physical_and_mental_strength_taiyang = get_skill_level_data('pas0', index_buf_job_passive_lv15, data.base_job_passive_lv15_taiyang) \
                                                                          + get_skill_level_data('hol_pas0_1', index_buf_naiba_protect_badge_lv25)
        # 一觉被动（信念光环）增加的体力、精神数值
        first_awaken_passive_increase_physical_and_mental_strength = get_skill_level_data('hol_pas1', index_buf_first_awaken_passive_lv48)
        # 二觉增加的体力、精神数值
        second_awaken_increase_physical_and_mental_strength = get_skill_level_data('hol_act2', index_buf_second_awaken_lv85)
        # 三觉被动增加的体力、精神数值
        third_awaken_passive_increase_physical_and_mental_strength = get_skill_level_data('pas3', index_buf_third_awaken_passive_lv95)
        # 祝福适用的体力、精神数值
        physical_and_mental_strength_bless = base_array[index_buf_physical_and_mental_strength] + passive_lv15_lv25_increase_physical_and_mental_strength_bless \
                                             + first_awaken_passive_increase_physical_and_mental_strength + second_awaken_increase_physical_and_mental_strength \
                                             + third_awaken_passive_increase_physical_and_mental_strength + 19 * base_array[index_buf_amplification] \
                                             + data.base_stat_custom_bless_data_minus_taiyang_data
        # 太阳适用的体力、精神数值
        physical_and_mental_strength_taiyang = base_array[index_buf_physical_and_mental_strength] + passive_lv15_lv25_increase_physical_and_mental_strength_taiyang \
                                               + first_awaken_passive_increase_physical_and_mental_strength + second_awaken_increase_physical_and_mental_strength \
                                               + third_awaken_passive_increase_physical_and_mental_strength + 19 * base_array[index_buf_amplification]

        physical_and_mental_divisor = data.const.naiba_physical_and_mental_divisor

        # 祝福最终增加的力智
        bless_final_increase_strength_and_intelligence = int(
            int(
                (get_skill_level_data('hol_b_stat', index_buf_bless_lv30) + base_array[index_buf_bless_extra_strength_and_intelligence]) * (bless_extra_percent_strength_and_intelligence / 100 + 1)
            ) * (physical_and_mental_strength_bless / physical_and_mental_divisor + 1)
        )
        # 祝福最终增加的物理攻击力
        bless_final_increase_physical_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_physical_attack_power]) * (bless_extra_percent_physical_attack_power / 100 + 1)
            ) * (physical_and_mental_strength_bless / physical_and_mental_divisor + 1)
        )
        # 祝福最终增加的魔法攻击力
        bless_final_increase_magical_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_magical_attack_power]) * (bless_extra_percent_magical_attack_power / 100 + 1)
            ) * (physical_and_mental_strength_bless / physical_and_mental_divisor + 1)
        )
        # 祝福最终增加的独立攻击力
        bless_final_increase_independent_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_independent_attack_power]) * (bless_extra_percent_independent_attack_power / 100 + 1)
            ) * (physical_and_mental_strength_bless / physical_and_mental_divisor + 1)
        )
        # 祝福最终增加的三攻（平均值）
        bless_final_increase_attack_power_average = int(
            (bless_final_increase_physical_attack_power + bless_final_increase_magical_attack_power + bless_final_increase_independent_attack_power) / 3
        )
        # 太阳最终增加的力智
        taiyang_final_increase_strength_and_intelligence = int(
            int(
                (get_skill_level_data('c_stat', index_buf_taiyang_lv50) + base_array[index_buf_taiyang_extra_strength_and_intelligence]) * (taiyang_extra_percent_strength_and_intelligence / 100 + 1)
            ) * (physical_and_mental_strength_taiyang / 750 + 1)
        )
        # 信念光环增加的体力、精神数值
        belief_halo_increase_physical_and_mental_strength = int(get_skill_level_data('hol_pas1_out', index_buf_first_awaken_passive_lv48) + 213 + base_array[index_buf_belief_halo])
        # 一觉被动概览
        first_awaken_passive_overview = "{increase_intelligence_and_strength}  ({level}级)".format(
            increase_intelligence_and_strength=int(get_skill_level_data('hol_pas1_out', index_buf_first_awaken_passive_lv48) + 213 + base_array[index_buf_belief_halo]),
            level=int(20 + base_array[index_buf_first_awaken_passive_lv48])
        )
        # 祝福概览
        bless_overview = "{increase_intelligence_and_strength}/{increase_attack_power_average}   [{physical_and_mental_strength}({level}级)]".format(
            increase_intelligence_and_strength=bless_final_increase_strength_and_intelligence,
            increase_attack_power_average=bless_final_increase_attack_power_average,
            physical_and_mental_strength=physical_and_mental_strength_bless,
            level=int(base_array[index_buf_bless_lv30]),
        )
        # 太阳适用的面板数值（奶爸为体精、奶妈奶萝为智力）
        physical_and_mental_strength_or_intelligence_taiyang = physical_and_mental_strength_taiyang
        # 一觉被动增加的面板数值（奶爸为体精、奶妈奶萝为智力）
        first_awaken_increase_physical_and_mental_strength_or_intelligence = belief_halo_increase_physical_and_mental_strength

    else:
        intelligence_divisor = 675
        sing_song_increase_rate = 1.25
        if data.job_name == "(奶系)炽天使":
            intelligence_divisor = data.const.naima_intelligence_divisor  # 多少智力折合一级祝福
            sing_song_increase_rate = data.const.naima_sing_song_increase_rate_base + data.const.naima_sing_song_increase_rate_amplification_coef * base_array[index_buf_amplification]  # 唱歌时的倍率
        if data.job_name == "(奶系)冥月女神":
            intelligence_divisor = data.const.nailuo_intelligence_divisor  # 多少智力折合一级祝福
            sing_song_increase_rate = (data.const.nailuo_sing_song_increase_rate_base + data.const.nailuo_sing_song_increase_rate_amplification_coef * base_array[index_buf_amplification]) \
                                      * data.const.nailuo_sing_song_increase_rate_final_coef  # 唱歌时的倍率

        # 祝福增加的三攻
        bless_increase_attack_power = get_skill_level_data('se_b_atta', index_buf_bless_lv30)
        # [启示：圣歌]、[人偶操纵者] 增加的智力数值（祝福）
        passive_lv15_increase_intelligence_bless = get_skill_level_data('pas0', index_buf_job_passive_lv15, data.base_job_passive_lv15_bless)
        # [启示：圣歌]、[人偶操纵者] 增加的智力数值（太阳）
        passive_lv15_increase_intelligence_taiyang = get_skill_level_data('pas0', index_buf_job_passive_lv15, data.base_job_passive_lv15_taiyang)
        # 一觉被动（[虞诚信念]、[少女的爱]）增加的智力数值
        first_awaken_passive_increase_intelligence = get_skill_level_data('se_pas1', index_buf_first_awaken_passive_lv48) + base_array[index_buf_piety_halo_or_girs_love]
        # 二觉被动增加的智力数值
        second_awaken_increase_intelligence = get_skill_level_data('se_pas2', index_buf_second_awaken_passive_lv75)
        # 三觉被动增加的智力数值
        third_awaken_passive_increase_intelligence = get_skill_level_data('pas3', index_buf_third_awaken_passive_lv95)
        # 祝福适用的智力数值
        intelligence_bless = base_array[index_buf_intelligence] + passive_lv15_increase_intelligence_bless \
                             + first_awaken_passive_increase_intelligence + second_awaken_increase_intelligence \
                             + third_awaken_passive_increase_intelligence + data.base_stat_custom_bless_data_minus_taiyang_data
        # 太阳适用的智力数值
        intelligence_taiyang = base_array[index_buf_intelligence] + passive_lv15_increase_intelligence_taiyang \
                               + first_awaken_passive_increase_intelligence + second_awaken_increase_intelligence \
                               + third_awaken_passive_increase_intelligence
        # 祝福最终增加的力智
        bless_final_increase_strength_and_intelligence = int(
            int(
                (get_skill_level_data('se_b_stat', index_buf_bless_lv30) + base_array[index_buf_bless_extra_strength_and_intelligence]) * (bless_extra_percent_strength_and_intelligence / 100 + 1)
            ) * (intelligence_bless / intelligence_divisor + 1) * sing_song_increase_rate
        )
        # 祝福最终增加的物理攻击力
        bless_final_increase_physical_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_physical_attack_power]) * (bless_extra_percent_physical_attack_power / 100 + 1) * (intelligence_bless / intelligence_divisor + 1)
            ) * sing_song_increase_rate
        )
        # 祝福最终增加的魔法攻击力
        bless_final_increase_magical_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_magical_attack_power]) * (bless_extra_percent_magical_attack_power / 100 + 1) * (intelligence_bless / intelligence_divisor + 1)
            ) * sing_song_increase_rate
        )
        # 祝福最终增加的独立攻击力
        bless_final_increase_independent_attack_power = int(
            int(
                (bless_increase_attack_power + base_array[index_buf_bless_extra_independent_attack_power]) * (bless_extra_percent_independent_attack_power / 100 + 1) * (intelligence_bless / intelligence_divisor + 1)
            ) * sing_song_increase_rate
        )
        # 祝福最终增加的三攻（平均值）
        bless_final_increase_attack_power_average = int(
            (bless_final_increase_physical_attack_power + bless_final_increase_magical_attack_power + bless_final_increase_independent_attack_power) / 3
        )
        # 太阳最终增加的力智
        taiyang_final_increase_strength_and_intelligence = int(
            int(
                (get_skill_level_data('c_stat', index_buf_taiyang_lv50) + base_array[index_buf_taiyang_extra_strength_and_intelligence]) * (taiyang_extra_percent_strength_and_intelligence / 100 + 1)
            ) * (intelligence_taiyang / 750 + 1))
        # 虔诚信念或少女的爱增加的智力数值
        piety_halo_or_girs_love_increase_intelligence = int(first_awaken_passive_increase_intelligence + 442)
        # 一觉被动概览
        first_awaken_passive_overview = "{increase_intelligence_and_strength}  ({level}级)".format(
            increase_intelligence_and_strength=int(first_awaken_passive_increase_intelligence + 442),
            level=int(20 + base_array[index_buf_first_awaken_passive_lv48])
        )
        # 祝福概览
        bless_overview = ("{increase_lizhi_with_sing_song}({increase_lizhi})/ {increase_ap_with_sing_song}({increase_ap})\n"
                          "图内={intelligence}({level}级)").format(
            increase_lizhi_with_sing_song=bless_final_increase_strength_and_intelligence,
            increase_lizhi=int(bless_final_increase_strength_and_intelligence / sing_song_increase_rate),
            increase_ap_with_sing_song=bless_final_increase_attack_power_average,
            increase_ap=int(bless_final_increase_attack_power_average / sing_song_increase_rate),
            intelligence=int(intelligence_bless),
            level=int(base_array[index_buf_bless_lv30]),
        )
        # 太阳适用的面板数值（奶爸为体精、奶妈奶萝为智力）
        physical_and_mental_strength_or_intelligence_taiyang = intelligence_taiyang
        # 一觉被动增加的面板数值（奶爸为体精、奶妈奶萝为智力）
        first_awaken_increase_physical_and_mental_strength_or_intelligence = piety_halo_or_girs_love_increase_intelligence
    # 太阳概览
    taiyang_overview = "{increase_intelligence_and_strength} [{physical_and_mental_strength_or_intelligence_taiyang}({level}级)]".format(
        increase_intelligence_and_strength=taiyang_final_increase_strength_and_intelligence,
        physical_and_mental_strength_or_intelligence_taiyang=int(physical_and_mental_strength_or_intelligence_taiyang),
        level=int(base_array[index_buf_taiyang_lv50]),
    )
    # 太阳适用的面板数值
    taiyang_mianban = physical_and_mental_strength_or_intelligence_taiyang
    # 1 祝福得分
    bless_score = ((15000 + bless_final_increase_strength_and_intelligence) / 250 + 1) * (2650 + bless_final_increase_attack_power_average)
    # 2 太阳得分
    taiyang_score = ((15000 + taiyang_final_increase_strength_and_intelligence) / 250 + 1) * 2650

    return bless_score, taiyang_score, taiyang_mianban, bless_overview, taiyang_overview, first_awaken_passive_overview, \
           first_awaken_increase_physical_and_mental_strength_or_intelligence, taiyang_final_increase_strength_and_intelligence, bless_final_increase_strength_and_intelligence, bless_final_increase_attack_power_average


def get_bless_huanzhuang_equips_list(step: CalcStepData):
    bless_huanzhuang_equips_list = []  # type: List[BlessHuanZhuang]

    max_replaced_count = step.calc_data.huan_zhuang.max_replaced_count
    if max_replaced_count == 1:
        for set_code, equips in step.calc_data.selected_set_2_equips_map.items():
            if len(equips) not in [2, 3, 5]:
                # 切装部位仅考虑当前搭配中移除一个部位后会少一个套装词条的部位
                continue
            # 从该三件套中选一件来作为被替换的装备
            for replaced_equip in equips:
                slot_index = get_slot_index(replaced_equip)
                if slot_index in step.calc_data.huan_zhuang.exclude_slot:
                    # 跳过不考虑切装的部位
                    continue
                for target_setcode, target_equips in step.calc_data.selected_set_2_equips_map.items():
                    if target_setcode == set_code:
                        # 过滤掉替换的套装
                        continue
                    if len(target_equips) not in [1, 2, 4]:
                        # 替换进来的装备仅考虑增加一个部位后会多一个套装磁条的部位，与之前所减少的一个词条抵消
                        continue

                    # 目标装备为神话，且来源只能是已拥有装备
                    target_equip_god = "{}{}1".format(slot_index, target_setcode)
                    if target_setcode in step.owned_set_2_equips_map and target_equip_god in step.owned_set_2_equips_map[target_setcode]:
                        # 已拥有神话装备
                        replaced_is_god = is_god(replaced_equip)
                        if not replaced_is_god or step.calc_data.huan_zhuang.include_manual_huanzhuang:
                            # 若换入的装备为神话，此时只考虑两种情况
                            # 1. 被替换的部位不是神话
                            # 2. 被替换的部位是神话，且配置允许祝福和太阳装各有一个不同的神话
                            huanzhuang_equips = list_replace(step.calc_data.selected_combination.copy(), replaced_equip, target_equip_god)
                            bless_huanzhuang_equips_list.append(BlessHuanZhuang(huanzhuang_equips, [target_equip_god], None, [], []))

                    # 确认是否可以获取替换进来的套装Y的该部位普通目标装备，来源包括：已拥有装备、百变怪（若其余部位未使用百变怪或当前部位为百变怪）、升级工作服、跨界
                    target_equip_normal = "{}{}0".format(slot_index, target_setcode)
                    if is_valid_buf_equips(target_equip_normal, step):
                        if target_setcode in step.owned_set_2_equips_map and target_equip_normal in step.owned_set_2_equips_map[target_setcode]:
                            # 已拥有普通装备
                            huanzhuang_equips = list_replace(step.calc_data.selected_combination.copy(), replaced_equip, target_equip_normal)
                            bless_huanzhuang_equips_list.append(BlessHuanZhuang(huanzhuang_equips, [target_equip_normal], None, [], []))
                        else:
                            # 未拥有的普通装备
                            if step.has_baibianguai and step.calc_data.baibianguai is None and can_convert_from_baibianguai(target_equip_normal):
                                # 百变怪（若其余部位未使用百变怪），且目标部位可以用百变怪转换
                                huanzhuang_equips = list_replace(step.calc_data.selected_combination.copy(), replaced_equip, target_equip_normal)
                                bless_huanzhuang_equips_list.append(BlessHuanZhuang(huanzhuang_equips, [target_equip_normal], target_equip_normal, [], []))
                            elif target_equip_normal in work_uniforms and len(step.calc_data.upgrade_work_uniforms) < step.can_upgrade_work_unifrom_nums:
                                # 升级工作服：若目标部位是工作服，且目前仍有可以升级的名额
                                huanzhuang_equips = list_replace(step.calc_data.selected_combination.copy(), replaced_equip, target_equip_normal)
                                bless_huanzhuang_equips_list.append(BlessHuanZhuang(huanzhuang_equips, [target_equip_normal], None, [target_equip_normal], []))
                                pass
                            else:
                                current_index = step.calc_data.selected_combination.index(replaced_equip)
                                if target_equip_normal in step.transfer_slots_equips[current_index] and len(step.calc_data.transfered_equips) < step.transfer_max_count:
                                    # 跨界：如果目标装备在对应部位的可跨界装备列表中，且目前仍有可以跨界的名额
                                    huanzhuang_equips = list_replace(step.calc_data.selected_combination.copy(), replaced_equip, target_equip_normal)
                                    bless_huanzhuang_equips_list.append(BlessHuanZhuang(huanzhuang_equips, [target_equip_normal], None, [], [target_equip_normal]))
    else:
        # 考虑每一个元素数目不超过配置的最大切装数目的非空子集
        for replaced_slots in subset(range(len(step.calc_data.selected_combination)), 1, max_replaced_count):
            replaced_equips = [step.calc_data.selected_combination[slot] for slot in replaced_slots]

            # 跳过不考虑切装的部位
            ignored = False
            for replaced_equip in replaced_equips:
                slot_index = get_slot_index(replaced_equip)
                if slot_index in step.calc_data.huan_zhuang.exclude_slot:
                    ignored = True
                    break
            if ignored:
                continue

            # 确认切换进来的部位
            init_step = BlessHuanZhuangStep()
            # 确认非切装部位是否有神话
            if not step.has_god:
                init_step.has_god = False
            else:
                # 太阳装有神话
                if step.calc_data.huan_zhuang.include_manual_huanzhuang:
                    # 考虑进手动切装，也就是允许太阳装和祝福装有不同的神话
                    replaced_has_god = False
                    for replaced_equip in replaced_equips:
                        if is_god(replaced_equip):
                            replaced_has_god = True
                            break
                    if replaced_has_god:
                        init_step.has_god = False
                    else:
                        init_step.has_god = True
                else:
                    # 不允许手动切装，因为此时太阳装已有神话，所以不允许祝福装替换部位换入不同的神话
                    init_step.has_god = True
            dfs_huanzhuang(init_step, replaced_slots, BlessHuanZhuang(step.calc_data.selected_combination.copy(), [], None, [], []), step, bless_huanzhuang_equips_list)

    return bless_huanzhuang_equips_list


def dfs_huanzhuang(huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list):
    current_index = replaced_slots[huanzhuang_step.current_index]
    current_selected_equip = step.calc_data.selected_combination[current_index]

    # 考虑当前部位的每一件可选装备
    for equip in step.items[current_index]:
        try_equip(equip, huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list)

    # 当拥有百变怪，且目前的尝试序列尚未使用到百变怪的时候考虑使用百变怪充当当前部位
    if step.has_baibianguai and step.calc_data.baibianguai is None and bless_huanzhuang.baibianguai is None:
        for equip in step.not_select_items[current_index]:
            bless_huanzhuang.baibianguai = equip
            try_equip(equip, huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list)
            bless_huanzhuang.baibianguai = None

    # 若当前部位的工作服尚未拥有，且可升级工作服的次数尚未用完，则尝试本部位升级工作服
    if not step.has_uniforms[current_index] and len(step.calc_data.upgrade_work_uniforms) < step.can_upgrade_work_unifrom_nums:
        work_uniform = step.work_uniforms_items[current_index]

        bless_huanzhuang.upgrade_work_uniforms.append(work_uniform)
        try_equip(work_uniform, huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list)
        bless_huanzhuang.upgrade_work_uniforms.pop()

    # 当当前部位有可以从选定账号跨界的装备，且已跨界数目未超过设定上限，则考虑跨界该部位的装备
    if len(step.transfer_slots_equips[current_index]) != 0 and len(step.calc_data.transfered_equips) + len(bless_huanzhuang.transfered) < step.transfer_max_count:
        for equip_to_transfer in step.transfer_slots_equips[current_index]:
            bless_huanzhuang.transfered.append(equip_to_transfer)
            try_equip(equip_to_transfer, huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list)
            bless_huanzhuang.transfered.pop()


def try_equip(equip, huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list):
    current_index = huanzhuang_step.current_index
    current_slot_index = replaced_slots[huanzhuang_step.current_index]
    current_selected_equip = step.calc_data.selected_combination[current_slot_index]
    if equip == current_selected_equip:
        return

    # 剪枝条件1：若当前切装序列已经有神话装备（god），且当前这个部位遍历到的仍是一个神话装备，则可以直接跳过
    if huanzhuang_step.has_god and is_god(equip):
        return

    # 保存回溯状态
    old_equip = bless_huanzhuang.equips[current_slot_index]
    has_god = huanzhuang_step.has_god

    # 更新搜索状态
    bless_huanzhuang.equips[current_slot_index] = equip
    bless_huanzhuang.huanzhuang_equips.append(equip)
    huanzhuang_step.current_index += 1
    huanzhuang_step.has_god = huanzhuang_step.has_god or is_god(equip)

    if current_index < len(replaced_slots) - 1:
        # 未到最后一层，继续迭代

        # 剪枝条件2：预计算出后面切装备部位能够获得的最大价值量，若当前已有价值量与之相加低于已处理的最高价值量，则剪枝
        pruned = False
        if not step.dont_pruning:
            ub = upper_bound(huanzhuang_step, replaced_slots, bless_huanzhuang, step.prefer_god, step.last_god_slot)
            if ub < step.local_max_setop - step.set_perfect - step.prune_cfg.delta_between_lower_bound_and_max:
                # 如果比缓存的历史最高词条数少，则剪枝
                pruned = True
            else:
                if step.local_max_setop < step.max_possiable_setopt:
                    # 否则尝试更新最新值，再判断一次
                    step.local_max_setop = step.max_setopt.value
                    if ub < step.local_max_setop - step.set_perfect - step.prune_cfg.delta_between_lower_bound_and_max:
                        pruned = True

        if not pruned:
            dfs_huanzhuang(huanzhuang_step, replaced_slots, bless_huanzhuang, step, bless_huanzhuang_equips_list)
    else:
        # 最后一层，即形成了一个切装方案
        if not step.dont_pruning:
            # 检查是否有神话装备
            god = 0
            if step.prefer_god and (has_god or is_god(equip)):
                god = 1
            # 计算套装数目
            set_list = ["1" + str(get_set_name(bless_huanzhuang.equips[x])) for x in range(0, 11)]
            set_val = Counter(set_list)
            del set_val['136', '137', '138']
            # 套装词条数：1件价值量=0，两件=1，三件、四件=2，五件=3，神话额外增加1价值量
            setopt_num = sum([floor(x * 0.7) for x in set_val.values()]) + god

            # 仅当当前搭配的词条数不低于历史最高值时才视为有效搭配
            if setopt_num >= step.local_max_setop - step.set_perfect - step.prune_cfg.delta_between_lower_bound_and_max:
                # 尝试获取全局历史最高词条数
                if step.local_max_setop < step.max_possiable_setopt:
                    step.local_max_setop = step.max_setopt.value
                # 二次对比
                if setopt_num >= step.local_max_setop - step.set_perfect - step.prune_cfg.delta_between_lower_bound_and_max:
                    # 尝试更新全局最高词条数和本进程缓存的历史最高词条数
                    if step.local_max_setop <= setopt_num - god * step.set_perfect:
                        max_setopt = setopt_num - god * step.set_perfect
                        step.max_setopt.value = max_setopt
                        step.local_max_setop = max_setopt

                    # 加入到换装集合中
                    bless_huanzhuang_equips_list.append(copy.deepcopy(bless_huanzhuang))
        else:
            # 不进行任何剪枝操作，切装对比的标准是最终计算出的伤害与奶量倍率
            bless_huanzhuang_equips_list.append(copy.deepcopy(bless_huanzhuang))

    huanzhuang_step.has_god = has_god
    huanzhuang_step.current_index -= 1
    bless_huanzhuang.huanzhuang_equips.pop()
    bless_huanzhuang.equips[current_slot_index] = old_equip


def upper_bound(huanzhuang_step, replaced_slots, bless_huanzhuang, prefer_god, last_god_slot):
    # 计算至今为止已有的价值量
    selected_combination = bless_huanzhuang.huanzhuang_equips.copy()
    for slot, equip in enumerate(bless_huanzhuang.equips):
        # 加入非切装部位
        if slot not in replaced_slots:
            selected_combination.append(equip)

    current_value = calc_equip_value(selected_combination, huanzhuang_step.has_god, prefer_god)
    # 后续按最大价值量计算，即每个槽位按能产生一个套装词条数计算
    remaining_max_value = max_inc_values[len(replaced_slots) - huanzhuang_step.current_index]
    # 获取神话的词条
    god_value = 0
    if prefer_god:
        if huanzhuang_step.has_god:
            god_value = 1
        else:
            for slot in replaced_slots[huanzhuang_step.current_index:]:
                if slot <= last_god_slot:
                    god_value = 1
                    break

    return current_value + remaining_max_value + god_value


def list_replace(l: list, old, new):
    l[l.index(old)] = new
    return l


def is_valid_buf_equips(equip, step: CalcStepData):
    return equip in step.calc_data.opt_buf


def subset(iterable, min_elements, max_elements):
    """
    subset([1,2,3], 0, 2) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3)
    """
    xs = list(iterable)
    min_elements = max(min_elements, 0)
    max_elements = min(max_elements, len(iterable))
    # note we return an iterator rather than a list
    return itertools.chain.from_iterable(itertools.combinations(xs, n) for n in range(min_elements, max_elements + 1))
