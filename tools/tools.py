from tools.web.WebTool import SearchTool, google_search
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

class GoogleSearch:
    def __init__(self) -> None:
        pass
    def GoogleSearchTool(self, query):
        api_key = 'AIzaSyCgyLeK_yXOrKy0_asD-NpMuAxVv9gJuvU'
        cse_id = 'a4decc2606f9c4cef'
        search_results = google_search(query, api_key, cse_id)

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

class HuggingfaceAPIBart:
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key must be provided")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def query(self, payload):
        if not payload:
            raise ValueError("Payload must be provided")
        
        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        except RequestException as e:
            # Handle specific exceptions for network issues, timeout, etc.
            print(f"An error occurred: {e}")
            return None
        
        try:
            # We expect a JSON response. If the response isn't JSON, this will raise a ValueError
            response_data = response.json()
        except ValueError as e:
            print(f"Invalid JSON response: {e}")
            return None

        # At this point, the request was successful, and response is JSON
        if 'error' in response_data:
            # API might send back JSON with an error message
            print(f"API Error: {response_data['error']}")
            return None

        return response_data

def SearchStable(query):
    try:
        data = GoogleSearch().GetData(query)

        api_key = "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"  # This should be kept secret and safe.
        huggingface_api = HuggingfaceAPIBart(api_key)

        output = huggingface_api.query({
            "inputs": data
        })
        if output == None:
            return data
        else:
            return output
    except Exception as e:
        return f"Error: {e}"

def GetLinkData(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from the soup object, e.g., get text from the <body> tag
            page_text = soup.body.get_text(separator=' ', strip=True)
            return page_text
        else:
            print(f"Failed to retrieve {link}, status code: {response.status_code}")
            return f"Failed to retrieve {link}, status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return f"Request failed: {e}"
    