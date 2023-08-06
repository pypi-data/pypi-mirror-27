import requests

__version__ = '0.0.1'

s = requests.Session()

def get_listings_inner(offset=0, per_page=100, min_beds=0, min_baths=0):

    params = {
        "sort_field": "price", # ["created_at", "price", "total_images", "beds", "baths", "year_blt"]
        "sort_direction": "desc",
        "purchase_types": "buy",
        "region_id": "nj",
        "search_num_results": str(per_page),
        "search_start_offset": str(offset),
        "min_beds": str(min_beds),
        "min_baths": str(min_baths),
        # unsure what this is right now, but it makes the results match the website
        "origin_ids": "51967f537293b476e0000003",
    }

    response = s.get("https://queryserviceb.placester.net/search", params=params)
    response.raise_for_status()
    data = response.json()

    return data

def get_listings(per_page=100, **kwargs):

    data = get_listings_inner(per_page=per_page, **kwargs)
    
    meta = {
        'total_results': data['organic_results']['total_results'],
        'results_returned': data['organic_results']['results_returned'],
        'offset': 'offset',
        'search_result_ids': data['organic_results']['SEARCH_RESULT_IDS'],
    }
    
    for listing in data['organic_results']['search_results']:
        yield meta, listing

    total_results = data['organic_results']['total_results']

    for offset in range(per_page+1, total_results+per_page, per_page):
        data = get_listings_inner(offset=offset, per_page=per_page, **kwargs)
        meta = {
            'total_results': data['organic_results']['total_results'],
            'results_returned': data['organic_results']['results_returned'],
            'offset': offset,
            'search_result_ids': data['organic_results']['SEARCH_RESULT_IDS'],
        }
        for listing in data['organic_results']['search_results']:
            yield meta, listing

if __name__ == "__main__":

    for i, (meta, listing,) in enumerate(get_listings(min_beds=3, min_baths=2)):
        print(i, meta, listing['location'])
