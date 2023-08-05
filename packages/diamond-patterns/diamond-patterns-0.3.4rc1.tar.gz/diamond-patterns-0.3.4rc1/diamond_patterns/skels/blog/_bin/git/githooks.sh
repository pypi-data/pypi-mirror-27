#!/bin/bash
# (cc) 2016 diamond-patterns

source .settings.conf

cp "_bin/git/post-receive.sh" "${GIT_REPO}/hooks/post-receive"
