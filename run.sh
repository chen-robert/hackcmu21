#!/bin/sh
/usr/sbin/nginx
/usr/local/bin/uwsgi --ini /etc/uwsgi/uwsgi.ini
