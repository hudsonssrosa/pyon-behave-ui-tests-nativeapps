import os

SEP = os.sep


def main():
    run_updates()


def run_updates():
    _ver3 = set_for_unix()

    print("\nUpdating PIP...")
    os.system(f"python3 -m pip install --upgrade pip")

    print("\nInstalling Python Environment...")
    os.system(f"python3 -m pip install pipenv")

    print("\nSetting a new Python Environment...")
    os.system(f"python3 -m virtualenv venv")

    print("\nUpdating all packages and resources...")
    os.system(f"python3 -m pip install -r requirements.txt --user")
    os.system(f"python3 -m pip install -U black --user")
    os.system(f"python3 -m pip install -U rope --user")

    print("\nPackages installed:")
    os.system(f"python3 -m pip list")
    os.system(f"python3 -m pip install --upgrade pip")


def set_for_unix():
    if os.name != "nt":
        return "3"


class Update:
    if __name__ == "__main__":
        main()
