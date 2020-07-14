@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

:: 目标版本，如v3.11.2
set target_version=%1

:: 存放补丁的目录
set patches_dir=patches
RMDIR /S /Q %patches_dir%
MKDIR %patches_dir%

:: 创建各个版本的补丁
CALL :create_patch v3.10.0
CALL :create_patch v3.11.0
CALL :create_patch v3.11.1

:: 压缩补丁文件
bc c -y -r -aoa -fmt:7z -l:9 "再度魔改版史诗装备计算器_%target_version%_by风之凌殇_增量更新文件.7z" "%patches_dir%"

:: the end
PAUSE
GOTO :EOF

:create_patch
set source_version=%source_version%
echo 创建从%source_version%升级到%target_version%的补丁
hdiffz.exe 再度魔改版史诗装备计算器_%source_version%_by风之凌殇 再度魔改版史诗装备计算器_%target_version%_by风之凌殇 %patches_dir%\%source_version%.patch
EXIT /B %ERRORLEVEL%
