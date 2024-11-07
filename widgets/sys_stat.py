from features.widget import Widget
import psutil


class SysStat(Widget):
    def __init__(self, title="System Stats"):
        super().__init__(name="SysStat", title=title)
        self.events.append('refresh')

    def refresh(self):
        cpu_load = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()
        return f"CPU Load: {cpu_load}%\nMemory Usage: {mem_info.percent}%"
