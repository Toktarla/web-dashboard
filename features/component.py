import threading

from server import Agent

class Component:
    def __init__(self, name, title, height, width):
        self.name = name
        self.title = title
        self.height = height
        self.width = width
        self.env = {}
        self.param = {}
        self.events = []
        self.refresh_interval = 0
        self.observers = []
        self._lock = threading.Lock()
        
    def add_observer(self, observer):
        with self._lock:
            self.observers.append(observer)
            
    def remove_observer(self, observer):
        with self._lock:
            if observer in self.observers:
                self.observers.remove(observer)
                
    def notify_observers(self):
        with self._lock:
            for observer in self.observers:
                observer.component_updated(self)

    def view(self):
        return f"Component: {self.title} ({self.name})"

    def trigger(self, event, params=None):
        if event in self.events:
            with self._lock:
                if params:
                    # Get the current thread's agent
                    current_thread = threading.current_thread()
                    if isinstance(current_thread, Agent):
                        params = current_thread.component_params.get(self.name, {})
                    getattr(self, event)(params)
                else:
                    getattr(self, event)()
                self.notify_observers()
        else:
            raise ValueError(f"Event '{event}' not implemented")

    def refresh(self):
        with self._lock:
            self._refresh()
            self.notify_observers()
    
    def _refresh(self):
    # Actual refresh implementation
        pass
