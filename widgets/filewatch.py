from features.widget import Widget
import os


class FileWatch(Widget):
    def __init__(self, title="File Watcher"):
        super().__init__(name="FileWatch", title=title)
        self.env['filename'] = ""
        self.env['numberoflines'] = 10
        self.file_data = []
        self.events.append('refresh')

    def refresh(self):
        if os.path.exists(self.env['filename']):
            with open(self.env['filename'], 'r') as file:
                lines = file.readlines()[-self.env['numberoflines']:]
                self.file_data = lines
        return f"File Watch Data:\n{''.join(self.file_data)}"
