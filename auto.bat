@echo off
cd /d %~dp0

:: Get the current timestamp in YYYY-MM-DD HH:MM:SS format
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set timestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%

python fetch_airdata.py
python read_airdata.py
git add .

:: Commit with timestamp
git commit -m "fetch data on %timestamp%"
git push -u origin main