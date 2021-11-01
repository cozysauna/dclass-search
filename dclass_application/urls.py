from django.urls import path
from .views import IndexView, ResultView, LikeView, ClassView
# from .views import IndexView, ResultView, LikeView, ClassView, SigninView, SignoutView, SignupView, ProfileView
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('result', ResultView.as_view(), name = 'result'),
    path('result/<int:pk>/like', LikeView, name = 'like'),
    path('class/<int:pk>', ClassView, name = 'class'),
    # path('signin', SigninView, name='signin'),
    # path('signout', SignoutView, name='signout'),
    # path('signup', SignupView, name='signup'),
    # path('profile/<int:pk>', ProfileView, name = 'profile')
]
