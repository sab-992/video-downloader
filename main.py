from src.tasks.fetch_video import FetchVideo
from src.threads.threads import Threads
from src.video.video import Video


VIDEO_URL = ""

def main():
    video = Video(VIDEO_URL, "1920x1080", 60)

    threads = Threads()
    threads.start_all()

    for _ in range(len(threads)):
        threads.add_task(FetchVideo(video=video, thread_count=len(threads)))

    results: dict = threads.stop_all()

    video.save(results)

if __name__ == "__main__":
    main()