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

    def view(self):
        return f"Component: {self.title} ({self.name})"

    def trigger(self, event):
        if event in self.events:
            getattr(self, event)()
        else:
            raise ValueError(f"Event '{event}' not implemented")

    def refresh(self):
        pass
