from features.widget import Widget


class Chat(Widget):
    def __init__(self, title="Chat"):
        super().__init__(name="Chat", title=title)
        self.messages = []
        self.events.append('submit')

    def trigger(self, event, message=""):
        if event == "submit":
            self.messages.append(message)
        else:
            super().trigger(event)

    def refresh(self):
        return f"Chat Messages:\n" + "\n".join(self.messages)
