from keydnn.utilities import KeyResponse
from typing import Callable
from functools import wraps
import requests

API_KEY = "4f9f1996be5cc26124a5ab97fed0074222948ec0a33ac3faf76080dd7e186d74"

def mi2s_microservice(api_token: str) -> Callable:
    assert isinstance(api_token, str)
    def _mi2s_microservice(function: Callable) -> Callable:
        assert callable(function)
        @wraps(function)
        def call_mi2s_microservice(sentence: str) -> KeyResponse:
            assert isinstance(sentence, str)
            try:
                response = requests.post("https://140.116.245.149:7749/infer", 
                    json = { "data" : sentence, "api-key" : api_token }, 
                    timeout = 5,
                    verify = False
                )
                if (response.status_code != 200):
                    return KeyResponse(False, "Request to Mi2S Microservice Hub resulted in HTTP status code: {}".format(response.status_code))
                return KeyResponse(True, function(response.json()))
            except KeyboardInterrupt:
                raise
            except requests.exceptions.Timeout:
                return KeyResponse(False, "Connection to the Mi2S Microservice Hub timed out.")
            except Exception:
                return KeyResponse(False, "An unexpected error occurred while processing your request.")
        return call_mi2s_microservice
    return _mi2s_microservice

@mi2s_microservice(API_KEY)
def call_api(response_json: dict) -> KeyResponse:
    return response_json["message"]["answer"]

if __name__ == "__main__":

    input_data: str = "庫魯化錠有沒有毒性？"

    api_response: KeyResponse = call_api(sentence=input_data)

    print("API Success: {}".format(api_response["status"]))

    print("API Response: {}".format(api_response["message"]))