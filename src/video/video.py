import yt_dlp
from src.utils.logger import Logger, Level
from src.video.detail.track import Track
from src.video.detail.audio_track import AudioTrack
from src.video.detail.video_track import VideoTrack


MB_CONVERSION_MULT = 1000000
class Video:
    def __init__(self, url: str, resolution: str, fps: int=None):
        self.__url = url
        self.__resolution = resolution

        ydl_opts = { "format": f"bestvideo[height={self.__get_resolution_height(resolution)}]{f"[fps={fps}]" if fps else ""}+bestaudio/best",
                     "outtmpl": "video.mp4",
                     "quiet": True,
                     "no_warnings": True, }

        self.__video_information: dict[str, Track] = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.__url, download=False)
            self.__title = info.get("title", "unnamed_video")

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
    
    def save(self, results: dict[int, dict[str, bytearray]], audio_extension: str=None):
        if len(results) <= 0:
            return

        # Verify if audio and video tracks are already merged.
        if len(results[0]) == 1 and results[0].get("merged", None):
            final_video = bytearray()
            for i in range(len(results)):
                final_video += results[i]["merged"]
                
            with open(f"{self.__title}.{self.__video_information["merged"].ext()}", "wb") as f:
                f.write(final_video)
            
            Logger.log(f"Wrote {len(final_video) / MB_CONVERSION_MULT} MB.")
            return

        video_merged = bytearray()
        audio_merged = bytearray()

        for i in range(len(results)):
            audio_merged += results[i]["audio"]
            video_merged += results[i]["video"]
        audio_path = f"{self.__title}.{self.__video_information["audio"].ext() if not audio_extension else audio_extension}"
        video_path = f"{self.__title}.{self.__video_information["video"].ext()}"

        with open(audio_path, "wb") as f:
            f.write(audio_merged)

        with open(video_path, "wb") as f:
            f.write(video_merged)

        Logger.log(f"Wrote {len(audio_merged) / MB_CONVERSION_MULT} MB for the AUDIO.")
        Logger.log(f"Wrote {len(video_merged) / MB_CONVERSION_MULT} MB for the VIDEO.")
        # TODO: write the mp4 file by combining frame data and audio data

    def title(self):
        return self.__title
            
    def url(self):
        return self.__url

    def __get_resolution_height(self, resolution: str):
        times_index = resolution.find("x")
        if times_index != -1:
            return resolution[times_index + 1:]
        
        p_index = resolution.find("p")
        if p_index != -1:
            return resolution[:p_index]

        raise Exception("Resolution is ill-formed")