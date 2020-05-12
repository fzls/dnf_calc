@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001
CLS

:: 设置变量
SET PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe
SET PYTHON_VERSION=python-3.8.2

echo.
echo [提示]: 开始下载 %PYTHON_VERSION%......请耐心等待0-0
echo.

:: 如果已存在则删除
if exist "%PYTHON_VERSION%.exe" del "%PYTHON_VERSION%.exe"

:: 下载python
tools\curl.exe --remote-name --remote-header-name %PYTHON_DOWNLOAD_URL%

:: 判断是否下载完成
if not exist "%PYTHON_VERSION%.exe" cls&color 0c&echo [Error]:Download Python false!...&pause>nul&exit

echo.
echo "[提示]: 下载完成，接下来请按照步骤安装python，一路只管点第一个选项就好啦"
echo.

:: 打开安装程序
%PYTHON_VERSION%.exe

:: 删除本地安装文件
del "%PYTHON_VERSION%.exe"&echo [Info]: %PYTHON_VERSION% Installation is complete(OK)!

:: 设置path
set PATH=%PATH%;"%appdata%\..\Local\Programs\Python\Python38-32";"%appdata%\..\Local\Programs\Python\Python38-64";"%appdata%\..\Local\Programs\Python\Python38";"%PROGRAMFILES%\Python38";"%PROGRAMFILES(x86)%\Python38";
set PATH=%PATH%;"%appdata%\..\Local\Programs\Python\Python38-32\Scripts";"%appdata%\..\Local\Programs\Python\Python38-64\Scripts";"%appdata%\..\Local\Programs\Python\Python38\Scripts";"%PROGRAMFILES%\Python38\Scripts";"%PROGRAMFILES(x86)%\Python38\Scripts";

echo.
echo "[提示]: python安装完成，接下来开始安装需要用到的一些类库"
echo.

:: 按照需要的类库
pip install --no-warn-script-location -r requirements.txt

echo.
echo "[提示]: 类库安装完成，接下来开始打包构建应用"
echo.

:: 调用构建脚本，打包
call _build.bat

echo.
echo "[提示]: 一切都搞定啦，现在可以直接点[再度魔改版史诗装备计算器_by风之凌殇.exe]运行啦"
echo.

pause

