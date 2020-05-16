@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

echo.
echo [提示]: 更新子模块
echo.

git submodule update --remote
