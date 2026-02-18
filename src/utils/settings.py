from pathlib import Path


# Logging
ENABLE_LOGGING: bool = False
PRINT_TO_STDOUT: bool = False
MAX_LOG_HASH_FILENAME_SIZE: int = 64
LOG_FOLDER_PATH: str = f"{Path(__file__).parent.resolve()}/logs"

# Networking
DOWNLOAD_CHUNK_SIZE = 5000000 # 5MB per chunk

# Threads
MAX_POOL_THREADS: int = 25
QUEUE_TIMEOUT_SECONDS: int = 1

# Results
RESULT_FOLDER_PATH: str = f"{Path(__file__).parent.resolve()}/../../result"