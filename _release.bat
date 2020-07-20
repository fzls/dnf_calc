@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

set /P version="请输入版本号："

set run_start_time=%time%

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
set parent_dir="D:\downloads\(发布魔改计算器"
set target_dir="D:\downloads\(发布魔改计算器\再度魔改版史诗装备计算器_v%version%_by风之凌殇"

echo copy to "%target_dir%"

:: 删除目标目录并重建
RMDIR /S /Q "%target_dir%"
MKDIR %target_dir%

:: 将所有文件复制到目标目录
XCOPY ".\*.*" "%target_dir%" /S /Y

:: 复制增量更新相关文件
XCOPY _create_patch.py "%parent_dir%" /S /Y
XCOPY hdiffz.exe "%parent_dir%" /S /Y
XCOPY _apply_patch.bat "%parent_dir%" /S /Y
XCOPY hpatchz.exe "%parent_dir%" /S /Y

:: 跳转到目标目录
cd "%target_dir%"

:: 初始化相关存档
xcopy preset_clear.XLSX preset.XLSX /Y/B
xcopy run_env_release.py dnf_calc\run_env.py /Y/B
echo f | xcopy README.md "更新日志.txt" /Y/B

:: 删除旧版本的这些文件
cd "使用说明"
del /Q 提示*.txt 注意*.txt 使用说明.txt 更新日志.txt _常见问题解答*.docx _手动安装运行环境教程*.docx 计算器简易使用说明*_By_AJOIL.docx 《使用说明：从入门到入土》*_by真的超级傻.pdf 增量更新教程*.docx
cd ..

xcopy 提示*.txt "使用说明\" /Y/B
xcopy 注意*.txt "使用说明\" /Y/B
xcopy 使用说明.txt "使用说明\" /Y/B
xcopy 更新日志.txt "使用说明\" /Y/B
xcopy _常见问题解答*.docx "使用说明\" /Y/B
xcopy _手动安装运行环境教程*.docx "使用说明\" /Y/B
xcopy 计算器简易使用说明*_By_AJOIL.docx "使用说明\" /Y/B
xcopy 《使用说明：从入门到入土》*_by真的超级傻.pdf "使用说明\" /Y/B
xcopy 增量更新教程*.docx "使用说明\" /Y/B


:: 清理目录结构，使目录更加清爽
cd "%target_dir%"
RMDIR /S /Q ".git"
RMDIR /S /Q ".idea"
RMDIR /S /Q "等待添加的装备图片"
RMDIR /S /Q "dnf_calc\__pycache__"
RMDIR /S /Q "dnf_calc\logs"
RMDIR /S /Q "dnf_calc_setting_tool"
RMDIR /S /Q "dnf_calc_setting_tool_py\__pycache__"
DEL /Q "dnf_calc_setting_tool_py\UI\.DS_Store"
DEL /Q "dnf_calc_setting_tool_py\.git"
DEL /Q "dnf_calc_setting_tool_py\.gitignore"
RMDIR /S /Q "logs"
RMDIR /S /Q "robot"
RMDIR /S /Q "test"
DEL /Q ".gitignore"
DEL /Q ".gitmodules"
DEL /Q "_git_push_remote.bat"
DEL /Q "_git_update_submodule.bat"
DEL /Q "_release.bat"
DEL /Q _常见问题解答*.docx
DEL /Q _手动安装运行环境教程*.docx
DEL /Q 《使用说明：从入门到入土》*_by真的超级傻.pdf
DEL /Q "preset_clear.XLSX"
DEL /Q "preset_test_set.XLSX"
DEL /Q "README.md"
DEL /Q "run_env_release.py"
DEL /Q "test.py"
DEL /Q "txt_from_excel.txt"
DEL /Q 计算器简易使用说明*_By_AJOIL.docx
DEL /Q "排行结果.xlsx"
DEL /Q "使用说明.txt"
DEL /Q 提示*.txt
DEL /Q 注意*.txt
DEL /Q _create_patch.py
DEL /Q hdiffz.exe
DEL /Q _apply_patch.bat
DEL /Q hpatchz.exe

echo.
echo [提示]: 处理完成，开始压缩打包
echo.

:: 打包为7z
cd ..
set target_7z=再度魔改版史诗装备计算器_v%version%_by风之凌殇.7z
set source_dir=再度魔改版史诗装备计算器_v%version%_by风之凌殇
bc c -y -r -aoa -fmt:7z -l:9 "%target_7z%" "%source_dir%"

echo.
echo [提示]: 创建增量更新补丁
echo.

call _create_patch.py v%version%

echo 打包完毕
echo 开始时间：%run_start_time%
echo 结束时间：%time%

pause
