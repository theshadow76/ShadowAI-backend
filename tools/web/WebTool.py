from googlesearch import Search
import requests
import json

def google_search(query, api_key, cse_id, **kwargs):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key
    }
    params.update(kwargs)
    response = requests.get(url, params=params)
    return response.json()

class SearchTool:
    def __init__(self):
        self.GURL = "https://www.google.com/search?q="
        self.BURL = "https://www.bing.com/search?q="
    def GoogleAPI(self, query):
        result = Search(query)
        return result.results