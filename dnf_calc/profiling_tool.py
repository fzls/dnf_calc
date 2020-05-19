#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : debug
# Date   : 2020/5/17 0017
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import time
from inspect import getframeinfo, stack

from dnf_calc import logger, format_time

###########################################################
#                      性能排查工具                        #
###########################################################

_profiling_start_time = time.time()
_profiling_last_step_time = time.time()

_profiling_stats = []


def _profiling_print_debug_timing_info(message):
    global _profiling_last_step_time, _profiling_stats
    timeline = time.time() - _profiling_start_time
    used_time_since_last_step = time.time() - _profiling_last_step_time
    _profiling_last_step_time = time.time()

    # if message in ["初始化tkinter"]:
    #     return

    # if message not in ["读取各种装备与套装的图片"]:
    #     return

    stat = {
        "lineno": getframeinfo(stack()[1][0]).lineno,
        "timeline": timeline,
        "step_used": used_time_since_last_step,
        "message": message,
    }

    _profiling_stats.append(stat)

    logger.debug("line {:4}: timeline={} step_used={} message={}"
        .format(
        stat["lineno"],
        format_time(stat["timeline"]),
        format_time(stat["step_used"]),
        stat["message"]
    )
    )


def _profiling_print_stats():
    global _profiling_stats
    if len(_profiling_stats) == 0:
        return

    total_used_time = _profiling_stats[-1]["timeline"]
    logger.debug("-----------------total={}-----------top 10 step----------------------------".format(
        format_time(total_used_time)))

    _profiling_stats = sorted(_profiling_stats, key=lambda k: k['step_used'], reverse=True)
    if len(_profiling_stats) > 10:
        _profiling_stats = _profiling_stats[:10]

    for stat in _profiling_stats:
        lineno = stat["lineno"]
        step_used = stat["step_used"]
        step_percent = step_used / total_used_time * 100

        logger.debug("line {:4}: step_used={} percent={:.2f}% message={}"
            .format(
            stat["lineno"],
            format_time(stat["step_used"]),
            step_percent,
            stat["message"]
        )
        )
