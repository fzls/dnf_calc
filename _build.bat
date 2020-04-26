python _export_excel_to_txt.py

:: 使用pyinstaller打包
pyinstaller.exe --hidden-import pkg_resources.py2_warn  --noconsole -F "再度魔改版史诗装备计算器_by风之凌殇.py"

:: 复制生成的结果后删除临时文件
COPY /Y "dist\再度魔改版史诗装备计算器_by风之凌殇.exe" "再度魔改版史诗装备计算器_by风之凌殇.exe"
RMDIR /S /Q "build" "dist" "__pycache__"
DEL /Q "再度魔改版史诗装备计算器_by风之凌殇.spec"
