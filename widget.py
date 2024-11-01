from component import Component


class Widget(Component):
    def __init__(self, name, title, height=100, width=100):
        self.name = name
        self.title = title
        self.height = height
        self.width = width
        self.env = {}
        self.param = {}
        self.events = []
        self.refresh_interval = 0

    def view(self):
        return f"{self.name}: {self.title} ({self.height}x{self.width})"

    def trigger(self, event):
        if event in self.events:
            getattr(self, event)()
        else:
            raise ValueError(f"Event {event} not supported")