from pathlib import Path

from features.component import Component

DATA_DIR = Path("./shared_files")
DATA_DIR.mkdir(exist_ok=True)


class FileShare(Component):
    def __init__(self):

        super().__init__("FileShare", "FileShare Widget", 50, 50)

    def upload(self, filename, content):
        file_path = DATA_DIR / filename
        with open(file_path, "w") as f:
            f.write(content)
        self.notify(f"File {filename} uploaded")

    def download(self, filename):
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, "r") as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File {filename} not found")

    def delete(self, filename):
        file_path = DATA_DIR / filename
        if file_path.exists():
            file_path.unlink()
            self.notify(f"File {filename} deleted")
        else:
            raise FileNotFoundError(f"File {filename} not found")
