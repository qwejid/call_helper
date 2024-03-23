from django.urls import include, path
from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls

api_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += doc_urls
urlpatterns += user_urls
