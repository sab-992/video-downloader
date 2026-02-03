import yt_dlp
from src.utils.logger import Logger, Level
from src.video.detail.track import Track
from src.video.detail.audio_track import AudioTrack
from src.video.detail.video_track import VideoTrack


class Video:
    def __init__(self, url: str, resolution: str):
        self.__url = url
        self.__resolution = resolution

        ydl_opts = { 'format': '18', # TODO: Remove hardcoded value
                     'quiet': True,
                     'no_warnings': True, }

        self.__video_information: dict[str, Track] = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.__url, download=False)
            self.__title = info.get("title", "")
            
            # Check if we got a single URL or multiple streams
            if 'url' in info:
                self.__video_information["merged"] = Track(info)
            elif 'requested_formats' in info:
                self.__video_information["audio"] = AudioTrack(info['requested_formats'][1])
                self.__video_information["video"] = VideoTrack(info['requested_formats'][0])
            else:
                raise Exception(Logger.log(message=f"Couldn't extract video information", level=Level.ERROR))

    def information(self) -> dict[str, Track]:
        return self.__video_information

    def resolution(self):
        return self.__resolution
    
    def save(self, results: dict[int, dict[str, bytearray]]):
        video_merged = bytearray()
        audio_merged = bytearray()

        for i in range(len(results)):
            audio_merged += results[i]["audio"]
            video_merged += results[i]["video"]

        with open(f"{self.__title}.mp3", "wb") as f:
            f.write(audio_merged)

        # TODO: write the mp4 file by combining frame data and audio data

    def title(self):
        return self.__title
            
    def url(self):
        return self.__url
