@echo off
echo BAT脚本：windows系统右下角任务栏时间显示秒数
echo --------------------------------------
echo 执行过程监控：
echo.
echo 1、修改注册表项中...

for %%i in (python.exe) do @set py=%%~$PATH:i
for %%i in ( %py%) do @set py=%%~dpi
echo %py%

reg add "HKEY_CLASSES_ROOT\.ae" /t REG_SZ /d kaelang
reg add "HKEY_CLASSES_ROOT\kaelang" /t REG_SZ /d Kae脚本文件
reg add "HKEY_CLASSES_ROOT\kaelang\DefaultIcon" /t REG_SZ /d %~dp0.asserts\favicon64.ico
reg add "HKEY_CLASSES_ROOT\kaelang\shell\open\command" /t REG_SZ /d "%py%/Scripts/kae.exe \"%%1\""
echo 注册表修改完成.

echo.
echo 2、重启资源管理器...
taskkill /f /im explorer.exe & start explorer.exe
::判断资源管理器是否重启成功
if %errorlevel%==0 (
echo 资源管理器重启完成.
) else (
echo 资源管理器重启失败.
)
echo.
echo 3、任务执行完毕.
echo --------------------------------------
pause
