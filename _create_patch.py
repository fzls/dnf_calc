#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File      : _create_patch.py
# DateTime  : 2020/7/15 0015 2:22
# Author    : Chen Ji
# Email     : fzls.zju@gmail.com
# -------------------------------
import os
import re
import shutil
import sys
from typing import List


class VersionInfo:
    def __init__(self, version: tuple, dirpath: str):
        self.version = version
        self.dirpath = dirpath

    def __lt__(self, other):
        return self.version < other.version

    def __repr__(self):
        return str(self.__dict__)


def parse_version(regex, version_str):
    match = re.search(regex, version_str)
    if match is None:
        return False, (0, 0, 0)
    match_dict = match.groupdict()
    major_ver = int(match_dict["major_ver"])
    minor_ver = int(match_dict["minor_ver"])
    patch_ver = int(match_dict["patch_ver"])
    return True, (major_ver, minor_ver, patch_ver)


def version_str(version):
    return ".".join(str(v) for v in version)


# 解析传入的最新版本号
matched, latest_version = parse_version(r"v?(?P<major_ver>\d+)\.(?P<minor_ver>\d+)\.(?P<patch_ver>\d+)", sys.argv[1])
if not matched:
    print("传入的版本号格式不正确，示例：v3.12.0 或 3.12.0")
    sys.exit(-1)

print(os.getcwd(), latest_version)

version_dir_regex = r"再度魔改版史诗装备计算器_v(?P<major_ver>\d+)\.(?P<minor_ver>\d+)\.(?P<patch_ver>\d+)_by风之凌殇"

# 获取最新的几个版本的信息
old_version_infos = []  # type: List[VersionInfo]
for dirpath in os.listdir("."):
    if not os.path.isdir(dirpath):
        continue

    matched, version = parse_version(version_dir_regex, dirpath)
    if not matched:
        continue
    if version >= latest_version:
        continue

    old_version_infos.append(VersionInfo(version, dirpath))

create_patch_for_latest_n_version = 8
old_version_infos = sorted(old_version_infos)[-create_patch_for_latest_n_version:]
print(old_version_infos)

# 创建patch目录
patches_dir = "patches"

shutil.rmtree(patches_dir, ignore_errors=True)
os.mkdir(patches_dir)

# 为旧版本创建patch文件
latest_version_str = version_str(latest_version)
target_version_dir = "再度魔改版史诗装备计算器_v{}_by风之凌殇".format(latest_version_str)
print(target_version_dir)

for version_info in old_version_infos:
    version = version_str(version_info.version)
    patch_file = "{}/{}.patch".format(patches_dir, version)

    print("创建从v{}升级到v{}的补丁{}".format(version, latest_version_str, patch_file))

    version_dir = "再度魔改版史诗装备计算器_v{}_by风之凌殇".format(version)
    os.system("hdiffz.exe {} {} {}".format(version_dir, target_version_dir, patch_file))

# 压缩打包
patch_oldest_version = version_str(old_version_infos[0].version)
patch_newest_version = version_str(old_version_infos[-1].version)
os.system('bc c -y -r -aoa -fmt:7z -l:9 "再度魔改版史诗装备计算器_v{}_by风之凌殇_增量更新文件_v{}_to_v{}.7z" "{}"'.format(
    latest_version_str, patch_oldest_version, patch_newest_version, patches_dir
))
