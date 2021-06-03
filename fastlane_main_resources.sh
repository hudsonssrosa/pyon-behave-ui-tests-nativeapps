#!/bin/bash
#chmod +x behave_runner.py

# Make this script callable automatically only in case of scalling new VMs.

# CHECK / INSTALL PYTHON 3.8
if which python > /dev/null 2>&1;
then
    python_version=`python --version 2>&1 | awk '{print $2}'`
    python_version_full=`python --version`
    if [[ $python_version_full == *"Python 3."* ]]; 
    then
        echo "Python version $python_version it's there!"
    else
        echo 'PYTHON - Installing...'
        brew install python@3.8
    fi
else
    echo "No Python executable is found."
    echo 'PYTHON - Installing...'
    brew install python@3.8
fi
echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> ~/.zshrc
export LDFLAGS="-L/usr/local/opt/python@3.8/lib"
export PKG_CONFIG_PATH="/usr/local/opt/python@3.8/lib/pkgconfig"


# CHECK / INSTALL JAVA 8
if which java > /dev/null 2>&1;
then
    java_version=`java -version 2>&1 | head -n 1`
    echo "Java version $java_version is installed."
else
    echo "No Java executable is found."
    echo 'JAVA - Installing...'
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    $ brew tap homebrew/cask-versions
    brew update
    brew tap caskroom/cask
    brew cask install adoptopenjdk8
    JAVA_HOME=/usr/libexec/java_home
    export PATH=$PATH:$JAVA_HOME:$JAVA_HOME/bin
fi

# ANDROID_HOME=/usr/local/bin/adb
# export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools


