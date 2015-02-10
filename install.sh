#!/bin/sh
sudo virtualenv env
sudo ./env/bin/pip install -r requirements.txt
mkdir logs
sudo ln -s /server/www/meimew/nginx.conf /etc/nginx/conf.d/meimew.conf
sudo ln -s /server/www/meimew/supervisor.conf /etc/supervisor/conf.d/meimew.conf
