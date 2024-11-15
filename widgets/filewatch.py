from features.component import Component


class FileWatch(Component):
    def __init__(self):
        super().__init__("FileWatch", "File Watcher", 50, 50)
        self.env['filename'] = "data/file.txt"
        self.env['lines_to_display'] = 3
        self.file_content = []
        self.last_read_line_count = 0
        self.initialize()

    def initialize(self):
        if self.env['filename']:
            with open(self.env['filename'], 'r') as file:
                lines = file.readlines()
                self.last_read_line_count = len(lines)

    def refresh(self):
        if self.env['filename']:
            with open(self.env['filename'], 'r') as file:
                lines = file.readlines()
                new_lines = lines[self.last_read_line_count:]
                if new_lines:
                    self.file_content.extend(new_lines)
                    self.last_read_line_count = len(lines)


        else:
            self.file_content = []

    def view(self):
        # If new lines are added, show them
        if self.file_content:
            new_lines = ''.join(self.file_content[-self.env['lines_to_display']:])
            return f"File Watcher: New lines added:\n{new_lines}"
        else:
            return "No new lines found."
