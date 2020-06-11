#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : hardware_info
# Date   : 2020/5/22 0022
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import platform
if platform.system() == "Windows":
    import pythoncom
    import wmi


def get_hardward_info() -> (str, int, str):
    if platform.system() != "Windows":
        return "", 0, ""

    pythoncom.CoInitialize()
    wmiInfo = wmi.WMI()

    cpu_name = ""
    physical_cpu_cores = 0
    manufacturer = ""

    for cpu in wmiInfo.Win32_Processor():
        cpu_name = cpu.Name

        try:
            physical_cpu_cores = cpu.NumberOfCores
        except:
            physical_cpu_cores = 1

    for board_id in wmiInfo.Win32_BaseBoard():
        manufacturer = board_id.Manufacturer  # 主板生产品牌厂家

    return cpu_name, physical_cpu_cores, manufacturer
