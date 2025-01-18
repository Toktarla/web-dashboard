from features.component import Component
import requests
from bs4 import BeautifulSoup

class URLGetter(Component):
    def __init__(self):
        super().__init__("URLGetter", "URL Content Getter", 50, 50)
        self.env['url'] = None
        self.content = ""

    def refresh(self):
        if self.env['url']:
            try:
                response = requests.get(self.env['url'])
                if response.status_code == 200:
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract the title
                    title = soup.title.string if soup.title else "No title found"

                    # Extract the favicon (if available)
                    favicon = soup.find('link', rel='icon')
                    favicon_url = favicon['href'] if favicon else "No favicon found"

                    # Extract meta description
                    meta_description = soup.find('meta', attrs={'name': 'description'})
                    description = meta_description['content'] if meta_description else "No meta description found"

                    # Extract Open Graph title
                    og_title = soup.find('meta', attrs={'property': 'og:title'})
                    og_title_content = og_title['content'] if og_title else "No OG title found"

                    # Extract Open Graph image
                    og_image = soup.find('meta', attrs={'property': 'og:image'})
                    og_image_url = og_image['content'] if og_image else "No OG image found"

                    # Combine the extracted content into a formatted message
                    self.content = (
                        f"Title: {title}\n"
                        f"Favicon: {favicon_url}\n"
                        f"Meta Description: {description}\n"
                        f"OG Title: {og_title_content}\n"
                        f"OG Image: {og_image_url}"
                    )
                else:
                    self.content = f"Failed to fetch URL: Status code {response.status_code}"
            except requests.exceptions.RequestException as e:
                self.content = f"Failed to fetch URL: {e}"
        else:
            self.content = "No URL set."

    def view(self):
        return self.content
