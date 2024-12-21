from threading import Condition, RLock


class Observer:
    def __init__(self, N):
        self.values = [0 for _ in range(N)]
        self.mut = RLock()
        self.observers = {}

    def register(self, obj, vset):
        ''' A new condition is created per observer and it is notified when interest set of the observer changes '''
        with self.mut:
            cond = Condition(self.mut)
            self.observers[obj] = (vset, cond)
            return cond

    def unregister(self, obj):
        with self.mut:
            del self.observers[obj]

    def wait(self, obj):
        with self.mut:
            if obj in self.observers:
                self.observers[obj][1].wait()

    def __getitem__(self, idx):
        with self.mut:
            return self.values[idx]

    def __setitem__(self, idx, v):
        with self.mut:
            self.values[idx] = v
            # notify interested observers
            for obs in self.observers.values():
                if idx in obs[0]:
                    obs[1].notify()
