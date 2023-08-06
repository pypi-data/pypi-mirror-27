from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os.path import isfile, getsize

SQLITE_HEADER_SIZE = 100
SQLITE_HEADER_STRING_LENGTH = 16
SQLITE_HEADER_DESCRIPTION = b'SQLite format 3\x00'


def is_sqlite_db(filename):
    if not isfile(filename) or getsize(filename) < SQLITE_HEADER_SIZE:
        return False
    with open(filename, 'rb') as db_file:
        header = db_file.read(SQLITE_HEADER_SIZE)
    return header[:SQLITE_HEADER_STRING_LENGTH] == SQLITE_HEADER_DESCRIPTION


class Store:

    def __init__(self, db):
        self.engine = create_engine('sqlite:///' + db)

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_db()

    def disconnect_db(self):
        self.session.commit()
        self.session.close()
