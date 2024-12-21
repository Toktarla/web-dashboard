from threading import Condition, RLock

class Component:
    def __init__(self, name, title, height, width):
        self.name = name
        self.title = title
        self.height = height
        self.width = width
        self.env = {}
        self.param = {}
        self.events = []
        self.refresh_interval = 0
        self.mutex = RLock()
        self.conditions = {}

    def view(self):
        return f"Component: {self.title} ({self.name})"

    def trigger(self, event):
        if event in self.events:
            getattr(self, event)()
        else:
            raise ValueError(f"Event '{event}' not implemented")

    def refresh(self):
        pass

    def register(self, user): 
        with self.mutex:
            cond = Condition(self.mutex)
            self.conditions[user] = cond
            return cond

    def unregister(self, user):
        with self.mutex:
            if user in self.conditions:
                del self.conditions[user]

    def notify(self, message):
        with self.mutex:
            for cond in self.conditions.values():
                cond.notify_all()
