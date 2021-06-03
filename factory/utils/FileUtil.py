import configparser
import os
import shutil
import time
from factory.handling.running_exception import RunningException as Rexc


class FileUtil:
    @staticmethod
    def remove_files(deletion_message, rel_or_abs_dir):
        try:
            if os.path.exists(rel_or_abs_dir):
                shutil.rmtree(rel_or_abs_dir)
                print(f"-> {rel_or_abs_dir} {deletion_message}")
            time.sleep(2)
        except FileNotFoundError as fnfe:
            Rexc.raise_exception_error("Directory not found: ", fnfe)

    @staticmethod
    def read_properties(conf_files):
        if conf_files is not None:
            config = configparser.RawConfigParser()
            for i, conf_file in enumerate(conf_files):
                if os.path.exists(conf_file):
                    config.read(conf_file)
            return config

    @staticmethod
    def remove_last_element_from_path(full_path):
        split_path = str(full_path).split(os.sep)
        del split_path[-1]
        return os.sep.join(folders for folders in split_path)
