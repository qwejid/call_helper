from django.urls import path, include
from users.views import users

# router = DefaultRouter()

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name = 'reg'),
    path('user/me/', users.MeView.as_view(), name = 'me'),
    path('users/reg/change-passwd/', users.ChangePasswordView.as_view(), name = 'change_passwd'),
]

# urlpatterns += path('users/', include(router.urls))