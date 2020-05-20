#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : config
# Date   : 2020/5/20 0020
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import logging
import multiprocessing
from typing import List

import toml

from dnf_calc import notify_error, logger, consoleHandler


class BaseConfig(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        setattr(self, key, value)


class MultiThreadingConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 设置最大工作线程数，当为0时默认为当前的逻辑线程数
        self.max_thread = multiprocessing.cpu_count()
        # 设置dfs的第多少层开始多线程并行计算（从1开始计数，0表示不启用多线程并行计算）
        self.start_parallel_computing_at_depth_n = 2

    def __str__(self):
        return str(vars(self))


class ExportResultAsExcelConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 启用导出excel功能
        self.enable = False
        # 导出的文件名
        self.export_file_name = "排行结果.xlsx"
        # 导出前N名
        self.export_rank_count = 1000


class DataFixupConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 由于词条[所有职业Lv1~30全部主动技能Lv+X（特性技能除外）]不能直接对应输出职业的1-45主动技能,需要打个折,可以自行配置折扣率
        self.extra_all_job_all_active_skill_lv_1_30_deal_1_45_rate = 0.8


class SaveNameConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 对应存档名
        self.save_name = "召唤"
        # 该存档名的分数伤害转换系数
        self.score_to_damage_rate = "1 / 1077.97 * 3320"


class TwentySecondsDamageConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 是否显示预估的20s打桩数据
        self.enable = True
        # 默认的分数与打桩的比例关系
        self.score_to_damage_rate = "1 / 1077.97 * 3320"  # 本人召唤在分数为107797%时，修炼场20s的伤害为3320e，先以这个为准给一版供参考的伤害值
        # 设定存档对应的分数与打桩的比例关系，若下列数组中配置了当前存档的打桩系数，则会使用该系数，否则使用默认的打桩系数
        self.save_name_configs: List[SaveNameConfig] = []


class InititalDataConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        # 啥也不穿的满级奶爸的体力与精神
        self.physical_and_mental = "2674"
        # 啥也不穿的满级奶妈和奶萝的智力
        self.intelligence = "2400 - 33"


class ConstConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        ## 奶爸
        # 多少体精折合一级祝福
        self.naiba_physical_and_mental_divisor = 630

        ## 奶妈
        # 多少智力折合一级祝福
        self.naima_intelligence_divisor = 675
        # 唱歌倍率的一些系数：sing_song_increase_rate = naima_sing_song_increase_rate_base + naima_sing_song_increase_rate_amplification_coef * base_array[index_buf_amplification]
        self.naima_sing_song_increase_rate_base = 1.25
        self.naima_sing_song_increase_rate_amplification_coef = 0.05

        ## 奶萝
        # 多少智力折合一级祝福
        self.nailuo_intelligence_divisor = 665
        # # 唱歌倍率的一些系数：sing_song_increase_rate = (nailuo_sing_song_increase_rate_base + nailuo_sing_song_increase_rate_amplification_coef * base_array[index_buf_amplification]) * nailuo_sing_song_increase_rate_final_coef
        self.nailuo_sing_song_increase_rate_base = 1.20
        self.nailuo_sing_song_increase_rate_amplification_coef = 0.05
        self.nailuo_sing_song_increase_rate_final_coef = 1.20


class Config(BaseConfig):
    log_level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self):
        super().__init__()
        # 日志等级, 级别从低到高依次为 "debug", "info", "warning", "error", "critical"
        self.log_level = "info"
        # 是否检查更新
        self.check_update_on_start = True
        # 是否允许主界面缩放（界面实际布局是固定大小的）
        self.main_window_resizable = False
        # 最大存档数
        self.max_save_count = 1000
        # 是否在点击读取存档按钮时关闭结果窗口（若存在）
        self.destroy_result_windows_when_click_load_checklist_button = True
        # 多线程配置
        self.multi_threading = MultiThreadingConfig()
        # 是否需要额外将输出结果导出为excel文件
        self.export_result_as_excel = ExportResultAsExcelConfig()
        # 一些需要特殊补正的数据
        self.data_fixup = DataFixupConfig()
        # 20s打桩数据
        self.twenty_seconds_damage = TwentySecondsDamageConfig()
        # 一些初始值
        self.initital_data = InititalDataConfig()
        # 一些常量
        self.const = ConstConfig()

    def on_config_loaded(self):
        self.fix_data()

        consoleHandler.setLevel(self.log_level_map[self.log_level])

        logger.info("config loaded")
        logging.info("log level change to %s", self.log_level)
        logging.info("max thread is set to %d", self.multi_threading.max_thread)
        logger.debug("config={}".format(g_config))

    def fix_data(self):
        # ps: 之前使用toml配置文件的时候，配置名写成了以数字为开头，这使得不能直接通过.attr的方式访问属性，但又要保证配置兼容，所以只能在这里中转一下
        if hasattr(self, "20s_damage"):
            self.twenty_seconds_damage = getattr(self, "20s_damage")

        # 设置最大工作线程数，当为0时默认为当前的逻辑线程数
        if self.multi_threading.max_thread == 0:
            self.multi_threading.max_thread = multiprocessing.cpu_count()


g_config = Config()


# 读取程序config
def load_config(config_path="config.toml"):
    global g_config
    try:
        g_config = toml.load(config_path, Config)
        g_config.on_config_loaded()
    except FileNotFoundError as error:
        notify_error(logger, "未找到{}文件，是否直接在压缩包中打开了？".format(config_path))
        exit(0)


def config():
    return g_config
