#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : parallel_dfs
# Date   : 2020/6/7 0007
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import copy
from collections import Counter
from math import floor

from dnf_calc import CalcStepData, is_god, get_set_name


# 带剪枝的dfs搜索装备搭配过程
def parallel_dfs(step: CalcStepData):
    """
    背景，假设当前处理到下标n（0-10）的装备，前面装备已选择的组合为selected_combination(of size n)，未处理装备为后面11-n-1个，其对应组合数为rcp=len(Cartesian Product(后面11-n-1个装备部位))

    @param step: 搜索过程的状态
    """
    # 考虑当前部位的每一件可选装备
    for equip in step.items[step.current_index]:
        try_equip(step, equip)

    # 当拥有百变怪，且目前的尝试序列尚未使用到百变怪的时候考虑使用百变怪充当当前部位
    if step.has_baibianguai and step.calc_data.baibianguai is None:
        for equip in step.not_select_items[step.current_index]:
            step.calc_data.baibianguai = equip
            try_equip(step, equip)
            step.calc_data.baibianguai = None

    # 若当前部位的工作服尚未拥有，且可升级工作服的次数尚未用完，则尝试本部位升级工作服
    if not step.has_uniforms[step.current_index] and len(step.calc_data.upgrade_work_uniforms) < step.can_upgrade_work_unifrom_nums:
        work_uniform = step.work_uniforms_items[step.current_index]

        step.calc_data.upgrade_work_uniforms.append(work_uniform)
        try_equip(step, work_uniform)
        step.calc_data.upgrade_work_uniforms.pop()

    # 当当前部位有可以从选定账号跨界的装备，且已跨界数目未超过设定上限，则考虑跨界该部位的装备
    if len(step.transfer_slots_equips[step.current_index]) != 0 and len(step.calc_data.transfered_equips) < step.transfer_max_count:
        for equip_to_transfer in step.transfer_slots_equips[step.current_index]:
            step.calc_data.transfered_equips.append(equip_to_transfer)
            try_equip(step, equip_to_transfer)
            step.calc_data.transfered_equips.pop()


def copy_step(step: CalcStepData) -> CalcStepData:
    """
    用于在进行并发计算时对搜索状态中的引用类型数据进行深拷贝
    @param step: 要复制的搜索状态
    @return: 一份拷贝的搜索状态，其中一些引用类型数据将被深拷贝，跨进程队列、变量等将维持引用
    """
    copied_step = copy.copy(step)

    copied_step.items = copy.deepcopy(step.items)
    copied_step.not_select_items = copy.deepcopy(step.not_select_items)
    copied_step.has_uniforms = copy.deepcopy(step.has_uniforms)
    copied_step.work_uniforms_items = copy.deepcopy(step.work_uniforms_items)
    copied_step.transfer_slots_equips = copy.deepcopy(step.transfer_slots_equips)
    copied_step.owned_set_2_equips_map = copy.deepcopy(step.owned_set_2_equips_map)

    data = step.calc_data

    copied_data = copy.copy(data)
    copied_data.selected_combination = copy.deepcopy(data.selected_combination)
    copied_data.upgrade_work_uniforms = copy.deepcopy(data.upgrade_work_uniforms)
    copied_data.transfered_equips = copy.deepcopy(data.transfered_equips)
    copied_data.selected_set_2_equips_map = copy.deepcopy(data.selected_set_2_equips_map)
    copied_data.weapon_indexs = copy.deepcopy(data.weapon_indexs)
    copied_data.base_array_with_deal_bonus_attributes = data.base_array_with_deal_bonus_attributes.copy()
    copied_data.opt_one = copy.deepcopy(data.opt_one)
    copied_data.base_array_with_buf_bonus_attributes = data.base_array_with_buf_bonus_attributes.copy()
    copied_data.const = copy.deepcopy(data.const)
    copied_data.opt_buf = copy.deepcopy(data.opt_buf)
    copied_data.opt_buflvl = copy.deepcopy(data.opt_buflvl)
    copied_data.exclude_buf_huanzhuang_slot = copy.deepcopy(data.exclude_buf_huanzhuang_slot)

    copied_step.calc_data = copied_data

    return copied_step


def try_equip(step: CalcStepData, equip):
    # 剪枝条件1：若当前组合序列已经有神话装备（god），且当前这个部位遍历到的仍是一个神话装备，则可以直接跳过
    if step.has_god and is_god(equip):
        return

    # 保存回溯状态
    current_index = step.current_index
    has_god = step.has_god

    set_name = get_set_name(equip)
    if set_name not in step.calc_data.selected_set_2_equips_map:
        step.calc_data.selected_set_2_equips_map[set_name] = set()

    # 更新搜索状态
    step.calc_data.selected_combination.append(equip)
    step.calc_data.selected_set_2_equips_map[set_name].add(equip)
    step.current_index += 1
    step.has_god = step.has_god or is_god(equip)

    if current_index < len(step.items) - 1:
        # 未到最后一层，继续迭代

        # 剪枝条件2：预计算出后面装备部位能够获得的最大价值量，若当前已有价值量与之相加低于已处理的最高价值量，则剪枝
        pruned = False
        if not step.dont_pruning:
            ub = upper_bound(step.items, step.calc_data.selected_combination, has_god or is_god(equip), current_index + 1, step.prefer_god, step.last_god_slot)
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
            if current_index != step.start_parallel_computing_at_depth_n:
                # 未到开始进行并发计算的层数，串行搜索
                parallel_dfs(step)
            else:
                # 此层数的所有子树采用并行搜索
                step.producer(copy_step(step))
    else:
        # 最后一层，即形成了一个装备搭配方案
        if not step.dont_pruning:
            # 检查是否有神话装备
            god = 0
            if step.prefer_god and (has_god or is_god(equip)):
                god = 1
            # 计算套装数目
            set_list = ["1" + str(get_set_name(step.calc_data.selected_combination[x])) for x in range(0, 11)]
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

                    # 开始计算装备搭配
                    step.process_func(step)
        else:
            # 不进行任何剪枝操作，装备搭配对比的标准是最终计算出的伤害与奶量倍率
            step.process_func(step)

    # 回溯状态
    step.has_god = has_god
    step.current_index = current_index
    step.calc_data.selected_set_2_equips_map[set_name].remove(equip)
    step.calc_data.selected_combination.pop()


# 为当前已选择序列和后续剩余可选序列计算出一个尽可能精确的上限
def upper_bound(items, selected_combination, selected_has_god, remaining_start_index, prefer_god, last_god_slot):
    return upper_bound_2(items, selected_combination, selected_has_god, remaining_start_index, prefer_god, last_god_slot)


# note: 对照组：也就是后续
def upper_bound_none(items, selected_combination, selected_has_god, remaining_start_index, prefer_god, last_god_slot):
    return 1000000


# note: 思路一：由于每个新增部位产生套装词条数为1或0，因此计算当前序列的价值量，后续每个可选部位按照新增一个套装词条数来计算，可得到约束条件最小的最大上限
def upper_bound_1(items, selected_combination, selected_has_god, remaining_start_index, prefer_god, last_god_slot):
    # 计算至今为止已有的价值量
    current_value = calc_equip_value(selected_combination, selected_has_god, prefer_god)
    # 后续按最大价值量计算，即每个槽位按能产生一个套装词条数计算
    remaining_max_value = 11 - remaining_start_index
    # 获取神话的词条
    god_value = get_god_value(selected_has_god, remaining_start_index, prefer_god, last_god_slot)

    return current_value + remaining_max_value + god_value


# note: 思路二：计算新增k个序列所能产生的价值量最大套装词条数
# 新增k个装备所能产生的最大套装词条数（不计入神话）
max_inc_values = [0 for i in range(11 + 1)]
max_inc_values[1] = 1  # 2=>3
max_inc_values[2] = 2  # 1,1 => 2,2
max_inc_values[3] = 3  # 1,1,1 => 2,2,2
max_inc_values[4] = 4  # 1,1,1,1 => 2,2,2,2
max_inc_values[5] = 5  # 1,1,1,1 => 2,2,2,3
max_inc_values[6] = 6  # 1,1,1,1 => 2,2,3,3
max_inc_values[7] = 7  # 1,1,1,1 => 2,3,3,3
max_inc_values[8] = 7  # upper limit = 533->7
max_inc_values[9] = 7  # upper limit = 533->7
max_inc_values[10] = 7  # upper limit = 533->7
max_inc_values[11] = 7  # upper limit = 533->7


def upper_bound_2(items, selected_combination, selected_has_god, remaining_start_index, prefer_god, last_god_slot):
    # 计算至今为止已有的价值量
    current_value = calc_equip_value(selected_combination, selected_has_god, prefer_god)
    # 后续按最大价值量计算，即每个槽位按能产生一个套装词条数计算
    remaining_max_value = max_inc_values[11 - remaining_start_index]
    # 获取神话的词条
    god_value = get_god_value(selected_has_god, remaining_start_index, prefer_god, last_god_slot)

    return current_value + remaining_max_value + god_value


# 计算已有装备的套装词条数
def calc_equip_value(selected_combination, selected_has_god, prefer_god):
    set_list = ["1" + str(get_set_name(selected_combination[x])) for x in range(0, len(selected_combination))]
    set_val = Counter(set_list)
    del set_val['136', '137', '138']
    # 1件词条数=0，两件=1，三件、四件=2，五件=3
    setopt_num = sum([floor(x * 0.7) for x in set_val.values()])

    return setopt_num


def get_god_value(selected_has_god, remaining_start_index, prefer_god, last_god_slot):
    if prefer_god and (selected_has_god or remaining_start_index <= last_god_slot):
        return 1
    else:
        return 0

# undone: 思路三：进一步降低上限，在当前已有序列的各套装个数的前提下，计算任意n个序列所能产生的价值量最大套装词条数
# undone：思路四：进一步降低上限，在当前已有序列的各套装个数的前提下，计算后面n个序列的各套装配置下所能产生的价值量最大套装词条数
