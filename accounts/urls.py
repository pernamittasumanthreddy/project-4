from django.urls import path
from accounts.views import LoginView, LogoutView, CurrentUserView, switch_user_session

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', CurrentUserView.as_view(), name='auth_me'),
    path('switch/<str:username>/', switch_user_session, name='auth_switch_user'),
]

