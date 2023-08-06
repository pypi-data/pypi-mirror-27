import json
import time
from aemessenger.Server.serverstorage import ContactList, ServerDB, Client
from aemessenger.JIM.jimresponse import JIMResponse
from aemessenger.JIM.jimmsg import JIMSendContactListMsg


class JIMServerController(object):
    def __init__(self):
        self.db = ServerDB()

    def parse_client_message(self, msg_bytes, from_username):
        timestr = time.ctime(time.time())
        # предварительно найти клиента в базе
        owner = None
        if from_username:
            owner = self.db.session.query(Client).filter_by(login=from_username).first()
        try:
            parsed_msg = json.loads(msg_bytes)
        except ValueError:
            print(msg_bytes)
            return JIMResponse(400, 'Incorrectly formed JSON', timestr, None, None), \
                   ServerAction('error', None, from_username)
        if 'action' in parsed_msg:
            action = parsed_msg['action']

            if action == 'presence':
                serv_action = ServerAction('presence', None, (parsed_msg['user']['account_name'],))
                return JIMResponse(200, 'OK', None, None, parsed_msg['uid']), serv_action

            elif action == 'msg':
                to = parsed_msg['to']
                if to.startswith('#'):
                    pass
                else:
                    serv_action = ServerAction('msg', msg_bytes, (to,))
                    response = JIMResponse(200, 'OK', timestr, None, parsed_msg['uid'])
                    return response, serv_action

            elif action == 'get_contacts':
                if owner:
                    # Найти контакты в базе и получить их id
                    contacts_query = self.db.session.query(ContactList).filter_by(ownerid=owner.id).all()
                    contacts_ids = [x.contactid for x in contacts_query]
                    # Получить объекты Client из id контактов
                    contacts = self.db.session.query(Client).filter(Client.id.in_(contacts_ids)).all()
                    serv_action = ServerAction('quantity', len(contacts), (from_username,))
                    responses = [JIMResponse(202, None, timestr, len(contacts), parsed_msg['uid'])]
                    for contact in contacts:
                        responses.append(JIMSendContactListMsg(contact.login))
                    return responses, serv_action
                else:
                    response = JIMResponse(404, 'User not found', timestr, None, parsed_msg['uid'])
                    return response, None

            elif action == 'add_contact':
                if owner:
                    # Найдем контакт в базе
                    user_query = self.db.session.query(Client).filter_by(login=parsed_msg['contact_id']).first()
                    if not user_query:
                        return JIMResponse(404, 'Contact not found', timestr, None, parsed_msg['uid']), None
                    # Проверим, что его нет в контакт листе клиента
                    contacts_query = self.db.session.query(ContactList)\
                        .filter_by(ownerid=owner.id)\
                        .filter_by(contactid=user_query.id)\
                        .first()
                    if contacts_query:  # контакт уже есть в базе данных
                        return JIMResponse(100, 'Contact already exists', timestr, None, parsed_msg['uid']), None
                    # Добавим контакт в контакт лист клиенту
                    contact = ContactList(owner.id, user_query.id)
                    self.db.session.add(contact)
                    self.db.session.commit()
                    return JIMResponse(200, 'OK', timestr, None, parsed_msg['uid']), None
                else:
                    response = JIMResponse(404, 'Please log in.', timestr, None, parsed_msg['uid']), None
                    return response, None

            elif action == 'del_contact':
                if owner:
                    user_query = self.db.session.query(Client).filter_by(login=parsed_msg['contact_id']).first()
                    if not user_query:
                        return JIMResponse(404, 'Contact not found', timestr, None, parsed_msg['uid']), None
                    self.db.session.delete(user_query)
                    self.db.session.commit()
                    return JIMResponse(200, 'OK', timestr, None, parsed_msg['uid']), None
                else:
                    response = JIMResponse(404, 'Please log in.', timestr, None, parsed_msg['uid'])
                    return response, None
        else:
            return JIMResponse(400, 'Incorrectly formed JSON', timestr, None, parsed_msg['uid']), None

    def get_server_response(self, response, alert, error):  # TODO: СТАРЫЙ КОД, УБРАТЬ
        msg = ''
        timestr = time.ctime(time.time())
        if alert:
            msg = json.dumps({'response': response, 'time': timestr, 'alert': alert})
        if error:
            msg = json.dumps({'response': response, 'time': timestr, 'error': error})
        return msg

    def user_exist(self, username):
        query = self.db.session.query(Client).filter_by(login=username).first()
        return True if query else False

    def add_user_to_db(self, username, info):
        if info is None:
            info = ''
        if username is None:
            return False
        self.db.add_user_to_db(username, info)



class ServerAction(object):
    def __init__(self, action, msg, usernames):
        self.action = action  # Что делать
        self.msg = msg  # Как делать
        self.usernames = usernames  # Кому делать
