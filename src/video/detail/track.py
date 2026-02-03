class Track:
    def __init__(self, information: dict):
        self.__info = information

    def headers(self) -> dict:
        return self.__info.get("http_headers", {})

    def size(self) -> int:
        return int(self.__info.get("filesize", -1))
    
    def url(self) -> str:
        return self.__info.get("url", "")