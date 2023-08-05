#!/bin/bash
# (cc) 2016 diamond-patterns

if [ -f /usr/local/rvm/scripts/rvm ]; then
    source /usr/local/rvm/scripts/rvm
fi

bundle install --path vendor/bundle
