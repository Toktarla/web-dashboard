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

    def start(self):
        if not self.running:
            self.running = True
            self.remaining_time = int(self.env['value'])
            self.last_refresh_time = time.time()
            print(f"Timer started with {self.remaining_time} seconds.")

    def stop(self):
        self.running = False
        print("Timer stopped.")

    def reset(self):
        self.remaining_time = int(self.env.get('value', 0))
        self.running = False
        print(f"Timer reset to {self.remaining_time} seconds.")

    def pause(self):
        self.running = False
        print("Timer paused.")

    def play(self):
        if not self.running:
            self.running = True
            print("Timer resumed.")

    def refresh(self):
        # Refresh once every second
        if time.time() - self.last_refresh_time >= 1:
            self.last_refresh_time = time.time()
            if self.running and self.remaining_time > 0:
                self.remaining_time -= 1
            elif self.remaining_time <= 0:
                self.running = False
                print("Timer finished.")

    def view(self):
        if self.remaining_time > 0 and self.running:
            return f"Timer: {self.remaining_time} seconds remaining"
        else:
            return "Timer finished."
