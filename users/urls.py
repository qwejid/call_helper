from django.urls import path, include
from users.views.users import RegistrationView

# router = DefaultRouter()

urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name = 'reg')
]

# urlpatterns += path('users/', include(router.urls))