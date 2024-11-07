from features.widget import Widget


class Timer(Widget):
    def __init__(self, title="Timer"):
        super().__init__(name="Timer", title=title)
        self.env['value'] = 0
        self.remaining_time = self.env['value']
        self.is_running = False
        self.events.append('start')
        self.events.append('pause')
        self.events.append('reset')

    def trigger(self, event):
        if event == 'start':
            self.is_running = True
        elif event == 'pause':
            self.is_running = False
        elif event == 'reset':
            self.remaining_time = self.env['value']
            self.is_running = False
        else:
            super().trigger(event)

    def refresh(self):
        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
        return f"Timer: {self.remaining_time} seconds remaining"
