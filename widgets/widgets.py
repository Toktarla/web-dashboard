import requests
import sqlite3
import time
import psutil
import os

from widget import Widget


class URLGetter(Widget):
    def __init__(self, title="URL Getter"):
        super().__init__(name="URLGetter", title=title)
        self.env['url'] = ""
        self.content = ""

    def fetch_content(self):
        try:
            response = requests.get(self.env['url'])
            self.content = response.text
        except Exception as e:
            self.content = f"Failed to fetch URL: {e}"

    def refresh(self):
        self.fetch_content()
        return f"URL Content: {self.content}"


class MessageRotate(Widget):
    def __init__(self, title="Message Rotate"):
        super().__init__(name="MessageRotate", title=title)
        self.env['messages'] = []
        self.current_index = 0
        self.events.append('refresh')

    def refresh(self):
        if self.env['messages']:
            self.current_index = (self.current_index + 1) % len(self.env['messages'])
            return f"Message: {self.env['messages'][self.current_index]}"
        return "No messages available."


class DBQuery(Widget):
    def __init__(self, title="DB Query"):
        super().__init__(name="DBQuery", title=title)
        self.env['query'] = ""
        self.db_path = "example.db"
        self.events.append('refresh')

    def execute_query(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(self.env['query'])
                return cursor.fetchall()
        except Exception as e:
            return f"Query failed: {e}"

    def refresh(self):
        results = self.execute_query()
        return f"Query Results: {results}"


class Timer(Widget):
    def __init__(self, title="Timer"):
        super().__init__(name="Timer", title=title)
        self.env['value'] = 0
        self.remaining_time = self.env['value']
        self.is_running = False
        self.events.append('start')
        self.events.append('pause')
        self.events.append('reset')

    def trigger(self, event):
        if event == 'start':
            self.is_running = True
        elif event == 'pause':
            self.is_running = False
        elif event == 'reset':
            self.remaining_time = self.env['value']
            self.is_running = False
        else:
            super().trigger(event)

    def refresh(self):
        if self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1
        return f"Timer: {self.remaining_time} seconds remaining"


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


class SysStat(Widget):
    def __init__(self, title="System Stats"):
        super().__init__(name="SysStat", title=title)
        self.events.append('refresh')

    def refresh(self):
        cpu_load = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()
        return f"CPU Load: {cpu_load}%\nMemory Usage: {mem_info.percent}%"


class Chat(Widget):
    def __init__(self, title="Chat"):
        super().__init__(name="Chat", title=title)
        self.messages = []
        self.events.append('submit')

    def trigger(self, event, message=""):
        if event == "submit":
            self.messages.append(message)
        else:
            super().trigger(event)

    def refresh(self):
        return f"Chat Messages:\n" + "\n".join(self.messages)
