# Initialize Repo and register components
from repo import Repo
from tab import Tab
from widgets.widgets import URLGetter, MessageRotate, Timer, Chat

repo = Repo()
repo.register_component("URLGetter", URLGetter)
repo.register_component("MessageRotate", MessageRotate)
repo.register_component("Timer", Timer)
repo.register_component("Chat", Chat)

# Create a Dash and add Tabs and Components
dash_id = repo.create("MyPage")
dash = repo.attach(dash_id, "user1")

tab1 = Tab()
tab1.newrow()
tab1.newrow()
url_getter = repo.create_component("URLGetter")
url_getter.env['url'] = "https://google.com"
tab1.place(url_getter, 0)

# List and view Dash and Tab layouts
print(tab1.view())
