class Component:
    def desc(self):
        raise NotImplementedError

    def type(self):
        raise NotImplementedError

    def attrs(self):
        return {}

    def __getattr__(self, attr):
        if attr in self.attrs():
            return self.attrs()[attr]
        else:
            raise AttributeError(f"Attribute {attr} not found")

    def __setattr__(self, attr, value):
        if attr in self.attrs():
            self.attrs()[attr] = value
        else:
            super().__setattr__(attr, value)

    def draw(self):
        return "Component visual representation"

