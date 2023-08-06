# Jimmer

Simple messenger (server+client) written on Python. Message transfer based on JSON IM Protocol.

## Installation
From pypi (using pip):

    pip install jimmer

## Server start:

    python server_start.py

#### Usage:
server_start.py [-h] [-a ADDRESS] [-p PORT]

optional arguments:

-h, --help  show this help message and exit

-a ADDRESS  Server ip address. Optional.

-p PORT     Server port. Optional.


## Client start

    python client_start.py

Client could be started with any user name.
Contact could be added only from them which already exist in server database.
There're next users already in server database: newUser, newUser1, newUser2.

## Dependencies

``Python 3`` ``PyQt5`` ``SQLAlchemy``

## Pypi package

https://pypi.python.org/pypi/jimmer
