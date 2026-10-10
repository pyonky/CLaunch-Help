@echo off
cd /d "%~dp0"
python hhc_to_toc.py --title "CLaunch Help" --lang ja --encoding CP932 "%1" toc.html
