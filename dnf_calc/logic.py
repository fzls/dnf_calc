#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : logic
# Date   : 2020/5/22 0022
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------


###########################################################
#                         逻辑相关函数                     #
###########################################################

# 计算乘算的词条在增加对应比例后新的比率。如原先为增加20%技攻，新的词条额外增加50%技攻，则实际为1.2*1.5-1=80%技攻提升率
from dnf_calc import config, get_setting, logger
from .const import *


def multiply_entry(old_inc_percent, add_inc_percent):
    return (old_inc_percent / 100 + 1) * (add_inc_percent / 100 + 1) * 100 - 100


# 获取国服特殊加成属性, job_type = "buf" or "deal"
def add_bonus_attributes_to_base_array(job_type, base_array, style, creature, save_name):
    cfg = config()

    original_base_array = base_array.copy()

    guofu_teses = [
        {"name": "称号", "setting_name": "styles", "selected": style},
        {"name": "宠物", "setting_name": "creatures", "selected": creature},
        {"name": "其余特色", "setting_name": "account_other_bonus_attributes", "selected": "所有账号共用"},
        {"name": "其余特色", "setting_name": "account_other_bonus_attributes", "selected": save_name},
    ]

    for tese in guofu_teses:
        # 处理每一种特色
        setting = get_setting(tese["setting_name"], tese["selected"])
        if setting is None or setting["entries"] is None:
            continue
        # 增加当前选择的特色的各个词条对应的该类型职业的属性
        logger.info("应用国服特色：{}({})".format(tese["selected"], tese["name"]))
        for entry in setting["entries"]:
            for name, value in entry.items():
                entry_indexes = entry_name_to_indexes[name]
                entry_value = eval(str(value))
                entry_writen = False
                if job_type == "deal":
                    # 处理输出职业的对应属性
                    if "deal" not in entry_indexes:
                        continue
                    for entry_index in entry_indexes["deal"]:
                        if entry_index in deal_multiply_entry_indexes:
                            # 需要乘算
                            base_array[entry_index] = multiply_entry(base_array[entry_index], entry_value)
                        else:
                            # 其余加算
                            if name == "extra_all_job_all_active_skill_lv_1_30" and entry_index == index_deal_extra_active_skill_lv_1_45:
                                # 由于词条[所有职业Lv1~30全部主动技能Lv+X（特性技能除外）]不能直接对应输出职业的1-45主动技能,需要打个折,可以自行配置折扣率
                                base_array[entry_index] += entry_value * cfg.data_fixup.extra_all_job_all_active_skill_lv_1_30_deal_1_45_rate
                            else:
                                # 正常情况
                                base_array[entry_index] += entry_value
                        if not entry_writen:
                            logger.info("\t词条：{} {}".format(entry_name_to_name[name], entry_value))
                            entry_writen = True
                        logger.info("\t\t{} => {}".format(deal_entry_index_to_name[entry_index], entry_value))
                else:
                    # 处理奶系职业的对应属性
                    if "buf" not in entry_indexes:
                        continue
                    for entry_index in entry_indexes["buf"]:
                        if entry_index in buf_multiply_entry_indexes:
                            # 需要乘算
                            base_array[entry_index] = multiply_entry(base_array[entry_index], entry_value)
                        else:
                            # 全部加算
                            base_array[entry_index] += entry_value
                        if not entry_writen:
                            logger.info("\t词条：{} => {}".format(entry_name_to_name[name], entry_value))
                            entry_writen = True
                        logger.info("\t\t{} => {}".format(buf_entry_index_to_name[entry_index], entry_value))

    all_tese_strs = []

    diff_base_array = base_array - original_base_array
    index_info = job_to_base_array_index_range_and_index_to_name_dict[job_type]
    index_to_name_dict = index_info["index_to_name_dict"]
    for index in range(index_info["index_begin"], index_info["index_end"] + 1):
        name = index_to_name_dict[index]
        if diff_base_array[index] == 0:
            # 跳过没有实际加成的特色词条
            continue
        all_tese_strs.append("{} => {}".format(name, diff_base_array[index]))

    logger.info("最终特色加成属性如下:\n{}".format("\n".join(all_tese_strs)))
