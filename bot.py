import http.client
import json


class Bot:

    def __init__(self, token, api_url="api.telegram.org"):
        self.TOKEN = token
        self.API_URL = api_url
        self.QUERY_URL = "/bot" + self.TOKEN

    def connect(self):
        self.connection = http.client.HTTPSConnection(self.API_URL)

    def disconnect(self):
        self.connection.close()

    def _API_request(self, url, parameters):
        try:
            body = json.dumps(parameters)

            self.connection.request("POST",
                                    url,
                                    body,
                                    {"Content-Type": "application/json"})

            response = self.connection.getresponse().read()

            parsed = json.loads(response.decode('utf-8'))

            if "ok" in parsed and parsed["ok"] is True and "result" in parsed:
                return parsed["result"]

            else:
                print("API exception!")
                return None

        except http.client.HTTPException:
            print("Networking exception!")
            return None

        except json.JSONDecodeError:
            print("JSON decoding exception!")
            return None

        except TypeError:
            print("Type error!")
            return None

    def get_updates(self,
                    offset=None,
                    limit=None,
                    timeout=None,
                    allowed_updates=None):
        req_url = self.QUERY_URL + "/getUpdates"

        parameters = {}

        if offset is not None:
            parameters["offset"] = offset

        if limit is not None:
            parameters["limit"] = limit

        if timeout is not None:
            parameters["timeout"] = timeout

        if allowed_updates is not None:
            parameters["allowed_updates"] = allowed_updates

        ret = self._API_request(req_url, parameters)

        if ret is not None:
            return ret

        else:
            return []

    def send_message(self,
                     chat_id,
                     text,
                     parse_mode=None,
                     disable_web_page_preview=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     reply_markup=None):
        req_url = self.QUERY_URL + "/sendMessage"

        parameters = {"chat_id": chat_id, "text": text}

        if parse_mode is not None:
            parameters["parse_mode"] = parse_mode

        if disable_web_page_preview is not None:
            parameters["disable_web_page_preview"] = disable_web_page_preview

        if disable_notification is not None:
            parameters["disable_notification"] = disable_notification

        if reply_to_message_id is not None:
            parameters["reply_to_message_id"] = reply_to_message_id

        if reply_markup is not None:
            parameters["reply_markup"] = reply_markup

        ret = self._API_request(req_url, parameters)

        return ret
