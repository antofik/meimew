#!/bin/sh
mkdir logs
sudo ln -s /server/www/meimew/nginx.conf /etc/nginx/conf.d/meimew.conf
sudo ln -s /server/www/meimew/supervisor.conf /etc/supervisor/conf.d/meimew.conf