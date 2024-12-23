from features.component import Component
import requests


class URLGetter(Component):
    def __init__(self):
        super().__init__("URLGetter", "URL Content Getter", 50, 50)
        self.env['url'] = None
        self.content = ""
        self.max_width = 80  # Maximum width for content display
        self.max_height = 10  # Maximum number of lines to display

    def refresh(self):
        if self.env['url']:
            try:
                response = requests.get(self.env['url'])
                content = response.text[:500]  # Limit content length
                # Format content into fixed-width lines
                formatted_lines = []
                for line in content.split('\n'):
                    while len(line) > self.max_width:
                        formatted_lines.append(line[:self.max_width])
                        line = line[self.max_width:]
                    formatted_lines.append(line)
                
                # Limit number of lines
                formatted_lines = formatted_lines[:self.max_height]
                self.content = "\n".join(formatted_lines)
            except requests.exceptions.RequestException as e:
                self.content = f"Error: {str(e)}"
        else:
            self.content = "No URL set"

    def view(self):
        header = f"URL: {self.env['url']}\n" + "-" * self.max_width
        return f"{header}\n{self.content}"
