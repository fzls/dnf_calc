@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

echo.
echo [提示]: 推送本地改动到远程仓库
echo.

git push origin master --tags
