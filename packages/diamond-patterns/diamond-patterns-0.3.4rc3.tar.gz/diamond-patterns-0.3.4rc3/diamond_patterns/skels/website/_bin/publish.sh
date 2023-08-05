#!/bin/bash
# (cc) 2016 diamond-patterns

if [ -f /usr/local/rvm/scripts/rvm ]; then
    source /usr/local/rvm/scripts/rvm
fi

echo "publish site"
cd ~/site
git pull
make build install
echo "OK"
