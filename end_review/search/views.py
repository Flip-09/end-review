from django.shortcuts import render

from outer_api.apis.kakao import return_place_with_keyword, return_score_with_place_id


def search_view(request):
    query = request.GET.get('query')

    result = []

    if query:
        result = return_place_with_keyword(query).json().get('documents', [])

    result = result[:5]
    ids = [place.get('id') for place in result]
    id_score_dict = return_score_with_place_id(ids)
    rating_excludes = []
    for index, dict_obj in enumerate(result):
        dict_id = dict_obj.get('id')
        dict_obj['rating'] = id_score_dict.get(dict_id)
        if dict_obj['rating'] == '후기미제공':
            rating_excludes.append(index)

    rating_exclude_result = []
    while rating_excludes:
        pop_index = rating_excludes.pop(-1)
        rating_exclude_result.append(result.pop(pop_index))

    result = sorted(result, key=lambda x: x.get('rating', -1), reverse=True)
    result += rating_exclude_result

    return render(request, 'search.html', {
        'query': query,
        'result': result,
    })
