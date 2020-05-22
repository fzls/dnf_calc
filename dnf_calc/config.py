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
from abc import ABCMeta
from typing import List

import toml

from dnf_calc import notify_error, logger, consoleHandler


# 如果配置的值是dict，可以用ConfigInterface自行实现对应结构，将会自动解析
# 如果配置的值是list/set/tuple，则需要实现ConfigInterface，同时重写auto_update_config，在调用过基类的该函数后，再自行处理这三类结果
class ConfigInterface(metaclass=ABCMeta):
    def auto_update_config(self, raw_config: dict):
        for key, val in raw_config.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(attr, ConfigInterface):
                    config_field = attr  # type: ConfigInterface
                    config_field.auto_update_config(val)
                else:
                    setattr(self, key, val)

    def get_str_for(self, v):
        res = v
        if isinstance(v, ConfigInterface):
            res = v.__str__()
        elif isinstance(v, list):
            res = list(self.get_str_for(sv) for sk, sv in enumerate(v))
        elif isinstance(v, tuple):
            res = tuple(self.get_str_for(sv) for sk, sv in enumerate(v))
        elif isinstance(v, set):
            res = set(self.get_str_for(sv) for sk, sv in enumerate(v))
        elif isinstance(v, dict):
            res = {sk: self.get_str_for(sv) for sk, sv in v.items()}

        return res

    def __str__(self):
        res = {}
        for k, v in self.__dict__.items():
            res[k] = self.get_str_for(v)
        return str(res)


class MultiThreadingConfig(ConfigInterface):
    def __init__(self):
        # 设置最大工作线程数，当为0时默认为当前的逻辑线程数
        self.max_thread = multiprocessing.cpu_count()
        # 设置dfs的第多少层开始多线程并行计算（从1开始计数，0表示不启用多线程并行计算）
        self.start_parallel_computing_at_depth_n = 2

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)
        if self.max_thread == 0:
            self.max_thread = multiprocessing.cpu_count()


class ExportResultAsExcelConfig(ConfigInterface):
    def __init__(self):
        # 启用导出excel功能
        self.enable = False
        # 导出的文件名
        self.export_file_name = "排行结果.xlsx"
        # 导出前N名
        self.export_rank_count = 1000


class DataFixupConfig(ConfigInterface):
    def __init__(self):
        # 由于词条[所有职业Lv1~30全部主动技能Lv+X（特性技能除外）]不能直接对应输出职业的1-45主动技能,需要打个折,可以自行配置折扣率
        self.extra_all_job_all_active_skill_lv_1_30_deal_1_45_rate = 0.8


class SaveNameConfig(ConfigInterface):
    def __init__(self):
        # 对应存档名
        self.save_name = "召唤"
        # 该存档名的分数伤害转换系数
        self.score_to_damage_rate = "1 / 1077.97 * 3320"


class TwentySecondsDamageConfig(ConfigInterface):
    def __init__(self):
        # 是否显示预估的20s打桩数据
        self.enable = True
        # 默认的分数与打桩的比例关系
        self.score_to_damage_rate = "1 / 1077.97 * 3320"  # 本人召唤在分数为107797%时，修炼场20s的伤害为3320e，先以这个为准给一版供参考的伤害值
        # 设定存档对应的分数与打桩的比例关系，若下列数组中配置了当前存档的打桩系数，则会使用该系数，否则使用默认的打桩系数
        self.save_name_configs = []  # type: List[SaveNameConfig]

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)
        if "save_name_configs" in raw_config:
            self.save_name_configs = []  # type: List[SaveNameConfig]
            for cfg in raw_config["save_name_configs"]:
                save_name_config = SaveNameConfig()
                save_name_config.auto_update_config(cfg)
                self.save_name_configs.append(save_name_config)


class InititalDataConfig(ConfigInterface):
    def __init__(self):
        # 啥也不穿的满级奶爸的体力与精神
        self.physical_and_mental = "2674"
        # 啥也不穿的满级奶妈和奶萝的智力
        self.intelligence = "2400 - 33"


class ConstConfig(ConfigInterface):
    def __init__(self):
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


class Config(ConfigInterface):
    log_level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    def __init__(self):
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
        self.twenty_seconds_damage = TwentySecondsDamageConfig()  # type: TwentySecondsDamageConfig
        # 一些初始值
        self.initital_data = InititalDataConfig()
        # 一些常量
        self.const = ConstConfig()

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)

        # 名字不同，需要特殊处理
        if "20s_damage" in raw_config:
            self.twenty_seconds_damage.auto_update_config(raw_config["20s_damage"])

        self.on_config_update(raw_config)

    def on_config_update(self, raw_config: dict):
        consoleHandler.setLevel(self.log_level_map[self.log_level])

        logger.info("config loaded")
        logging.info("log level change to %s", self.log_level)
        logging.info("max thread is set to %d", self.multi_threading.max_thread)
        logger.debug("raw_config={}".format(raw_config))
        logger.debug("config={}".format(g_config))


g_config = Config()


# 读取程序config
def load_config(config_path="config.toml"):
    global g_config
    try:
        raw_config = toml.load(config_path)
        g_config.auto_update_config(raw_config)
    except FileNotFoundError as error:
        notify_error(logger, "未找到{}文件，是否直接在压缩包中打开了？".format(config_path))
        exit(0)


def config():
    return g_config
