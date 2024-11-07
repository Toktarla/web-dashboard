from features.widget import Widget

class MessageRotate(Widget):
    def __init__(self, title="Message Rotate"):
        super().__init__(name="MessageRotate", title=title)
        self.env['messages'] = []
        self.current_index = 0
        self.events.append('refresh')

    def refresh(self):
        if self.env['messages']:
            self.current_index = (self.current_index + 1) % len(self.env['messages'])
            return f"Message: {self.env['messages'][self.current_index]}"
        return "No messages available."