import threading
import heapq
from datetime import datetime, timedelta


class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.queue = []  # Min-heap for timers
        self.condition = threading.Condition()

    def add_timer(self, component, refresh_interval):
        with self.condition:
            next_refresh = datetime.now() + timedelta(seconds=refresh_interval)
            heapq.heappush(self.queue, (next_refresh, component))
            self.condition.notify()

    def run(self):
        while True:
            with self.condition:
                if not self.queue:
                    self.condition.wait()
                else:
                    now = datetime.now()
                    next_refresh, component = self.queue[0]

                    if now >= next_refresh:
                        heapq.heappop(self.queue)
                        component.refresh()
                        print(f"Component {component.name} refreshed")

                        self.add_timer(component, 5)
                    else:
                        self.condition.wait((next_refresh - now).total_seconds())
