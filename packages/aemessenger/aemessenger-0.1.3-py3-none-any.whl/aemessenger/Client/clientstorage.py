from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()


class ContactList(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    contactid = Column(Integer)
    username = Column(String)
    info = Column(String)

    def __init__(self, contactid, username, info):
        self.contactid = contactid
        self.username = username
        self.info = info

    def __repr__(self):
        return '<Contact({0}, {1})>'.format(self.username, self.info)


class MsgHistory(Base):
    __tablename__ = 'msghistory'
    id = Column(Integer, primary_key=True)
    chatid = Column(Integer, nullable=True)
    to_username = Column(String, nullable=True)
    from_username = Column(String)
    msg = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, chatid, to_username, from_username, msg, timestamp):
        self.chatid = chatid
        self.to_username = to_username
        self.from_username = from_username
        self.msg = msg
        self.timestamp = timestamp

    def __repr__(self):
        str_timestamp = self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
        if self.chatid:
            return '<MSG at{0} in chat {1}, user {2}: {3}'.format(
                str_timestamp, self.chatid, self.from_username, self.msg)
        else:
            return '<MSG at{0}, to user {1} from {2}: {3}'.format(
                str_timestamp, self.to_username, self.from_username, self.msg)


class ClientDB:
    def __init__(self, username):
        package_dir = os.path.abspath(os.path.dirname(__file__))
        db_dir = os.path.join(package_dir, 'client' + username + '.sqlite?check_same_thread=False')
        sqlite_path = ''.join(['sqlite:///', db_dir])
        # self.engine = create_engine('sqlite:///client' + username + '.sqlite?check_same_thread=False')
        self.engine = create_engine(sqlite_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_contact(self, username):
        exist = self.session.query(ContactList).filter_by(username=username).first()
        if not exist:
            contact = ContactList(username, username, '')
            self.session.add(contact)
            self.session.commit()

    def get_contacts(self):
        clients = self.session.query(ContactList).all()
        return [c.username for c in clients]

    def add_msg_history(self, msg):
        self.session.add(msg)
        self.session.commit()

def mainloop():
    clientdb = ClientDB('Dany')
    print('Session:', clientdb.session)


if __name__ == '__main__':
    mainloop()
