class Tab:
    def __init__(self):
        self.layout = []

    def newrow(self, row=-1):
        if row == -1 or row >= len(self.layout):
            self.layout.append([])
        else:
            self.layout.insert(row, [])

    def place(self, component, row, col=-1):
        if row < len(self.layout):
            if col == -1:
                self.layout[row].append(component)
            else:
                self.layout[row].insert(col, component)

    def __getitem__(self, position):
        row, col = position
        return self.layout[row][col]

    def __delitem__(self, position):
        row, col = position
        del self.layout[row][col]

    def remove(self, component):
        for row in self.layout:
            if component in row:
                row.remove(component)

    def view(self):
        return "\n".join([", ".join([comp.desc() for comp in row]) for row in self.layout])

    def refresh(self):
        for row in self.layout:
            for comp in row:
                comp.refresh()
