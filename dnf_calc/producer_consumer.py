#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File      : producer_consumer
# DateTime  : 2020/6/7 0007 12:04
# Author    : Chen Ji
# Email     : fzls.zju@gmail.com
# -------------------------------

import multiprocessing
import platform
import time
import traceback
import uuid

import bugsnag

from dnf_calc import logger, configure_bugsnag, notify_error, get_hardward_info, config, all_settings, RUN_ENV, now_version, ver_time, load_config, load_settings


class ProducerData:
    def __init__(self):
        self.work_queue = None  # type: multiprocessing.JoinableQueue
        self.calc_index = 0
        self.produced_count = 0


producer_data = ProducerData()


def producer(*args):
    # if exit_calc.value == 1:
    #     return
    producer_data.work_queue.put((producer_data.calc_index, args))

    producer_data.produced_count += 1
    logger.info("producer put %3dth work into work queue", producer_data.produced_count)


def consumer(work_queue, exit_calc, work_func):
    current_process = multiprocessing.current_process()
    # 为工作线程配置bugsnag信息
    configure_bugsnag()

    # 启动时先读取config和setting
    load_config()
    load_settings()

    logger.info("work thread={} started, configure_bugsnag done, ready to work".format(current_process))
    current_calc_index = 0
    processed_count = 0
    while True:
        calc_index, args = work_queue.get()
        try:
            if calc_index != current_calc_index:
                current_calc_index = calc_index
                processed_count = 0
            processed_count += 1
            logger.info("work thread {} processing {}th work".format(current_process, processed_count))

            work_func(*args)
            raise Exception("test 3")
        except Exception as error:
            report_bugsnag_in_worker(current_process, error, processed_count, [arg.__dict__ for arg in args])
        finally:
            work_queue.task_done()


def report_bugsnag_in_worker(current_process, error, processed_count, args, show_error_messagebox=True):
    traceback_info = traceback.format_exc()

    # 打印错误日志
    logger.info("work thread {} unhandled exception={} when processing {}th work\nargs={}\n{}".format(current_process, error, processed_count, args, traceback_info))

    # 弹出错误框
    if show_error_messagebox:
        notify_error(logger, "工作线程{}在处理第{}个计算项的搜索搭配过程中出现了未处理的异常\n{}".format(current_process, processed_count, traceback_info))

    # 上报bugsnag
    cpu_name, physical_cpu_cores, manufacturer = get_hardward_info()
    meta_data = {
        "worker_task_info": {
            "args": args,
        },
        "stacktrace_brief": {
            "info": traceback_info,
        },
        "config": config(),
        "settings": all_settings(),
        "app": {
            "releaseStage": RUN_ENV,
            "version": now_version,
            "release_time": ver_time,
        },
        "device": {
            "uuid": uuid.getnode(),
            "node": platform.node(),
            "osName": platform.system(),
            "osVersion": platform.version(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "logical_cpu_num": multiprocessing.cpu_count(),
            "physical_cpu_num": physical_cpu_cores,
            "cpu_name": cpu_name,
            "manufacturer": manufacturer,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": time.strftime("%z", time.gmtime()),
        },
    }
    bugsnag.notify(
        exception=error,
        context="worker",
        meta_data=meta_data,
        user={"id": platform.node(), "uuid": uuid.getnode(), },
    )
