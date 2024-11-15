from features.component import Component


class MessageRotate(Component):
    def __init__(self):
        super().__init__("MessageRotate", "Message Rotator", 50, 50)
        self.env['messages'] = []
        self.current_index = 0

    def refresh(self):
        if self.env['messages']:
            self.current_index = (self.current_index + 1) % len(self.env['messages'])

    def view(self):
        if self.env['messages']:
            return f"Message: {self.env['messages'][self.current_index]}"
        return "No messages available."
