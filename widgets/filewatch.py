from features.component import Component
import os


class FileWatch(Component):
    def __init__(self):
        super().__init__("FileWatch", "File Watcher", 50, 50)
        self.env['filename'] = "data/file.txt"
        self.env['lines_to_display'] = 3
        self.file_content = []
        self.last_read_line_count = 0
        self.max_width = 80
        self.initialize()

    def initialize(self):
        if self.env['filename'] and os.path.exists(self.env['filename']):
            with open(self.env['filename'], 'r') as file:
                self.last_read_line_count = sum(1 for _ in file)

    def refresh(self):
        if not self.env['filename'] or not os.path.exists(self.env['filename']):
            self.file_content = ["File not found"]
            return

        with open(self.env['filename'], 'r') as file:
            lines = file.readlines()
            current_line_count = len(lines)
            
            if current_line_count > self.last_read_line_count:
                new_lines = lines[self.last_read_line_count:]
                self.file_content.extend(new_lines)
                self.last_read_line_count = current_line_count

    def view(self):
        if not self.file_content:
            return "No changes detected"

        header = f"File: {self.env['filename']}\n" + "-" * self.max_width
        recent_changes = self.file_content[-self.env['lines_to_display']:]
        formatted_changes = [
            f"[NEW] {line.strip()}" for line in recent_changes
        ]
        
        return f"{header}\nRecent Changes:\n" + "\n".join(formatted_changes)
