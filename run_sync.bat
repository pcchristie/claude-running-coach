@echo off
REM run_sync.bat -- Standard session runner for sync.py
REM
REM Sets the correct working directory and encoding so sync.py works
REM regardless of which terminal or parent process calls it. %~dp0
REM resolves to the directory containing this .bat file, so this works
REM automatically no matter where the project is installed -- no need
REM to edit the path.
REM
REM Usage:
REM   run_sync.bat --athlete <name>                -- sync one athlete
REM   run_sync.bat --athlete <name> --history 730  -- initial DB load (2 years); only needed once
REM
REM Athlete names are whatever you configured in your .env file
REM (any ATHLETE_ID_<NAME> entry). If only one athlete is configured,
REM --athlete is optional.
REM
REM Output is written to sync_output.txt in this folder.

set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
python sync.py %*