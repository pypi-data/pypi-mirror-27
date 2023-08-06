from datetime import datetime
from os.path import join

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from server.store import Store

client_db = join('client', 'db', 'client.sqlite')

Base = declarative_base()


class ClientStore(Store):

    def __init__(self, db=client_db):
        self.db = db
        super().__init__(self.db)
        Base.metadata.create_all(self.engine)

    def get_or_create_contact(self, contact):
        if not self.session.query(ContactList).filter_by(contactName=contact).first():
            self.session.add(ContactList(contact))
        return contact

    def del_contact(self, contact):
        self.session.query(ContactList).filter_by(contactName=contact).delete()

    def clear_contacts(self):
        self.session.query(ContactList).delete()

    def add_message(self, message):
        self.session.add(MessageHistory(message))


class ContactList(Base):
    __tablename__ = 'contacts'

    def __init__(self, contact):
        self.contactName = contact

    contactId = Column(Integer, primary_key=True)
    contactName = Column(String, unique=True, nullable=False)
    contactMessages = relationship('MessageHistory', backref='contact_')


class MessageHistory(Base):
    __tablename__ = 'messages'

    def __init__(self, *args):
        self.contactName, self.message, _datetime = args[0]
        self.dateTime = datetime.utcfromtimestamp(_datetime)

    id = Column(Integer, primary_key=True)
    contactName = Column(ForeignKey(ContactList.contactName))
    message = Column(String)
    dateTime = Column(DateTime)
