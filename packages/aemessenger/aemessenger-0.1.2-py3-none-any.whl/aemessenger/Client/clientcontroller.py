import datetime
import json
import locale
import sys
from sys import argv
from aemessenger.Client.clientstorage import ClientDB, MsgHistory
from aemessenger.Client.socketclient import SocketClient
from aemessenger.JIM.jimmsg import JIMPresenceMsg, JIMGetContactsMsg, JIMAddContactMsg, JIMDelContactMsg, JIMUserMsg
from aemessenger.JIM.jimresponse import JIMResponse

ADDRESS = 'localhost'
PORT = 7777


class ClientController(object):
    def __init__(self, username):
        self.db = ClientDB(username)
        self.args = self.checkcmdargs()
        try:
            self.client = SocketClient(self.args)
        except ConnectionRefusedError as e:
            print(e)
            raise e
        self.username = username
        self.password = ''
        self.status = ''

    def checkcmdargs(self):
        args = [0, 0]
        args[0] = argv[1] if len(argv) > 1 else ADDRESS
        args[1] = int(argv[2]) if len(argv) > 2 else PORT
        return args

    def send_presense(self):
        if self.username == '':
            self.username = 'Guest'
        msg = JIMPresenceMsg(self.username, self.status)
        self.client.add_to_send_queue(msg)
        action = self.parse_server_response()
        print(action)
        if action.action == 'quit':
            return -1
        return 0

    def parse_server_response(self):
        resp_json = self.client.resp_queue.get()

        if 'response' in resp_json:
            resp = JIMResponse.fromjson(resp_json)
            if hasattr(resp, 'quantity'):  # Сервер говорит, сколько будет контактов
                return ClientAction('quantity', resp.quantity)
            elif resp.response == '200':
                return ClientAction(True, None)
            elif resp.response == '409':  # Имя не подходит
                return ClientAction('quit', None)
            elif resp.response == '404':  # Что-то не нашли, например сообщение не доставлено
                return ClientAction(False, None)
        elif 'action' in resp_json:
            resp = json.loads(resp_json)  # dict, можно реализовать from_json в jimmsg
            if resp['action'] == 'contact_list':
                return ClientAction('contact_list', resp['user_id'])
        self.client.resp_queue.task_done()  # TODO: поправить, программа сюда не заходит

    def get_contacts(self):
        msg = JIMGetContactsMsg(self.username)
        self.client.add_to_send_queue(msg)
        # Получить контакты с сервера
        quantity = -1
        while quantity != 0:
            action = self.parse_server_response()  # None если клиента нет в базе
            if action.action:
                print(action)
                if action.action == 'quantity':
                    quantity = int(action.value)
                elif action.action == 'contact_list':
                    self.db.add_contact(action.value)
                    quantity -= 1
            else:
                return -1
            self.client.resp_queue.task_done()
        return 0

    def add_contact(self, contact_name):
        msg = JIMAddContactMsg(contact_name, self.username)
        self.client.add_to_send_queue(msg)
        action = self.parse_server_response()
        if action.action is not True:
            pass  # TODO обработать ошибку
        self.get_contacts()

    def del_contact(self, contact_name):
        msg = JIMDelContactMsg(contact_name, self.username)
        self.client.add_to_send_queue(msg)
        action = self.parse_server_response()
        if action.action is not True:
            pass  # TODO обработать ошибку
        self.get_contacts()

    def send_user_msg(self, message, to):
        msg = JIMUserMsg(to, self.username, message)
        self.client.add_to_send_queue(msg)
        action = self.parse_server_response()
        if action.action is not True:
            return -1  # TODO обработать ошибку
        self.add_user_msg_to_db(msg)  # добавить сообщение в базу
        return 0

    def add_user_msg_to_db(self, jimmsg):
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        else:
            locale.setlocale(locale.LC_ALL, 'en_US')
        time = datetime.datetime.strptime(jimmsg.time, "%a %b %d %H:%M:%S %Y")
        msg = MsgHistory(None, jimmsg.to, jimmsg.account, jimmsg.message, time)
        self.db.add_msg_history(msg)


class ClientAction(object):
    """Объект класса говорит, что делать клиенту на основе ответов сервера"""
    def __init__(self, action, value):
        self.action = action  # что делать
        self.value = value  # с чем делать

    def __repr__(self):
        return str(self.action) + ': ' + str(self.value)


def mainloop():
    controller = ClientController('Dany')
    if controller.send_presense() < 0:
        return
    controller.get_contacts()
    controller.send_user_msg('hi', 'Dany')
    while True:
        print(controller.client.msg_queue.get())
        controller.client.msg_queue.task_done()

if __name__ == '__main__':
    mainloop()
