@echo off
setlocal enabledelayedexpansion

set "regPath=HKEY_CURRENT_USER\Software\CyberIsGood\Client"
set "dirPath=%TEMP%\CyberIsGood"
set "tmpFile=call_numbers.tmp"
set "tmpPath=%~dp0%tmpFile%"

rem Check if directory key exists, if not create it.
reg query %regPath% >nul 2>&1
if !errorlevel! neq 0 (
    echo Registry key does not exist. Creating key and values...
    reg add "%regPath%" /f
    reg add "%regPath%" /v "server_ip" /t REG_SZ /d "" /f
    reg add "%regPath%" /v "server_port" /t REG_SZ /d "" /f
    reg add "%regPath%" /v "temp_file_index" /t REG_DWORD /d 0 /f
) else (
    echo Registry key exists. Checking for values...

    rem Check if server_ip exists, if not create it.
    reg query "%regPath%" /v "server_ip" >nul 2>&1
    if !errorlevel! neq 0 (
        echo Value server_ip does not exist. Creating it...
        reg add "%regPath%" /v "server_ip" /t REG_SZ /d "" /f
    ) else (
        echo Value server_ip already exists.
    )

    rem Check if server_port exists, if not create it.
    reg query "%regPath%" /v "server_port" >nul 2>&1
    if !errorlevel! neq 0 (
        echo Value server_port does not exist. Creating it...
        reg add "%regPath%" /v "server_port" /t REG_SZ /d "" /f
    ) else (
        echo Value server_port already exists.
    )

    rem Check if temp_file_index exists, if not create it.
    reg query "%regPath%" /v "temp_file_index" >nul 2>&1
    if !errorlevel! neq 0 (
        echo Value temp_file_index does not exist. Creating it...
        reg add "%regPath%" /v "temp_file_index" /t REG_DWORD /d 0 /f
    ) else (
        echo Value temp_file_index already exists.
    )
)

rem Check if temp directory exists, if not create it.
if not exist "%dirPath%" (
    echo Temp directory does not exist. Creating it...
    mkdir "%dirPath%"
) else (
    echo Temp directory already exists.
)

rem Check if call_numbers.tmp exists, if not create it.
if not exist %tmpPath% (
    echo File call_numbers.tmp does not exist. Creating it...
    type nul > "%tmpPath%"
) else (
    echo File call_numbers.tmp already exists.
)

endlocal