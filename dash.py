class Dash:
    def __init__(self, name):
        self.name = name
        self.tabs = {}

    def construct(self, name):
        return Dash(name)

    def __getitem__(self, key):
        return self.tabs.get(key)

    def __setitem__(self, key, tab):
        self.tabs[key] = tab

    def __delitem__(self, key):
        del self.tabs[key]
