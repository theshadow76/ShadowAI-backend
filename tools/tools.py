from tools.web.WebTool import SearchTool, google_search
from bs4 import BeautifulSoup
import requests

class GoogleSearch:
    def __init__(self) -> None:
        pass
    def GoogleSearchTool(self, query):
        api_key = 'AIzaSyCgyLeK_yXOrKy0_asD-NpMuAxVv9gJuvU'
        cse_id = 'a4decc2606f9c4cef'
        search_results = google_search('Python', api_key, cse_id)

        data = []

        for item in search_results.get('items', []):
            data.append(item['link'])
        return data
    def GetData(self, query):
        links = self.GoogleSearchTool(query)
        page_texts = []

        for link in links:
            try:
                response = requests.get(link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract text from the soup object, e.g., get text from the <body> tag
                    page_text = soup.body.get_text(separator=' ', strip=True)
                    page_texts.append(page_text)
                else:
                    print(f"Failed to retrieve {link}, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

        return page_texts
