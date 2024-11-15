from features.tab import Tab


class Dash:
    def __init__(self, name):
        self.name = name
        self.tabs = {}

    def create(self, tab_name):
        new_tab = Tab(tab_name)
        self.tabs[tab_name] = new_tab
        return new_tab

    def __getitem__(self, tab_name):
        return self.tabs[tab_name]

    def __setitem__(self, tab_name, tab):
        print(f"Adding Tab '{tab_name}' to Dash '{self.name}'.")
        self.tabs[tab_name] = tab

    def __delitem__(self, tab_name):
        print(f"Deleting Tab '{tab_name}' from Dash '{self.name}'.")
        del self.tabs[tab_name]