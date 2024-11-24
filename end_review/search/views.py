from django.shortcuts import render

from outer_api.apis.kakao import return_place_with_keyword


def search_view(request):
    query = request.GET.get('query')

    result = []

    if query:
        result = return_place_with_keyword(query).json().get('documents', [])

    return render(request, 'search.html', {
        'query': query,
        'result': result[:5],
    })
