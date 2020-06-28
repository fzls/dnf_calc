@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

echo.
echo [提示]: 导出excel为txt，方便版本对比
echo.

python _export_excel_to_txt.py


echo.
echo [提示]: 开始打包计算器
echo.


:: 使用pyinstaller打包
pyinstaller.exe --hidden-import pkg_resources.py2_warn --exclude-module PySide2 --noconsole -F "再度魔改版史诗装备计算器_by风之凌殇.py"

:: 复制生成的结果后删除临时文件
COPY /Y "dist\再度魔改版史诗装备计算器_by风之凌殇.exe" "再度魔改版史诗装备计算器_by风之凌殇.exe"
RMDIR /S /Q "build" "dist" "__pycache__"
DEL /Q "再度魔改版史诗装备计算器_by风之凌殇.spec"


echo.
echo [提示]: 计算器打包结束
echo.


echo.
echo [提示]: 开始打包配置工具
echo.

cd dnf_calc_setting_tool_py

:: 使用pyinstaller打包
pyinstaller.exe --hidden-import pkg_resources.py2_warn --hidden-import PySide2.QtXml --noconsole -F "setting_tool.py"

:: 复制生成的结果后删除临时文件
COPY /Y "dist\setting_tool.exe" "setting_tool.exe"
RMDIR /S /Q "build" "dist" "__pycache__"
DEL /Q "setting_tool.spec"

cd ..

echo.
echo [提示]: 配置工具打包结束
echo.
