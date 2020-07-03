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
import sys
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


class FontConfig(ConfigInterface):
    def __init__(self, family="Microsoft YaHei", size=10, weight="bold"):
        # 设置字体
        self.family = family
        # 字体大小
        self.size = size
        # 字体粗细：normal/roman/bold/italic
        self.weight = weight


class FontsConfig(ConfigInterface):
    def __init__(self):
        # 指引字体
        self.guide_font = FontConfig(size=10)
        # 中字体
        self.mid_font = FontConfig(size=14)
        # 大字体
        self.big_font = FontConfig(size=18)


class BackgroundConfig(ConfigInterface):
    def __init__(self):
        # dark_main的rgb颜色
        self.main = [32, 34, 37]
        # dark_sub的rgb颜色
        self.sub = [46, 49, 52]
        # dark_blue的rgb颜色
        self.blue = [29, 30, 36]


# ui装备套装内顺序配置，可调整各个数组中元素的顺序来实现下次启动按新的顺序展示套装内装备
# 防具五件套的元素数目为6（神话+5）,其余类别套装的元素数目为4（神话+3）
# 每个元素的第一位表示装备部位，第二位表示是否是神话（0-否，1-是）
#
# 装备部位编码
# 11 上衣  12 裤子   13 头肩 14 腰带 15 鞋子
# 21 手镯  22 项链   23 戒指
# 31 辅助装备 32 魔法石 33 耳环
#
# 套装编码
# 1 大祭司 2 魔法师 3 舞姬 4 阴影 5 裁决者 6 龙血玄黄 7 沙漠 8 灸炎 9 擎天 10 地狱 11 铁匠 12 荆棘 13 不息 14 歧路 15 大自然
# 16 尘封术式 17 破晓 18 三角 19 权能
# 20 军神 21 灵宝 22 时间 23 能量
# 24 黑魔法 25 时空 26 呐喊 27 狂乱
# 28 深渊 29 圣者 30 命运 31 愤怒
# 32 求道者 33 次元 34 天命 35 悲剧
# 36 传说防具
# 37 普雷首饰
# 38 普雷特殊
class SetEquipmentsOrderConfig(ConfigInterface):
    def __init__(self):
        # 防具五件套（1-15） 上衣（神话）、上衣、头肩、下装、鞋、腰带
        self.armor = "[(11, 1), (11, 0), (13, 0), (12, 0), (15, 0), (14, 0)]"
        # 首饰（16-19） 手镯（神话）、项链、手镯、戒指
        self.jewelry = "[(21, 1), (22, 0), (21, 0), (23, 0)]"
        # 特殊装备（20-23） 耳环（神话）、辅助装备、魔法石、耳环
        self.special_equipment = "[(33, 1), (31, 0), (32, 0), (33, 0)]"
        # 散件（中）（24-27） 手镯（神话）、下装、手镯、魔法石
        self.spare_parts_mid = "[(21, 1), (12, 0), (21, 0), (32, 0)]"
        # 散件（左）（28-31） 上衣（神话）、上衣、项链、辅助装备
        self.spare_parts_left = "[(11, 1), (11, 0), (22, 0), (31, 0)]"
        # 散件（右）（32-35） 耳环（神话）、鞋、戒指、耳环
        self.spare_parts_right = "[(33, 1), (15, 0), (23, 0), (33, 0)]"


class UIConfig(ConfigInterface):
    def __init__(self):
        # 字体配置
        self.fonts = FontsConfig()
        # 背景色配置
        self.background = BackgroundConfig()
        # ui装备套装内顺序配置
        self.set_equipments_order = SetEquipmentsOrderConfig()


class PruneConfig(ConfigInterface):
    def __init__(self):
        # 背景知识：目前采用套装的词条数来进行剪枝，在搜索过程中会根据当前确定的搭配部分和后续剩余槽位所能带来的最大套装词条数之和来作为剪枝依据
        #           假设计算出的预估套装词条数为predict，当前搜索过的最大套装词条数为max，则仅当predict>=max的时候会继续搜索该分支
        #           也就是predict在[max, inf)区间内才会继续搜索
        # 继续搜索分支的下限与当前最大套装词条数max的差值，也就是说配置该值后，predict将在[max-delta_between_lower_bound_and_max, inf)的区间内继续搜索
        self.delta_between_lower_bound_and_max = 0


class HuanZhuangConfig(ConfigInterface):
    def __init__(self):
        # 是否启用奶系的切装（限单件）搜索方案
        self.enable = True
        # 奶系切装排除的部位，用于将特定部位的切装方案排除，如鞋子上有宝珠的话，换装打造成本太高
        # 装备部位编码
        # 11 上衣  12 裤子   13 头肩 14 腰带 15 鞋子
        # 21 手镯  22 项链   23 戒指
        # 31 辅助装备 32 魔法石 33 耳环
        self.exclude_slot = []  # type: List[str]
        # 最多切多少件
        self.max_replaced_count = 1
        # 是否考虑手动切装的方案，也就是祝福装和太阳装各一个神话的情况，因为登记和身上不能各有一个不同的神话装备，这种搭配只能靠手动切装来实现放祝福和太阳分别适用不同的神话对应的搭配
        self.include_manual_huanzhuang = False


class GifConfig(ConfigInterface):
    def __init__(self):
        # 是否播放gif动画
        self.enable = True
        # 每秒播放多少帧
        self.frame_rate = 10


class MultiThreadingConfig(ConfigInterface):
    def __init__(self):
        self.default_max_thread = 2 * multiprocessing.cpu_count()
        # 默认最大线程数不超过32，避免出现3900X这种24核心的cpu默认96个导致崩溃。手动设置时不受该限制影响
        if self.default_max_thread > 32:
            self.default_max_thread = 32
        # 设置最大工作线程数，当为0时默认为min(2*逻辑线程数, 32)
        self.max_thread = self.default_max_thread
        # 设置dfs的第多少层开始多线程并行计算（从1开始计数，0表示不启用多线程并行计算）
        self.start_parallel_computing_at_depth_n = 2

    def auto_update_config(self, raw_config: dict):
        super().auto_update_config(raw_config)
        if self.max_thread == 0:
            self.max_thread = self.default_max_thread


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
        # 计算祝福数值时的额外15级转职被动等级（暂时不知道为啥要额外加）
        self.base_job_passive_lv15_bless = 0
        # 计算太阳数值时的额外15级转职被动等级（暂时不知道为啥要额外加）
        self.base_job_passive_lv15_taiyang = 3


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

        # 奶妈、奶萝站街、进图面板差值（估算用）
        self.naima_nailuo_mianban_delta = 487


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
        self.max_save_count = 61
        # readme page
        self.readme_page = "https://github.com/fzls/dnf_calc/blob/master/README.md"
        # 是否在点击读取存档按钮时关闭结果窗口（若存在）
        self.destroy_result_windows_when_click_load_checklist_button = True
        # ui相关配置
        self.ui = UIConfig()
        # 剪枝调参
        self.prune = PruneConfig()
        # 换装
        self.huan_zhuang = HuanZhuangConfig()
        # 播放gif动画设置
        self.gif = GifConfig()
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

        if multiprocessing.current_process().name == "MainProcess":
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
    except UnicodeDecodeError as error:
        notify_error(logger, "{}的编码格式有问题，应为utf-8，如果使用系统自带记事本的话，请下载vscode或notepad++等文本编辑器\n错误信息：{}\n".format(config_path, error))
        sys.exit(0)
    except Exception as error:
        notify_error(logger, "读取{}文件出错，是否直接在压缩包中打开了？\n具体出错为：{}".format(config_path, error))
        sys.exit(-1)


def config():
    return g_config


if __name__ == '__main__':
    load_config("../config.toml")
    logger.info("ui cfg={}".format(g_config.ui))
