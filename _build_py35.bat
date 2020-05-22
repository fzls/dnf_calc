@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

echo.
echo [提示]: 导出excel为txt，方便版本对比
echo.

python _export_excel_to_txt.py

echo.
echo [提示]: 使用python35运行一下，先确保能启动
echo.

"C:\Program Files\Python35\python.exe" 再度魔改版史诗装备计算器_by风之凌殇.py

echo.
echo [提示]: 开始打包
echo.


:: 使用pyinstaller打包
"C:\Program Files\Python35\Scripts\pyinstaller.exe" --hidden-import pkg_resources.py2_warn  --noconsole -F "再度魔改版史诗装备计算器_by风之凌殇.py"

:: 复制生成的结果后删除临时文件
COPY /Y "dist\再度魔改版史诗装备计算器_by风之凌殇.exe" "再度魔改版史诗装备计算器_by风之凌殇.exe"
RMDIR /S /Q "build" "dist" "__pycache__"
DEL /Q "再度魔改版史诗装备计算器_by风之凌殇.spec"


echo.
echo [提示]: 打包结束
echo.
