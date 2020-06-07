#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File      : producer_consumer
# DateTime  : 2020/6/7 0007 12:04
# Author    : Chen Ji
# Email     : fzls.zju@gmail.com
# -------------------------------

import multiprocessing

from dnf_calc import logger


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
    logger.info("work thread={} started, ready to work".format(current_process))
    current_calc_index = 0
    processed_count = 0
    while True:
        # 加一个超时，用于最终计算完成时，没有新的task，超时1s退出
        calc_index, args = work_queue.get()
        if calc_index != current_calc_index:
            current_calc_index = calc_index
            processed_count = 0
        processed_count += 1
        logger.info("work thread {} processing {}th work".format(current_process, processed_count))
        # if exit_calc.value == 0:
        work_func(*args)
        work_queue.task_done()

    logger.info("work thread %2d stopped, processed_count=%3", thread_index, processed_count)
