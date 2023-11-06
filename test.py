from tools.web.WebTool import SearchTool, google_search

api_key = 'AIzaSyCgyLeK_yXOrKy0_asD-NpMuAxVv9gJuvU'
cse_id = 'a4decc2606f9c4cef'
search_results = google_search('Python', api_key, cse_id)

for item in search_results.get('items', []):
    print(item['link'])