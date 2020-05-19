#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : init_enviroment
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------

import bugsnag

from .run_env import RUN_ENV
from .version import now_version


def is_debug_mode():
    return RUN_ENV == "debug"


###########################################################
#                         bugsnag                         #
###########################################################


def configure_bugsnag():
    if is_debug_mode():
        return

    # 增加bugsnag上报一些不在预期内的错误
    bugsnag.configure(
        api_key="723026d09a7442c9e02ebc5d4a08e8d0",
        app_version=now_version,
        auto_capture_sessions=True,
    )
