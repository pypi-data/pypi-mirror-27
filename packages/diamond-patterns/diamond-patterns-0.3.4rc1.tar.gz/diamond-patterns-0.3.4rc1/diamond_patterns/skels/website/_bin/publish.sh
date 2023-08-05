#!/bin/bash
# (cc) 2016 diamond-patterns

source /usr/local/rvm/scripts/rvm

cd ~/$(whoami)
git pull
JEKYLL_ENV=production bundle exec jekyll build
rsync -acv --delete _site/ /var/www/$(whoami)/
