#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : data_struct
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

###########################################################
#                       辅助的数据结构                     #
###########################################################

import time
# 用于实现排行的最小堆
from heapq import heapify, heappush, heappushpop
from multiprocessing import Queue
from multiprocessing.managers import ValueProxy
from typing import List, Dict, Set

from numpy import ndarray

from .config import Config, ConstConfig, PruneConfig, HuanZhuangConfig, DataTransferConfig


class MinHeap:
    def __init__(self, top_n, batch_size):
        self.h = []
        self.length = top_n

        self.processed_result_count = 0

        self.batch_size = batch_size

        heapify(self.h)

    def add(self, element):
        if len(self.h) < self.length:
            heappush(self.h, element)
        else:
            heappushpop(self.h, element)

    def getTop(self):
        return sorted(self.h, reverse=True)

    def merge(self, other):
        """
        合并另一个堆
        @type other MinHeap
        """
        for elem in other.h:
            self.add(elem)
        self.processed_result_count += other.processed_result_count
        self.batch_size = other.batch_size

    def reset(self):
        self.h = []

        self.processed_result_count = 0

        heapify(self.h)

    def update_batch_size(self, data_transfer_cfg: DataTransferConfig):
        if self.batch_size < data_transfer_cfg.batch_stage_double_upper_bound:
            self.batch_size *= 2
        else:
            self.batch_size += data_transfer_cfg.batch_linear_increase_size


class MinHeapWithQueue:
    def __init__(self, name: str, minheap: MinHeap, minheap_queue: Queue):
        self.name = name
        self.minheap = minheap
        self.minheap_queue = minheap_queue

        self.start_time = time.time()

    def process_results_per_second(self) -> float:
        return float(self.minheap.processed_result_count) / (time.time() - self.start_time + 1e-6)


class UpdateInfo:
    def __init__(self):
        self.latest_version = ""
        self.netdisk_link = ""
        self.netdisk_passcode = ""
        self.update_message = ""

    def __str__(self):
        return str(self.__dict__)


class CalcStepData:
    def __init__(self):
        # 装备相关数据
        self.items = []
        self.has_baibianguai = False
        self.not_select_items = []
        self.has_uniforms = []
        self.can_upgrade_work_unifrom_nums = 0
        self.work_uniforms_items = []
        self.transfer_max_count = 0
        self.transfer_slots_equips = []

        # 预计算的一些量
        self.last_god_slot = 11  # 表示从最后一个有神话的槽位的下标，从0开始，10结束
        # 仅奶系使用的一些数据
        # 当前已拥有的装备中，各个套装的装备信息。set_index => set(equip_index)
        self.owned_set_2_equips_map = {}  # type: Dict[str, Set[str]]

        # 计算过程维护的一些中间量
        self.current_index = 0
        self.has_god = False
        # 统计当前最优词条数
        self.local_max_setop = 0
        self.max_setopt = 0  # type: ValueProxy[int]
        self.max_possiable_setopt = 3 + 2 + 2 + (1 - 0)  # 533 以及神话对应的一个词条（默认神话优先）
        self.calc_data = CalcData()

        # 一些配置
        self.dont_pruning = False
        self.set_perfect = 0
        self.prefer_god = True
        self.prune_cfg = None  # type: PruneConfig
        self.start_parallel_computing_at_depth_n = 0

        # 配置数据
        self.config = None  # type: Config

        # 其他
        self.producer = None
        self.process_func = None

    def __str__(self):
        return "{}".format({
            "CalcStepData": self.__dict__,
            "CalcData": self.calc_data,
        })


class CalcData:
    def __init__(self):
        # 搜索得到的装备搭配信息
        self.selected_combination = []
        self.baibianguai = None
        self.upgrade_work_uniforms = []
        self.transfered_equips = []
        self.selected_set_2_equips_map = {}  # type: Dict[str, Set[str]]

        # 玩家选定的武器
        self.weapon_indexs = []

        # 职业类型
        self.is_shuchu_job = True  # 是否是输出职业

        # ----------------------输出职业----------------------
        # 各种加成
        self.base_array_with_deal_bonus_attributes = []  # type: ndarray
        # 配置表得到的信息
        self.opt_one = {}  # 将会预先切片，满足计算需求，避免每次计算时都重新切片
        self.job_lv1 = 0
        self.job_lv2 = 0
        self.job_lv3 = 0
        self.job_lv4 = 0
        self.job_lv5 = 0
        self.job_lv6 = 0
        self.job_pas0 = 0
        self.job_pas1 = 0
        self.job_pas2 = 0
        self.job_pas3 = 0
        # 玩家设定的其他信息
        self.cool_on = 0
        self.ele_skill = 0

        # ----------------------奶系职业----------------------
        # 各种加成
        self.base_array_with_buf_bonus_attributes = []  # type: ndarray
        # 配置表得到的信息
        self.job_name = ""
        self.const = None  # type: ConstConfig
        self.huan_zhuang = None  # type: HuanZhuangConfig
        self.huanzhuang_slot_fixup = {}  # 当前存档的buff换装槽位补正信息 slot_index => list(attribute_index_str => fixup_value)
        self.opt_buf = {}
        self.opt_buflvl = {}
        self.base_job_passive_lv15_bless = 0
        self.base_job_passive_lv15_taiyang = 0
        self.base_stat_custom_bless_data_minus_taiyang_data = 0
        self.base_stat_physical_and_mental = 0
        self.base_stat_intelligence = 0
        self.base_bless_level = 0
        self.base_taiyang_level = 0
        self.base_job_passive_lv15 = 0
        self.base_naiba_protect_badge_lv25 = 0

        # 本地排行用的最小堆
        self.minheaps = None  # type: List[MinHeap]
        # 回传结果的队列
        self.minheap_queues = None  # type: List[Queue]
        # 用于判定是否提前停止计算的变量 re: 这个等下测试性能时先干掉，然后后面通过消息、事件之类的实现。比如calc开始时通知各个工作线程进入工作状态，stop或计算完成时通知各个工作线程进行停止状态
        self.exit_calc = 0  # type: ValueProxy[int]

    def __str__(self):
        return "{}".format({
            "weapon_indexs": self.weapon_indexs,
            "selected_combination": self.selected_combination,
            "baibianguai": self.baibianguai,
            "upgrade_work_uniforms": self.upgrade_work_uniforms,
            "transfered_equips": self.transfered_equips,
            "selected_set_2_equips_map": self.selected_set_2_equips_map,

            "base_array_with_deal_bonus_attributes": self.base_array_with_deal_bonus_attributes,
            "cool_on": self.cool_on,
            "ele_skill": self.ele_skill,
            "job_name": self.job_name,
            "const": self.const,
        })


class BlessHuanZhuangStep:
    def __init__(self):
        self.current_index = 0
        self.has_god = False


class BlessHuanZhuang:
    def __init__(self, equips, huanzhuang_equips, baibianguai, upgrade_work_uniforms, transfered):
        self.equips = equips  # 勇气祝福换装装备
        self.huanzhuang_equips = huanzhuang_equips  # 与太阳装备不同的装备
        self.baibianguai = baibianguai  # 百变怪得来的切装装备
        self.upgrade_work_uniforms = upgrade_work_uniforms  # 额外升级的工作服的切装装备
        self.transfered = transfered  # 跨界过来的切装装备
