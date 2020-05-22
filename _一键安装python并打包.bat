@ECHO OFF

:: 修改console默认encoding为utf8，避免中文乱码
CHCP 65001

:: 设置变量
SET PYTHON_VERSION=3.5.4
Set PYTHON_PATH_DIR=Python35
:: 如果当前使用的系统版本比较新（2018年以后的版本），理论上可以使用最新版本的3.8.3，如果比较老，建议使用上面的版本，理论上2015年以后发布的系统都可以安装
::SET PYTHON_VERSION=3.8.3
::Set PYTHON_PATH_DIR=Python38
SET PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%.exe
SET PYTHON_FULL_VERSION=python-%PYTHON_VERSION%

echo.
echo [提示]: 开始下载 %PYTHON_FULL_VERSION%......请耐心等待0-0
echo.

:: 如果已存在则删除
if exist "%PYTHON_FULL_VERSION%.exe" del "%PYTHON_FULL_VERSION%.exe"

:: 下载python
tools\curl.exe --remote-name --remote-header-name %PYTHON_DOWNLOAD_URL%

:: 判断是否下载完成
if not exist "%PYTHON_FULL_VERSION%.exe" cls&color 0c&echo [Error]:Download Python false!...&pause>nul&exit

echo.
echo "[提示]: 下载完成，接下来请按照步骤安装python，一路只管点第一个选项就好啦，记得把加入运行路径的选项勾上【Add Python to environment variables】"
echo.

:: 打开安装程序
%PYTHON_FULL_VERSION%.exe

:: 删除本地安装文件
del "%PYTHON_FULL_VERSION%.exe"&echo [Info]: %PYTHON_FULL_VERSION% Installation is complete(OK)!

:: 设置path
set PATH=%PATH%;"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%-32";"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%-64";"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%";"%PROGRAMFILES%\%PYTHON_PATH_DIR%";"%PROGRAMFILES(x86)%\%PYTHON_PATH_DIR%";
set PATH=%PATH%;"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%-32\Scripts";"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%-64\Scripts";"%appdata%\..\Local\Programs\Python\%PYTHON_PATH_DIR%\Scripts";"%PROGRAMFILES%\%PYTHON_PATH_DIR%\Scripts";"%PROGRAMFILES(x86)%\%PYTHON_PATH_DIR%\Scripts";

:: 关联python文件使用python打开
assoc .py=Python.File
ftype Python.File="C:\WINDOWS\pyw.exe" "%L" %*

echo.
echo "[提示]: python安装完成，接下来开始安装需要用到的一些类库"
echo.

:: 按照需要的类库
pip install --no-cache-dir --no-warn-script-location -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo "[提示]: 类库安装完成，接下来开始打包构建应用"
echo.

:: 调用构建脚本，打包
call _build.bat

echo.
echo "[提示]: 一切都搞定啦，现在可以直接点[再度魔改版史诗装备计算器_by风之凌殇.exe]运行啦"
echo "[提示]: 也可以直接点[再度魔改版史诗装备计算器_by风之凌殇.py]运行"
echo.

pause

