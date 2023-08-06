import json
import time


class JIMResponse:
    # на будущее
    response_ids = {'100': 'Basic Notification', '101': 'Important Notification',
                    '200': 'OK', '201': 'Object Created', '202': 'Accepted',
                    '400': 'Malformed JSON', '401': 'Not Authorised', '402': 'Wrong Login/Password',
                    '403': 'Forbidden', '404': 'Not Found', '409': 'Connection Conflict',
                    '410': 'User Gone', '500': 'Server Error',
                    }

    def __init__(self, code, text='', resp_time=None, quantity=None, uid='', data=None):
        self.response = str(code)  # можно передавать число или строку
        if quantity is not None:  # Возврат количества контактов клиенту
            self.quantity = str(quantity)
            return

        if resp_time is None:  # когда клиент читает ответ сервера, у него уже есть отметка времени
            self.time = time.ctime(time.time())
        else:
            self.time = resp_time

        if self.response[0] == '1' or self.response[0] == '2':
            self.alert = text
        else:
            self.error = text

        if data is not None:
            self.data = data
        self.uid = uid

    @property
    def json(self):
        fields = self.__dict__
        j = {c: fields[c] for c in fields if fields[c] is not None}
        return json.dumps(j)

    @property
    def utf8(self):
        return self.json.encode('utf-8')

    @staticmethod
    def fromjson(json_resp):
        try:
            parsed_resp = json.loads(json_resp)
        except ValueError:
            return None
        if 'alert' in parsed_resp or 'error' in parsed_resp:
            text = parsed_resp['alert'] if 'alert' in parsed_resp else parsed_resp['error']
        else:
            text = None
        time = parsed_resp['time'] if 'time' in parsed_resp else None
        quantity = parsed_resp['quantity'] if 'quantity' in parsed_resp else None
        uid = parsed_resp['uid'] if 'uid' in parsed_resp else None
        data = parsed_resp['data'] if 'data' in parsed_resp else None
        response = JIMResponse(parsed_resp['response'], text, time, quantity, uid, data)
        return response

if __name__ == '__main__':
    resp = JIMResponse(300, 'Hello there', data='')
    print(resp.json)
    # print(resp.quantity)
    time.sleep(5)
    resp2 = JIMResponse.fromjson(resp.json)
    print(resp2.json)
    resp3 = JIMResponse(202, quantity=200)
    print(resp3.json)
