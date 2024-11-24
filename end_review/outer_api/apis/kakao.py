import requests

from outer_api.scrapings.common import run_scraping


def return_place_with_keyword(query):
    only_url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {
        'Authorization': 'KakaoAK 17883e54d7b46254cacfe3908ed18a2e',
    }
    params = {
        'query': query
    }
    result = requests.get(only_url, headers=headers, params=params)
    return result


def return_score_with_place_id(place_ids):
    dict_result = run_scraping(place_ids)
    return dict_result
