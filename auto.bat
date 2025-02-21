@echo off
cd /d %~dp0
python fetch_airdata.py
git add .
git commit -m "fetch data cont"
git push -u origin main