class Tab:
    def __init__(self, name):
        self.name = name
        self.layout = []

    def newrow(self, row=-1):
        if row == -1 or row >= len(self.layout):
            self.layout.append([])
        else:
            self.layout.insert(row, [])

    def place(self, component, row, col=-1):
        if row >= len(self.layout):
            raise IndexError("Row index out of range")
        if col == -1:
            self.layout[row].append(component)
        else:
            while len(self.layout[row]) <= col:
                self.layout[row].append(None)
            self.layout[row][col] = component

    def __getitem__(self, position):
        row, col = position
        return self.layout[row][col]

    def __delitem__(self, position):
        row, col = position
        self.layout[row][col] = None

    def remove(self, component):
        for row in self.layout:
            if component in row:
                row.remove(component)

    def view(self):
        representation = [f"Tab: {self.name}"]
        for i, row in enumerate(self.layout):
            row_view = [comp.view() if comp else "Empty" for comp in row]
            representation.append(f"Row {i + 1}: {', '.join(row_view)}")
        return "\n".join(representation)

    def refresh(self):
        for row in self.layout:
            for comp in row:
                if comp:
                    comp.refresh()