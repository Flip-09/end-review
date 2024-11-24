from django.urls import path, include


urlpatterns = [
    path('', include('search.urls')),

    path('__debug__/', include('debug_toolbar.urls')),
]
