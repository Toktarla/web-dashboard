from features.component import Component


class Chat(Component):
    def __init__(self):
        super().__init__("Chat", "Chat Box", 50, 50)
        self.lines = []
        self.events.append('submit')

    def submit(self):
        if 'mess' in self.param:
            self.lines.append(self.param['mess'])

    def view(self):
        return f"Chat Messages:\n" + "\n".join(self.lines)
