import os

SEP = os.sep


def main():
    # install_cocoapods()
    run_updates()
    run_local_app_build()


def install_cocoapods():
    print("\nPreparing Checkout App branch to be consumed locally...")
    os.environ["IPHONEOS_DEPLOYMENT_TARGET"] = "9.0"
    os.system("export IPHONEOS_DEPLOYMENT_TARGET=14.0")
    os.system("brew install cocoapods --build-from-source")
    os.system("sudo rm -rf /Library/Developer/CommandLineTools")
    os.system("sudo xcode-select --install")
    os.system("brew link --overwrite cocoapods")  # To overwrite an existing cocoapods installed
    
    
def run_updates():
    """[summary]
    Before executing this script, make sure you have:
    1) all the changes commited
    2) the current branch updated ('git checkout dev && git pull origin dev && git checkout <YOUR_BRANCH> && git rebase dev')
    """

    os.system("cd ..")
    os.system("rm -rf ~/Library/Developer/Xcode/DerivedData/")
    os.system("bundle install")
    os.system("pod update")
    os.system("bundle exec pod install")
    # os.system(f"open <YOUR_APP_SOURCE_NAME>.xcworkspace")
    print("\nNow you are able to run the XCUIT simulator")


def run_local_app_build():
    app_workspace = "../<YOUR_APP_SOURCE_NAME>.xcworkspace"
    stg_scheme = "<YOUR_APP_SOURCE_NAME>Staging"
    path_for_build = "/private/tmp/build/app"
    os.system(
        f'xcodebuild build-for-testing -workspace "{app_workspace}" -scheme "{stg_scheme}" -destination "platform=iOS Simulator,name=iPhone 12,OS=14.5" clean build CONFIGURATION_BUILD_DIR={path_for_build}'
    )


class Update:
    if __name__ == "__main__":
        main()
