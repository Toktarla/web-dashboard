from features.repo import Repo
from utils.db import create_db
from widgets.chat import Chat
from widgets.db_query import DBQuery
from widgets.filewatch import FileWatch
from widgets.message_route import MessageRotate
from widgets.sys_stat import SysStat
from widgets.timer import Timer
from widgets.url_getter import URLGetter
from widgets.db_update import DBUpdate
from widgets.file_share import FileShare
from tcp_server import TCPServer
from widgets.item import Item
import argparse
from observer import Observer

global_observer = Observer(4)

def main():
    # Attach users to the dashboard
    dashboard_id = Repo.create("MyPage")
    ogr = Repo.attach(dashboard_id, "onur")
    t1 = ogr.create("Personal")

    # Add rows to the Personal tab
    for _ in range(7):
        t1.newrow()

    # Place components in rows of the Personal tab
    t1.place(components["URLGetter"], 0)
    t1.place(components["MessageRotate"], 1)
    t1.place(components["Timer"], 2)
    t1.place(components["Chat"], 3)
    t1.place(components["DBQuery"], 4)
    t1.place(components["FileWatch"], 5)
    t1.place(components["SysStat"], 6)

    # Refresh tabs and print initial view
    print("Initial refresh:")
    t1.refresh()
    print(t1.view())

    print("Second refresh:")
    # Add message to the chat
    components["Chat"].param['mess'] = "Hello from Tolga!"
    components["Chat"].trigger("submit")

    # Stop the timer
    components["Timer"].trigger("stop")


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
    components["URLGetter"].env['url'] = "http://worldtimeapi.org/api/timezone/Europe/Istanbul"
    components["MessageRotate"].env['messages'] = [
        "Live the moment.",
        "Work hard. Stay humble.",
        "Be a voice, not an echo."
    ]
    components["Timer"].env['value'] = 30
    components["Timer"].trigger("start")
    components["Chat"].param['mess'] = "Hello from Onur!"
    components["Chat"].trigger("submit")
    components["DBQuery"].env['query'] = "SELECT * FROM users"
    components["FileWatch"].env['filename'] = "data/file.txt"
    components["FileWatch"].env['lines_to_display'] = 3

    # main()

    parser = argparse.ArgumentParser(description="Run the server with specified parameters.")
    parser.add_argument("--port", type=int, default=8008, help="Port number for the server.")
    args = parser.parse_args()

    server = TCPServer(args.port, "localhost", components, global_observer)
    server.run()
