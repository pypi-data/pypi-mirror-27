# coding: utf-8
from queue import Queue
from socket import *
from threading import Thread

from aemessenger.Log.log_config import configlogging

# from aemessenger.OLD.jimclient import get_presence_msg, get_user_to_chat_msg

logger = configlogging(False)
# ADDRESS = 'localhost'
# PORT = 7777
#
#
# @log(logger)
# def checkcmdargs():
#     args = [0, 0]
#     args[0] = argv[1] if len(argv) > 1 else ADDRESS
#     args[1] = int(argv[2]) if len(argv) > 2 else PORT
#     return args


class SendThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.is_stopped = False
        self.setDaemon(True)

    def run(self):
        while not self.is_stopped:
            msg = self.client.send_queue.get()
            print('sending:', msg)
            self.client.sock.send(msg.utf8)
            self.client.send_queue.task_done()


class RecieveThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.is_stopped = False
        self.setDaemon(True)

    def run(self):
        while not self.is_stopped:
            resp = self.client.sock.recv(1024)
            if resp:
                resp_json = resp.decode('utf-8')
                for r in resp_json.split('\r\n\r\n'):
                    if r == '':
                        continue
                    print('recieved:', r)
                    if 'msg' in r:  # Если это сообщение от пользователя/чата
                        self.client.msg_queue.put(r)
                    else:  # служебное сообщение сервера
                        self.client.resp_queue.put(r)


class SocketClient(object):
    def __init__(self, args):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.address, self.port = args
        self.sock.connect((self.address, self.port))
        self.send_queue = Queue()  # отправка сообщений на сервер
        self.resp_queue = Queue()  # сервисные сообщения от сервера
        self.msg_queue = Queue()  # сообщения пользователей/чатов с сервера
        self.is_alive = True  # TODO: использовать

        self.send_thread = SendThread(self)
        self.recv_thread = RecieveThread(self)

        self.send_thread.start()
        self.recv_thread.start()
        # self.start_async_tasks()

    def add_to_send_queue(self, msg):
        self.send_queue.put(msg)

    # async def get_responses(self):
    #     print('started')
    #     while True:
    #         resp = await self.sock.recv(1024)
    #         if resp:
    #             resp_json = resp.decode('utf-8')
    #             for r in resp_json.split('\r\n\r\n'):
    #                 if r == '':
    #                     continue
    #                 print('recieved:', r)
    #                 if 'msg' in r:  # Если это сообщение от пользователя/чата
    #                     self.msg_queue.put(r)
    #                 else:  # служебное сообщение сервера
    #                     self.resp_queue.put(r)
    #
    # async def send_messages(self):
    #     while True:
    #         msg = self.send_queue.get()
    #         print('sending:', msg)
    #         await self.sock.send(msg.utf8)
    #         self.send_queue.task_done()
    #
    # def start_async_tasks(self):
    #     eloop = asyncio.get_event_loop()
    #     asyncio.run_coroutine_threadsafe(self.send_messages(), eloop)
    #     asyncio.run_coroutine_threadsafe(self.get_responses(), eloop)

# if __name__ == '__main__':
#     client_test = SocketClient()
#     client_test.send_queue.put(get_presence_msg())
#
#     while client_test.is_alive:
#         text = input("Введите сообщение: ")
#         if text == 'quit':
#             break
#         client_test.send_queue.put(get_user_to_chat_msg(chatname='all', text=text))

# tm = self.sock.recv(1024)
# print(parse_server_message(tm.decode('ascii')))
# if mode == '-r':
#     while True:
#         tm = s.recv(1024)
#         if tm:
#             print(tm.decode('ascii'))  # пока никак не парсим, еще не утрясли кодирование протокола
# if mode == '-w':
#     while True:
#         text = input("Введите сообщение: ")
#         if text == 'quit':
#             break
#         s.send(get_user_to_chat_msg(chatname='all', text=text).encode('ascii'))
# self.sock.close()

