from datetime import datetime
from os import path

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from server.store import is_sqlite_db, Store

server_db = path.join('server', 'db', 'server.sqlite')
client_db = path.join('..', 'models', 'db', 'client.sqlite')
print(path.abspath(server_db), is_sqlite_db(server_db))

Base = declarative_base()


class ServerStore(Store):

    def __init__(self):
        self.db = server_db
        super().__init__(self.db)
        Base.metadata.create_all(self.engine)

    def get_client(self, client):
        return self.session.query(Client).filter_by(clientName=client.clientName).first()

    def get_or_create(self, client):
        if not self.session.query(Client).filter_by(clientName=client.clientName).first():
            self.session.add(client)
        return client

    def get_contacts(self, client):
        _contacts = self.session.query(ContactsList).filter(ContactsList.clientName == client.clientName).all()
        _contacts = [c.contactName for c in _contacts]
        return _contacts

    def add_contact(self, client, contact):
        if not self.session.query(ContactsList).filter(
                        ContactsList.clientName == client.clientName,
                        ContactsList.contactName == contact.clientName).first():
            self.session.add(ContactsList(client.clientName, contact.clientName))
            return True

    def del_contact(self, client, contact):
        _query = self.session.query(ContactsList).filter(
            ContactsList.clientName == client.clientName,
            ContactsList.contactName == contact.clientName).first()
        if _query:
            self.session.delete(_query)
            return True
        else:
            return False

    def upd_history(self, client, ipAddress):
        self.session.add(ClientHistory(client.clientName, ipAddress))
        return True


class Client(Base):
    __tablename__ = 'clients'

    def __init__(self, client):
        if isinstance(client, dict):
            self.clientName = client.get('account_name')
            self.clientPassword = client.get('password')
            self.clientInfo = client.get('status')
        elif isinstance(client, str):
            self.clientName = client
            self.clientPassword = None
            self.clientInfo = None

    def __repr__(self):
        return self.clientName

    clientId = Column(Integer, primary_key=True)
    clientName = Column(String, unique=True, nullable=False)
    clientPassword = Column(String)
    clientInfo = Column(String)
    history = relationship('ClientHistory', backref='client_')


class ContactsList(Base):
    __tablename__ = 'contacts'

    def __init__(self, client, contact):
        self.clientName = client
        self.contactName = contact

    def __repr__(self):
        return self.contactName

    id = Column(Integer, primary_key=True)
    clientName = Column(ForeignKey(Client.clientName))
    contactName = Column(ForeignKey(Client.clientName))


class ClientHistory(Base):
    __tablename__ = 'history'

    def __init__(self, client, ipAddress, dateTime=datetime.utcnow()):
        self.clientName = client
        self.ipAddress = '{}:{}'.format(*ipAddress)
        self.dateTime = dateTime

    id = Column(Integer, primary_key=True)
    clientName = Column(ForeignKey(Client.clientName))
    ipAddress = Column(String)
    dateTime = Column(DateTime)


# if __name__ == '__main__':
#     test_user = Client('testuser_name', 'testpwd')
#     # user = Client('user', 'pwd')
#     user = Client('newUser', 'Im here')
#     user1 = Client('user1', 'pwd1')
#     user2 = Client('user2', 'pwd2')
#     user3 = Client('user3', 'pwd3')
#
#     with ServerStore() as sstore:
#         sstore.get_or_create(test_user)
#         sstore.get_or_create(user1)
#         sstore.get_or_create(user2)
#         sstore.get_or_create(user3)
