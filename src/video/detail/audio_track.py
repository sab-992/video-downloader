from src.video.detail.track import Track


class AudioTrack(Track):
    def __init__(self, information: dict):
        super().__init__(information)

    def codec(self) -> str:
        return self.__info.get("acodec", "")