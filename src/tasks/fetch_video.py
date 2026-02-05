import math
import requests
from src.threads.task import Task
from src.utils.logger import Logger, Level
from src.utils.settings import DOWNLOAD_CHUNK_SIZE
from src.video.video import Video
from typing import Any


class FetchVideo(Task):
    def __init__(self, video: Video, thread_count: int):
        self.__video = video
        self.__thread_count = thread_count if thread_count >= 1 else 1

    def execute(self, thread_id: int) -> Any:
        session = requests.Session()
        chunk_data = {}
        for track_type, track in self.__video.information().items():
            chunk_data[track_type] = bytearray()
            work_per_thread = math.ceil(track.size() / self.__thread_count)
            work_start = thread_id * work_per_thread
            work_end = min(work_start + work_per_thread - 1, track.size() - 1)

            start = work_start
            while start <= work_end:
                end = min(start + DOWNLOAD_CHUNK_SIZE - 1, work_end)

                headers = track.headers()
                headers["Range"] = f"bytes={start}-{end}"

                response: requests.Response = session.get(track.url(), headers=headers)
                if response.status_code not in (200, 206):
                    raise Exception(Logger.log(message=f"[{response.status_code}] - Error at byte: {start}", level=Level.ERROR))

                chunk_data[track_type] += response.content
                Logger.log(message=f"THREAD #{thread_id} downloaded {end}/{work_end} bytes", level=Level.INFO)
                start = end + 1

            Logger.log(message=f"THREAD #{thread_id} finished {track_type} track ({track.size()} bytes)", level=Level.INFO)
        return chunk_data
