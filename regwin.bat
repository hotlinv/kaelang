@echo off
echo BAT�ű���windowsϵͳ���½�������ʱ����ʾ����
echo --------------------------------------
echo ִ�й��̼�أ�
echo.
echo 1���޸�ע�������...

for %%i in (python.exe) do @set py=%%~$PATH:i
for %%i in ( %py%) do @set py=%%~dpi
echo %py%

reg add "HKEY_CLASSES_ROOT\.ae" /t REG_SZ /d kaelang
reg add "HKEY_CLASSES_ROOT\kaelang" /t REG_SZ /d Kae�ű��ļ�
reg add "HKEY_CLASSES_ROOT\kaelang\DefaultIcon" /t REG_SZ /d %~dp0.asserts\favicon64.ico
reg add "HKEY_CLASSES_ROOT\kaelang\shell\open\command" /t REG_SZ /d "kae.exe \"%%1\""
echo ע����޸����.

echo.
echo 2��������Դ������...
taskkill /f /im explorer.exe & start explorer.exe
::�ж���Դ�������Ƿ������ɹ�
if %errorlevel%==0 (
echo ��Դ�������������.
) else (
echo ��Դ����������ʧ��.
)
echo.
echo 3������ִ�����.
echo --------------------------------------
pause
