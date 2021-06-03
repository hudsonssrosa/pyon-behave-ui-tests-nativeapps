#!/bin/bash
#chmod +x behave_runner.py


# NATIVE APP - OFFICIAL ENVIRONMENT SETTINGS
PYON_ENVIRONMENT='staging'
PYON_TARGET='remote_emulation'
PYON_MODE='native_app'

PYON_OS='iOS'
PYON_OS_VERSION='14.5'
PYON_DEVICE='iPhone 12'

PYON_ORIENTATION='Portrait'
PYON_LANGUAGE='en'
PYON_LOCALE='en_GB'
PYON_APP_PATH=$1

PYON_TAGS=
PYON_EXCLUDED_TAG='wip'


echo 'COPYING PROPERTIES...'
cp env_settings.properties.local env_settings.properties

echo '\nRUNNING BEHAVE TESTS...'
bash -c "
    python3 behave_runner.py --target $PYON_TARGET \
                            --environment '$PYON_ENVIRONMENT' \
                            --mode $PYON_MODE \
                            --os '$PYON_OS' \
                            --os_version '$PYON_OS_VERSION' \
                            --device_name '$PYON_DEVICE' \
                            --orientation '$PYON_ORIENTATION' \
                            --language '$PYON_LANGUAGE' \
                            --locale '$PYON_LOCALE' \
                            --app_path '$PYON_APP_PATH' \
                            --tags '$PYON_TAGS' \
                            --exclude '$PYON_EXCLUDED_TAG'
                        "
    
echo '\nSTOPPING APPIUM SERVER...'
python3 appium_setup.py --server stop
