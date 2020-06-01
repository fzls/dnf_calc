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

# 用于实现排行的最小堆
from heapq import heapify, heappush, heappushpop


class MinHeap():
    def __init__(self, top_n):
        self.h = []
        self.length = top_n
        heapify(self.h)

    def add(self, element):
        if len(self.h) < self.length:
            heappush(self.h, element)
        else:
            heappushpop(self.h, element)

    def getTop(self):
        return sorted(self.h, reverse=True)