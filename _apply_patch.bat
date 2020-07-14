@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001
CLS

:: 用于应用当前版本对应的增量更新到当前目录的脚本
:: 用法:根据提示输入当前版本号 如3.11.2若在增量更新列表中
::      会应用并提示更新成功。否则会提示错误
:: 相对目录情况如下
::  - 计算器主目录
::      - patches
::          - 3.11.2.patch
::      - _apply_patch.bat
::      - hpatchz.exe

echo 请输入你当前使用的版本号，可从压缩包的名字或计算器的原始解压缩目录名中获知，格式为：3.11.2
set /P current_version="当前版本号："

set target_patch_file="patches\%current_version%.patch"

if exist "%target_patch_file%" (
    hpatchz.exe -C-diff -f . "%target_patch_file%" .
    echo 已成功更新
) else (
    echo 更新失败，未找到当前版本对应的增量更新补丁，可能是版本太老了，可以尝试下载最新的完整包~
)

PAUSE
