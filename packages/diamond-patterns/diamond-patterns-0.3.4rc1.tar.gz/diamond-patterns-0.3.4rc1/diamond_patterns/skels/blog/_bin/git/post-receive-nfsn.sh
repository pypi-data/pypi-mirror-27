#!/bin/bash
# (cc) 2016 diamond-patterns

if [ -f /usr/local/rvm/scripts/rvm ]; then
    source /usr/local/rvm/scripts/rvm
fi

# extract settings from bare repo
export BARE_REPO=$PWD
echo $BARE_REPO
git show HEAD:.settings.conf > /tmp/.settings.conf

# load installation settings
source /tmp/.settings.conf

# clone the repo
export GIT_DIR=".git"
rm -rf "${WORKING_PATH}"
git clone "${BARE_REPO}" "${WORKING_PATH}"

# copy the archive of the ruby stuff over
cp -r /home/private/.bundle "${WORKING_PATH}/.bundle"
cp -r /home/private/vendor "${WORKING_PATH}/vendor"

# build
cd "${WORKING_PATH}"
make build

# publish
rsync -acv --delete _site/ "${PUBLISH_PATH}"

rm -rf "${WORKING_PATH}"
rm /tmp/.settings.conf
