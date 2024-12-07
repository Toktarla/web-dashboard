import threading
import time
import heapq

class TimerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._queue = []
        self._lock = threading.Lock()
        self._running = True
        
    def add_component(self, component, interval):
        with self._lock:
            next_refresh = time.time() + interval
            heapq.heappush(self._queue, (next_refresh, component))
            
    def run(self):
        while self._running:
            with self._lock:
                now = time.time()
                while self._queue and self._queue[0][0] <= now:
                    _, component = heapq.heappop(self._queue)
                    component.refresh()
                    if component.refresh_interval > 0:
                        next_refresh = now + component.refresh_interval
                        heapq.heappush(self._queue, (next_refresh, component))
            
            time.sleep(1)
            
    def stop(self):
        self._running = False
