@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001
CLS

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
RMDIR /S /Q ".git" ".idea" "logs"
DEL /Q "preset_clear.XLSX" "test.py" “排行结果.xlsx”
ren "魔改后.py__" "魔改后.py"
ren "calc.py__" "calc.py"
