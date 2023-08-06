import socket
import time
import os
from socketserver import BaseRequestHandler
from socketserver import TCPServer, ThreadingMixIn
from sys import argv
from aemessenger.Server.servercontroller import JIMServerController
from aemessenger.JIM.jimresponse import JIMResponse


class ThreadingJIMServer(ThreadingMixIn, TCPServer):
    def __init__(self, server_address, request_handler):
        super().__init__(server_address, request_handler, True)
        self.clients = list()
        self.usernames = list()
        self.controller = JIMServerController()

    def add_client(self, client, username):
        self.clients.append(client)
        self.usernames.append(username)

    def remove_client(self, client):
        index = self.clients.index(client)
        del self.clients[index]
        del self.usernames[index]

    def get_client_by_username(self, username):
        index = self.usernames.index(username)
        return self.clients[index]

    def get_username_by_client(self, client):
        index = self.clients.index(client)
        return self.usernames[index]

    allow_reuse_address = True
    max_children = 100


class JIMRequestHandler(BaseRequestHandler):
    def setup(self):
        """
        Подключить нового клиента и узнать его имя.
        Клиент после подключения должен сразу отправить presense-сообщение
        """
        print('Client connected:', self.client_address)
        presense_data = self.request.recv(1024)  # получить имя
        response, action = self.server.controller.parse_client_message(presense_data.decode('utf-8'), None)
        if action.usernames[0] in self.server.usernames:  # Если клиент с таким логином уже подключен
            uid = response.uid
            response = JIMResponse(409, 'Username already exists', None, None, uid)
            print('Error:', self.client_address, 'tried to use username:', action.usernames[0])
            self.server.add_client(self, action.usernames[0] + uid)
        else:
            print(self.client_address, 'got username:', action.usernames[0])
            self.server.add_client(self, action.usernames[0])  # записать имя и клиента
            # Проверить, что клиент есть в базе, если нет, то добавить
            if not self.server.controller.user_exist(action.usernames[0]):
                self.server.controller.add_user_to_db(action.usernames[0], None)
        self.request.sendall(response.utf8)  # отправить ответ

    def handle(self):
        if isinstance(self.request, socket.socket):
            # работа с потоком
            try:
                while True:
                    data = self.request.recv(1024)
                    if not data:
                        print('{0} disconnected'.format(self.client_address))
                        break
                    print(data.decode('utf-8'))
                    response, action = self.server.controller.parse_client_message(data.decode('utf-8'),
                                                                                   self.server.get_username_by_client(self))
                    if action:
                        if action.action == 'quantity':  # Шлём контакты
                            for r in response:
                                self.request.sendall(r.utf8 + '\r\n\r\n'.encode('utf-8'))
                        elif action.action == 'presence':  # Отвечаем на презенс
                            self.request.sendall(response.utf8)
                        elif action.action == 'msg':  # рассылаем сообщения
                            for username in action.usernames:
                                try:
                                    client = self.server.get_client_by_username(username)
                                    client.request.sendall(action.msg.encode('utf-8'))
                                except ValueError as e:
                                    # Не нашли товарища онлайн
                                    uid = response.uid
                                    response = JIMResponse(404, 'Username not found online', None, None, uid)
                            self.request.sendall(response.utf8)  # TODO если сообщение для чатика, то вылетит эксепшн
                    else:
                        self.request.sendall(response.utf8)
            except Exception as e:
                print()
                print('{0} expected an error'.format(self.client_address))
                raise e

    def finish(self):
        self.server.remove_client(self)


def checkcmdargs():
    args = ['localhost', 7777]
    args[0] = argv[1] if len(argv) > 1 else 'localhost'
    args[1] = int(argv[2]) if len(argv) > 2 else 7777
    return args


def mainloop():
    address, port = checkcmdargs()
    serv = ThreadingJIMServer((address, port), JIMRequestHandler)
    print('Сервер запущен в {0}'.format(time.ctime(time.time())))
    serv.serve_forever()

if __name__ == '__main__':
    mainloop()
