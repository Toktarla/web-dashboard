from features.component import Component
import requests


class URLGetter(Component):
    def __init__(self):
        super().__init__("URLGetter", "URL Content Getter", 50, 50)
        self.env['url'] = None
        self.content = ""

    def refresh(self):
        if self.env['url']:
            try:
                response = requests.get(self.env['url'])
                self.content = f"Fetched content from {self.env['url']}: {response.text[:200]}"
            except requests.exceptions.RequestException as e:
                self.content = f"Failed to fetch URL: {e}"
        else:
            self.content = "No URL set."

    def view(self):
        return self.content
