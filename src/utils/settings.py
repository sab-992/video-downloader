from pathlib import Path


# Logging
ENABLE_LOGGING: bool = True
PRINT_TO_STDOUT = True
MAX_LOG_HASH_FILENAME_SIZE = 64
LOG_FOLDER_PATH = f"{Path(__file__).parent.resolve()}/logs"

# Networking
DOWNLOAD_CHUNK_SIZE = 5000000 # 5MB per chunk

# Threads
MAX_POOL_THREADS: int = 25
QUEUE_TIMEOUT_SECONDS: int = 1