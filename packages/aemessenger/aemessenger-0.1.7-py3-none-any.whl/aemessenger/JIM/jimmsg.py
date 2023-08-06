import json
import time
from uuid import uuid1


# actions: authenticate, presence, quit, msg, join, leave, probe (server), avatar
# fields: action, time, user (account_name, status), type, to, from, encoding, message, room
class JIMMsg:
    def __init__(self, action):
        self.action = action
        self.time = time.ctime(time.time())
        self.uid = str(uuid1())

    @property
    def json(self):
        fields = self.__dict__
        j = {c: fields[c] for c in fields if fields[c] is not None}
        return json.dumps(j)

    def from_dict(self, values):
        for k, v in values.items():
            setattr(self, k, v)
        return self

    @property
    def utf8(self):
        return self.json.encode('utf-8')


class JIMAuthMsg(JIMMsg):
    def __init__(self, account_name='', password=''):
        super().__init__('authenticate')
        self.user = {'account_name': account_name, 'password': password}


class JIMPresenceMsg(JIMMsg):
    def __init__(self, account_name='', status='', msgtype=None):
        super().__init__('presence')
        self.user = {'account_name': account_name, 'status': status}
        self.type = msgtype


class JIMProbeMsg(JIMMsg):
    def __init__(self):
        super().__init__('probe')


class JIMQuitMsg(JIMMsg):
    def __init__(self):
        super().__init__('quit')


class JIMUserMsg(JIMMsg):
    def __init__(self, to='', acc_name='', message='', encoding='utf-8'):
        super().__init__('msg')
        self.to = to
        self.account = acc_name  # from - служебное слово
        self.encoding = encoding
        self.message = message


class JIMChatMsg(JIMMsg):
    def __init__(self, to='', acc_name='', message=''):
        super().__init__('msg')
        self.to = '#' + to
        self.account = acc_name  # from - служебное слово
        self.message = message


class JIMJoinChatMsg(JIMMsg):
    def __init__(self, room_name=''):
        super().__init__('join')
        self.room = '#' + room_name


class JIMLeaveChatMsg(JIMMsg):
    def __init__(self, room_name=''):
        super().__init__('leave')
        self.room = '#' + room_name


class JIMGetContactsMsg(JIMMsg):
    def __init__(self, user_id):
        super().__init__('get_contacts')
        self.user_id = user_id


class JIMSendContactListMsg(JIMMsg):
    def __init__(self, user_id):
        super().__init__('contact_list')
        self.user_id = user_id  # nickname


class JIMAddContactMsg(JIMMsg):
    def __init__(self, contact_id, user_id):
        super().__init__('add_contact')
        self.contact_id = contact_id  # nickname
        self.user_id = user_id


class JIMDelContactMsg(JIMMsg):
    def __init__(self, contact_id, user_id):
        super().__init__('del_contact')
        self.contact_id = contact_id  # nickname
        self.user_id = user_id


class JIMAvatarMsg(JIMMsg):
    """Если user_id соответствует имени отправившего клиента - то он постит картинку
    Если нет, то запрашивает картинку другого пользователя"""
    def __init__(self, username, data):
        super().__init__('avatar')
        self.user_id = username
        self.data = data


class JIMMessageBuilder:
    msg_classes = {'authenticate': 'JIMAuthMsg', 'presence': 'JIMPresenceMsg',
                   'quit': 'JIMQuitMsg', 'msg': ('JIMUserMsg', 'JIMChatMsg'),
                   'join': 'JIMJoinChatMsg', 'leave': 'JIMLeaveChatMsg',
                   'probe': 'JIMProbeMsg', 'get_contacts': 'JIMGetContactsMsg',
                   'contact_list': 'JIMSendContactListMsg', 'add_contact': 'JIMAddContactMsg',
                   'del_contact': 'JIMDelContactMsg', 'avatar': 'JIMAvatarMsg'
                   }

    @staticmethod
    def get_msg_from_json(json_msg):
        # Возвращает объект соответствующего класса сообщения в зависимости от action
        try:
            parsed_msg = json.loads(json_msg)  # Получить словарь атрибутов
        except ValueError:
            return None
        action = parsed_msg['action']
        if action == 'msg':  # сообщение пользователю или в чат
            if parsed_msg['to'][0] == '#':
                class_ = globals()[JIMMessageBuilder.msg_classes[action][1]]
            else:
                class_ = globals()[JIMMessageBuilder.msg_classes[action][0]]
        else:
            class_ = globals()[JIMMessageBuilder.msg_classes[action]]
        return class_().from_dict(parsed_msg)

if __name__ == '__main__':
    msg = JIMUserMsg('admin', 'user', 'hey man')
    js = msg.json
    print(js)
    msg = JIMMessageBuilder.get_msg_from_json(js)
    print(msg)
    print(msg.json)
    print(msg.utf8)