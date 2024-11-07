from features.widget import Widget
import requests


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