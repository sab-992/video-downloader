import platform
import random
from datetime import datetime
from enum import Enum
from pathlib import Path, PureWindowsPath, PurePosixPath

class Level(Enum):
    INFO = "[INFO]"
    WARNING = "[WARNING]"
    ERROR = "[ERROR]"

class Logger:
    def __init__(self):
        pass

    def log(self, exception: Exception, level: Level=Level.INFO, content: str="", file_name:str=random.getrandbits(64), folder_path=f"{Path(__file__).parent.resolve()}/logs"):
        detailed_path = f"{folder_path}/details/{file_name}.txt"

        with open(f"{folder_path}/logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{level.value} - Timestamp: {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")} -> {exception}. Written at: { str(PureWindowsPath(detailed_path) if platform.system() == "Windows" else PurePosixPath(detailed_path)) }\n")

        if len(content) > 0:
            with open(detailed_path, "w", encoding="utf-8") as f:
                f.write(content)

        return exception