#!/bin/bash

# To be able to run mayavi in headless mode (no windows) follow the
# instructions at:
# https://docs.travis-ci.com/user/gui-and-headless-browsers/#Using-xvfb-to-Run-Tests-That-Require-a-GUI
# Copied from the sphinx-gallery config file:
# https://github.com/sphinx-gallery/sphinx-gallery/blob/master/.travis.yml

# Only build the docs on Linux and Python 2,7. Mayavi won't work in Python 3
# yet or on OS X in headless mode (it might, but I don't want to find out how)

# To return a failure if any commands inside fail
set -e

if [ "$BUILD_DOCS" == "true" ];
then
    export DISPLAY=:99.0
    sh -e /etc/init.d/xvfb start
    sleep 3  # give xvfb some time to start
    make -C doc
    echo "Finished building documentation."
else
    echo "Not building documentation."
fi

# Workaround for https://github.com/travis-ci/travis-ci/issues/6522
# Turn off exit on failure.
set +e
