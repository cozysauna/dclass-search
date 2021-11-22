from django.urls import path
from .views import ProfileView, LoginView, LogoutView, SignupView, DuetView
urlpatterns = [
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('login/', LoginView.as_view(), name = 'account_login'),
    path('logout/', LogoutView.as_view(), name = 'account_logout'),
    path('signup/', SignupView.as_view(), name = 'account_signup'),
    path('duet/<int:uspk>', DuetView, name='duet')
]
