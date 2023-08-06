import requests

__version__ = '0.0.2'

s = requests.Session()

def transform_listing(x):
    try:
        return {
            'id': x['rets']['mls_id'],
            'price': x['cur_data']['price'],
            'address': x['location']['address'],
            'county': x['location']['county'],
            'city': x['location']['locality'],
            'sqft': x['cur_data']['sqft'] if x['cur_data']['sqft'] else None,
            'bedrooms': x['cur_data']['beds'],
            'baths_full': x['cur_data']['baths'],
            'baths_part':  x['cur_data']['half_baths'],
            'year_blt': x['cur_data']['year_blt'],
            'lat': x['latitude'],
            'lng': x['longitude'],
        }
    except Exception as e:
        print(e)
        print(x)

def get_listings_inner(offset=0, per_page=100, min_beds='', min_baths='', max_price=''):

    params = {
        "sort_field": "price", # ["created_at", "price", "total_images", "beds", "baths", "year_blt"]
        "sort_direction": "desc",
        "purchase_types": "buy",
        "region_id": "nj",
        "search_num_results": str(per_page),
        "search_start_offset": str(offset),
        "min_beds": str(min_beds),
        "min_baths": str(min_baths),
        "max_price": str(max_price),
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
        yield meta, transform_listing(listing)

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
            yield meta, transform_listing(listing)

if __name__ == "__main__":

    for i, (meta, listing,) in enumerate(get_listings(min_beds=3, min_baths=2, max_price=500000)):
        print(i, meta, listing)
