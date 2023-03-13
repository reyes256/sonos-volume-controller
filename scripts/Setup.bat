@echo off

pip install soco
pip install flask

cd C:\ && git clone https://github.com/reyes256/sonos-volume-controller.git

cd C:\sonos-volume-controller\ && git pull
