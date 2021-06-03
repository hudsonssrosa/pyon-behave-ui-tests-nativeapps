import os
import shutil
from subprocess import run
from sys import platform as _platform


class OsUtil:
    @staticmethod
    def search_file_in_root_dir(current_folder_name, file_name):
        settings_dir = os.path.dirname(os.path.abspath(file_name))
        root_dir = current_folder_name
        settings_dir_sep = settings_dir.split(root_dir)
        final_dir = settings_dir_sep[0] + root_dir
        return os.path.join(final_dir, file_name)

    @staticmethod
    def get_current_dir_by_chosen_name(current_folder_name):
        settings_dir = os.path.dirname(os.path.abspath(current_folder_name))
        settings_dir_sep = settings_dir.split(current_folder_name)
        final_dir = settings_dir_sep[0] + os.sep + current_folder_name
        return os.path.join(final_dir)

    @staticmethod
    def get_current_dir_name():
        return os.path.basename(os.getcwd())

    @staticmethod
    def get_current_dir():
        return os.path.curdir

    @staticmethod
    def zip_folder(root_dir, zip_file_name, file_format):
        shutil.make_archive(root_dir + os.sep + zip_file_name, file_format, root_dir)
        print(f"-> Package created in {root_dir}{os.sep}{zip_file_name}.{file_format}")

    @staticmethod
    def get_os_platform():
        if _platform == "linux" or _platform == "linux2":
            return "Linux"
        elif _platform == "darwin":
            return "MAC OS X"
        elif _platform == "win32":
            return "Windows 32 bits"
        elif _platform == "win64":
            return "Windows 64 bits"

    @staticmethod
    def get_os_platform_to_execute_a_file_format():
        return ".exe" if os.name == "nt" else ""

    @staticmethod
    def get_os_platform_web_driver_name():
        if _platform == "linux" or _platform == "linux2":
            return "_linux"
        elif _platform == "darwin":
            return "_macos"
        elif _platform == "win32" or _platform == "win64" or os.name == "nt":
            return ".exe"

    @staticmethod
    def has_os_platform_name(os_name):
        if _platform == os_name or str(_platform).__contains__(os_name):
            return True

    @staticmethod
    def send_command_to_os(*command_str):
        os.system(*command_str)

    @staticmethod
    def set_env_var(var_name, set_value):
        os.environ[var_name] = str(set_value)
        print(f'-> "{var_name}" ENV variable in PATH: {os.environ.get(var_name)}')

    @staticmethod
    def get_cmd_output(command_):
        output = run(command_, capture_output=True).stdout
        return str(output.decode("utf8")).replace("\n", "")
