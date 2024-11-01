from widget import Widget


class URLGetter(Widget):
    def __init__(self, title):
        super().__init__("URLGetter", title)
        self.env['url'] = ""

    def desc(self):
        return f"URLGetter for {self.env.get('url')}"


class MessageRotate(Widget):
    def __init__(self, title):
        super().__init__("MessageRotate", title)
        self.env['messages'] = []

    def desc(self):
        return f"MessageRotate showing: {self.env.get('messages')[0] if self.env['messages'] else 'No messages'}"


class Timer(Widget):
    def __init__(self, title):
        super().__init__("Timer", title)
        self.env['value'] = 0
        self.events = ['start', 'stop', 'reset']

    def desc(self):
        return f"Timer set to {self.env['value']} seconds"


class Chat(Widget):
    def __init__(self, title):
        super().__init__("Chat", title)
        self.param['mess'] = ""
        self.env['messages'] = []
        self.events = ['submit']

    def desc(self):
        return "Chat with messages"
