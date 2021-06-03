#!/bin/bash
#chmod +x behave_runner.py

echo 'XCODE Version'
xcodebuild -version

echo 'APPIUM CLIENT - Installing and Running...'
bash -c "\
    python3 appium_setup.py --server install_and_run & \
    sleep 5 &
    "

