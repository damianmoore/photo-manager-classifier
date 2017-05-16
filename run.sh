#!/bin/sh

>&2 echo "Starting supervisor"
supervisord -c /etc/supervisord.conf
