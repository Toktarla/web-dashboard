from utils.db import create_db
from webservice.ws_server import WebSocketServer
import argparse

from widgets.message_route import MessageRotate
from widgets.url_getter import URLGetter
from widgets.timer import Timer
from widgets.chat import Chat
from widgets.db_query import DBQuery
from widgets.sys_stat import SysStat
from widgets.db_update import DBUpdate
from widgets.file_share import FileShare
from widgets.item import Item
from widgets.filewatch import FileWatch

if __name__ == "__main__":
    create_db()
    
    components = {
        "URLGetter": URLGetter(),
        "MessageRotate": MessageRotate(),
        "Timer": Timer(),
        "Chat": Chat(),
        "DBQuery": DBQuery(),
        "FileWatch": FileWatch(),
        "SysStat": SysStat(),
        "DBUpdate": DBUpdate(),
        "FileShare": FileShare(),
        "Item": Item("Item"),
    }
    
    # Configure environment variables for components
    # ... (keep existing component configuration)
    
    parser = argparse.ArgumentParser(description="Run the WebSocket server with specified parameters.")
    parser.add_argument("--port", type=int, default=8008, help="Port number for the server.")
    args = parser.parse_args()
    
    server = WebSocketServer(args.port, "localhost", components)
    server.run() 