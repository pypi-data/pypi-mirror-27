from rethinkdb import *  # noqa
from .net import Connection, ConnectionPool  # noqa


def set_loop_type_curio():
    import rethinkdb.net
    rethinkdb.net.connection_type = Connection
