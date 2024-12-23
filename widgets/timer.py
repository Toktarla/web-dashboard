import time
from features.component import Component


class Timer(Component):
    def __init__(self):
        super().__init__("Timer", "Timer Widget", 50, 50)
        self.env['value'] = 0
        self.remaining_time = 0
        self.running = False
        self.events.extend(['start', 'stop', 'reset', 'pause', 'play'])
        self.last_refresh_time = time.time()
        self.refresh_interval = 1  # Set refresh interval to 1 second

    def start(self):
        if not self.running:
            self.running = True
            self.remaining_time = int(self.env['value'])
            self.last_refresh_time = time.time()

    def stop(self):
        self.running = False

    def reset(self):
        self.remaining_time = int(self.env.get('value', 0))
        self.running = False

    def pause(self):
        self.running = False

    def play(self):
        if not self.running:
            self.running = True

    def refresh(self):
        current_time = time.time()
        if self.running and self.remaining_time > 0:
            elapsed = int(current_time - self.last_refresh_time)
            if elapsed >= 1:
                self.remaining_time = max(0, self.remaining_time - elapsed)
                self.last_refresh_time = current_time
                
            if self.remaining_time <= 0:
                self.running = False

    def view(self):
        if self.remaining_time > 0:
            status = "Running" if self.running else "Paused"
            return f"Timer [{status}]: {self.remaining_time} seconds remaining"
        return "Timer: Finished"
