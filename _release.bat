@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

set /P version="请输入版本号："

echo.
echo [提示]: 开始发布版本v%version%
echo.


:: 增加版本标签
git tag -d v%version%
git tag -a v%version% -m "release v%version%"

:: 发布前将代码推送到github
call _git_push_remote.bat

:: 调用构建脚本，打包
call _build.bat

echo.
echo [提示]: 构建完成，将结果复制到发布目录
echo.

echo copy to "%target_dir%"

:: 设置目标目录
set target_dir=.\..\..\..\downloads\(发布魔改计算器\再度魔改版史诗装备计算器_v%version%_by风之凌殇

:: 删除目标目录并重建
RMDIR /S /Q "%target_dir%"
MKDIR %target_dir%

:: 将所有文件复制到目标目录
XCOPY ".\*.*" "%target_dir%" /S /E /Y

:: 跳转到目标目录
cd "%target_dir%"

:: 移除一些无需发布的文件，以及初始化相关存档
xcopy preset_clear.XLSX preset.XLSX /Y/B
xcopy run_env_release.py dnf_calc\run_env.py /Y/B

RMDIR /S /Q ".git"
RMDIR /S /Q ".idea"
RMDIR /S /Q "logs"
RMDIR /S /Q "dnf_calc\__pycache__"
RMDIR /S /Q "robot"
RMDIR /S /Q "test"

DEL /Q "preset_clear.XLSX"
DEL /Q "run_env_release.py"
DEL /Q "test.py"
DEL /Q "排行结果.xlsx"

:: re: 配置工具尚未完成，先不发布
RMDIR /S /Q "dnf_calc_setting_tool"

:: 删除旧版本的这些文件
cd "使用说明"
del /Q 提示*.txt 注意*.txt 使用说明.txt _常见问题解答*.docx _手动安装运行环境教程*.docx
cd ..

:: 复制一份各个提示文件到使用说明目录
for %I in (提示*.txt 注意*.txt 使用说明.txt _常见问题解答*.docx _手动安装运行环境教程*.docx) do xcopy %I "使用说明\"  /Y/B

pause
