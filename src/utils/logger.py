import platform
import random
import threading
from datetime import datetime
from enum import Enum
from pathlib import PurePosixPath, PureWindowsPath
from src.utils.settings import ENABLE_LOGGING, LOG_FOLDER_PATH, MAX_LOG_HASH_FILENAME_SIZE, PRINT_TO_STDOUT


mutex = threading.Lock()

class Level(Enum):
    INFO = "[INFO]"
    WARNING = "[WARNING]"
    ERROR = "[ERROR]"

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log(message: str, level: Level=Level.INFO, content: str="", file_name:str=random.getrandbits(MAX_LOG_HASH_FILENAME_SIZE), folder_path=LOG_FOLDER_PATH, to_std_out:bool=PRINT_TO_STDOUT):
        if not ENABLE_LOGGING:
            return message

        detailed_file_path = f"{folder_path}/details/{file_name}.txt"
        formatted_message: str = f"{level.value} - Timestamp: {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")} -> {message}."

        with mutex:
            if len(content) > 0:
                formatted_message += f" Written at: { str(PureWindowsPath(detailed_file_path) if platform.system() == "Windows" else PurePosixPath(detailed_file_path)) }\n"
                with open(detailed_file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            if to_std_out:
                print(formatted_message)

            with open(f"{folder_path}/logs.txt", "a", encoding="utf-8") as f:
                f.write(formatted_message + "\n")

        return message