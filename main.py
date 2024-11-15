from features.repo import Repo
from utils.db import create_db
from widgets.chat import Chat
from widgets.db_query import DBQuery
from widgets.filewatch import FileWatch
from widgets.message_route import MessageRotate
from widgets.sys_stat import SysStat
from widgets.timer import Timer
from widgets.url_getter import URLGetter


def main():
    # Register all components
    Repo.register_component("URLGetter", URLGetter)
    Repo.register_component("MessageRotate", MessageRotate)
    Repo.register_component("Timer", Timer)
    Repo.register_component("Chat", Chat)
    Repo.register_component("DBQuery", DBQuery)
    Repo.register_component("FileWatch", FileWatch)
    Repo.register_component("SysStat", SysStat)

    # Create dashboard
    dashboard_id = Repo.create("MyPage")

    # Attach users to the dashboard
    ogr = Repo.attach(dashboard_id, "onur")
    tgr = Repo.attach(dashboard_id, "tolga")

    Repo.list()
    Repo.list_components()

    t1 = ogr.create("Personal")
    t2 = ogr.create("Business")

    t1.newrow()
    t1.newrow()
    t1.newrow()
    t1.newrow()
    t1.newrow()
    t1.newrow()
    t1.newrow()

    # Create and set environment variables for components
    a = Repo.create_component("URLGetter")
    a.env['url'] = "http://worldtimeapi.org/api/timezone/Europe/Istanbul"

    b = Repo.create_component("MessageRotate")
    b.env['messages'] = ["Live the moment.", "Work hard. Stay humble.", "Be a voice, not an echo."]

    c = Repo.create_component("Timer")
    c.env['value'] = 30
    c.trigger("start")

    # Create a single Chat component instance
    d = Repo.create_component("Chat")
    d.param['mess'] = "Hello from Onur!"
    d.trigger("submit")

    # Create and configure new components
    e = Repo.create_component("DBQuery")
    e.env['query'] = "SELECT * FROM users"

    f = Repo.create_component("FileWatch")
    f.env['filename'] = "data/file.txt"
    f.env['lines_to_display'] = 3

    g = Repo.create_component("SysStat")

    # Place components in rows of the Personal tab
    t1.place(a, 0)
    t1.place(b, 1)
    t1.place(c, 2)
    t1.place(d, 3)
    t1.place(e, 4)
    t1.place(f, 5)
    t1.place(g, 6)

    # Refresh tabs and print initial view
    print("Initial refresh:")
    t1.refresh()
    print(t1.view())

    print("Second refresh:")
    # Add message to the chat
    d.param['mess'] = "Hello from Tolga!"
    d.trigger("submit")

    # Stop the timer
    c.trigger("stop")

    # Add new lines
    with open(f.env['filename'], "a") as file:
        file.write("Lorem Ipsum\n")
        file.write("BEST\n")
        file.write("HEY\n")

    t1.refresh()
    print(t1.view())


if __name__ == "__main__":
    create_db()
    main()
