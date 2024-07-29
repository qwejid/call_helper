from django.urls import path, include
from users.views import users
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search', users.UserListSearchView, 'users-search')

urlpatterns = [
    path('users/reg/', users.RegistrationView.as_view(), name='reg'),
    path('user/me/', users.MeView.as_view(), name='me'),
    path('users/reg/change-passwd/', users.ChangePasswordView.as_view(), name='change_passwd'),
]

urlpatterns += path('users/', include(router.urls)),
