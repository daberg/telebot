import http.client
import json
import time


class AbstractClient:


    def __init__(self, token):

        self.TOKEN = token

        self.API_URL = "api.telegram.org"

        self.LP_TIMEOUT = 3600

        self.QUERY_BASE = "/bot" + self.TOKEN
        self.LONG_POLL = self.QUERY_BASE + "/getUpdates?timeout=" + str(self.LP_TIMEOUT)
        self.SEND_MESSAGE = self.QUERY_BASE + "/sendMessage"

        self.SEND_HEADERS = {"Content-Type": "application/json"}

        self.connection = http.client.HTTPSConnection(self.API_URL)


    def _get_updates(self, offset=None):

        req_url = self.LONG_POLL

        if offset is not None:
            req_url = req_url + "&offset=" + str(offset)

        self.connection.request("GET", req_url)
        response = self.connection.getresponse()

        content = response.read()

        if content is None:
            return None

        # The encoding should be utf-8, so we can parse directly with json
        json_content = json.loads(content)

        if "result" in json_content:
            return json_content["result"]

        else:
            return None


    def send_message(self, text, chat_id):

        req_url = self.SEND_MESSAGE

        json_content = json.dumps({"chat_id": chat_id, "text": text})

        self.connection.request(
                "POST",
                req_url,
                json_content,
                self.SEND_HEADERS)

        print(self.connection.getresponse().read())


    def start_polling(self):

        max_update_id = -1

        try:
            while True:

                if max_update_id < 0:
                    updates = self._get_updates()

                else:
                    updates = self._get_updates(max_update_id + 1)

                    if updates is not None:
                        max_update_id = -1

                if updates is not None:

                    for update in updates:

                        print("UPDATE_ID " + str(update['update_id']))

                        if update is None or 'message' not in update:
                            continue

                        self.handle_message(update['message'])

                        update_id = update['update_id']
                        if update_id > max_update_id:
                            max_update_id = update_id

        except KeyboardInterrupt:
            print("\nDetected interrupt from keyboard. Closing...")

        finally:
            self.connection.close()


    def handle_message(self, message):
        raise NotImplementedError
