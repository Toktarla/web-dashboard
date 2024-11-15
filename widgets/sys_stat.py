from features.component import Component
import psutil


class SysStat(Component):
    def __init__(self):
        super().__init__("SysStat", "System Stats", "50", "50")
        self.stat = ""

    def refresh(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        self.stat = f"\nCPU Usage: {cpu_usage}%\nMemory Usage: {memory.percent}%"

    def view(self):
        return self.stat
