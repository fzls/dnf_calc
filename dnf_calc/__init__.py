#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : __init__.py
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import logging
import multiprocessing
import pathlib
import sys
from datetime import datetime

from .common import *
from .const import *
from .enviroment import *
from .run_env import *
from .version import *

###########################################################
#                         logging                         #
###########################################################
logFormatter = logging.Formatter("%(asctime)s %(levelname)-5.5s [%(name)s] %(funcName)s:%(lineno)d: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.name = "calc"

log_directory = "logs"
try:
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)
except PermissionError as err:
    notify_error(None, "创建日志目录logs失败，请确认是否限制了基础的运行权限")
    sys.exit(-1)

process_name = multiprocessing.current_process().name
if is_debug_mode() or "MainProcess" in process_name:
    time_str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    fileHandler = logging.FileHandler("{0}/{1}_{2}_{3}.log".format(log_directory, logger.name, process_name, time_str), encoding="utf-8")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

###########################################################
#                         imports                         #
###########################################################

from .profiling_tool import *

from .data_struct import *

from .config import *
from .setting import *

from .hardware_info import *

from .update import *
from .logic import *
from .equipment import *

from .export_def import *
from .export import *

from .parallel_dfs import *
from .calc_core import *

# ui
from .ui_components import *
from .ui_const import *

from .producer_consumer import *
