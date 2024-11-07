from widgets.chat import Chat
from widgets.db_query import DBQuery
from widgets.filewatch import FileWatch
from widgets.message_route import MessageRotate
from widgets.sys_stat import SysStat
from widgets.timer import Timer
from widgets.url_getter import URLGetter

url_getter = URLGetter(title="World Time API")
url_getter.env['url'] = "http://worldtimeapi.org/api/timezone/Europe/Istanbul"

message_rotate = MessageRotate(title="Motivational Quotes")
message_rotate.env['messages'] = ["Live the moment.", "Work hard. Stay humble", "Be a voice, not an echo"]

db_query = DBQuery(title="Database Query")
db_query.env['query'] = "SELECT * FROM example_table"

timer = Timer(title="Countdown Timer")
timer.env['value'] = 30

file_watch = FileWatch(title="Log Monitor")
file_watch.env['filename'] = "data/logfile.txt"
file_watch.env['numberoflines'] = 5

sys_stat = SysStat(title="System Statistics")

chat = Chat(title="Global Chat")
chat.trigger("submit", "Hello, everyone!")
chat.trigger("submit", "Hello, everyone!")

print(url_getter.refresh())
print(message_rotate.refresh())
print(db_query.refresh())
print(timer.refresh())
print(file_watch.refresh())
print(sys_stat.refresh())
print(chat.refresh())
