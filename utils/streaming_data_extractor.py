import json
from requests import Response
from utils.logger import Logger, Level

class StreamingDataExtractor:
    def __init__(self):
        pass

    def extract(self, response: Response) -> dict:
        return self.__extract_initial_player_response_json(response.text)["streamingData"]
    
    def __extract_initial_player_response_json(self, response_text: str) -> str:
        yt_initial_player_response_var = "var ytInitialPlayerResponse = " # JS variable for the JSON object containing the streaming data.

        start_of_json_obj: int = response_text.find(yt_initial_player_response_var)
        if (start_of_json_obj == -1):
            raise Logger().log(exception=Exception("Variable: \"ytInitialPlayerResponse\", has not been found"), level=Level.ERROR, content=response_text)

        raw_json_obj: str = response_text[start_of_json_obj + len(yt_initial_player_response_var):]

        end_of_json_obj: int = raw_json_obj.find("};")
        if (end_of_json_obj == -1):
            raise Logger().log(exception=Exception("\"ytInitialPlayerResponse\" JSON object is ill-formed"), level=Level.ERROR, content=raw_json_obj)

        return json.loads(raw_json_obj[:end_of_json_obj + 1])