import os
import argparse
from factory.utils.OsUtil import OsUtil
from subprocess import run

SEP = os.sep


def main(**args):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument(
        "--adb",
        choices=["install", "add_path"],
        help="==> Manage the ADB installation and path environments",
        default="add_path",
    )
    parser.add_argument(
        "--server",
        choices=["start", "stop", "install", "uninstall", "install_and_run"],
        help="==> Manage the Appium Client server execution. e.g.: 'python appium_setup.py --server start'",
        default="start",
    )
    parser.add_argument(
        "--localhost", help="==> Localhost IP for Appium connection.", default="0.0.0.0",
    )
    parser.add_argument(
        "--port", help="==> Localhost Port for Appium connection", default="4723",
    )
    args = parser.parse_args()
    adb = args.adb
    server = args.server
    localhost = args.localhost
    port = args.port

    adb_install(adb)
            
    adb_add_env_path(adb)
        
    appium_install(server)

    appium_uninstall(server)

    appium_start(server, localhost, port)

    appium_stop(server, port)

def appium_stop(server, port):
    if server == "stop":
        os_cmd_kill = (
            "taskkill /F /IM appium.exe"
            if OsUtil.has_os_platform_name("nt")
            else "kill -9 `lsof -i TCP:" + str(port) + " | awk '/LISTEN/{print $2}'`"
        )
        os.system(os_cmd_kill)
        check_created_processes("APPIUM KILLED")

def appium_start(server, localhost, port):
    if server == "start":
        print("\nAPPIM - Starting Client...")
        os.system(f"appium -v")
        os.system(f"appium --address {localhost} --port {port} &>/dev/null &")
        check_created_processes("APPIUM STARTED")

def appium_uninstall(server):
    if server == "uninstall":
        print("\nAPPIUM - Uninstalling Client ...")
        os.system("sudo npm uninstall -g appium --allow-root")
        os.system("sudo npm cache clean")
        print("Appium was uninstalled successfully!")

def appium_install(server):
    if server == "install" or server == "install_and_run":
        print("\nAPPIUM - Installing Client ...")
        os.system("npm install -g appium@1.20.2 --unsafe-perm=true --allow-root")
        os.system("npm install -g wd")
        os.system("npm i -g webpack")

        print("Appium version installed: ")
        os.system("appium -v")
        if server == "install_and_run":
            os.system("appium --address 0.0.0.0 --port 4723 &>/dev/null &")
            check_created_processes("APPIUM STARTED")

def adb_add_env_path(adb):
    if adb == "add_path":
        print("\nADB PATH ENVIRONMENT")
        os.system("export ANDROID_HOME=~/Library/Android/sdk")
        os.system("export ANDROID_SDK_ROOT=~/Library/Android/sdk")
        os.system("export PATH=$PATH:$ANDROID_HOME/platforms:$ANDROID_HOME/platform-tools >> ~/.bash_profile")
        os.system("source ~/.bash_profile")

def adb_install(adb):
    if adb == "install":
        try:
            print("\nANDROID DEBUG BRIDGE - Installing Client ...")
            os.system("brew install android-platform-tools")
        except: 
            os.system("brew reinstall android-platform-tools")
        finally:
            os.system("adb --version")


def check_created_processes(message):
    print(f"\n------- PROCESSES - {message} --------")
    os.system("ps -A | grep appium")


output = run("pwd", capture_output=True).stdout


class AppiumCmd:
    if __name__ == "__main__":
        main()
