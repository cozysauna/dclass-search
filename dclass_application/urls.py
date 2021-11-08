from django.urls import path
from .views import IndexView, ResultView, ClassView, FavoriteView, RemoveFavoriteView, AddCommentView
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('result', ResultView.as_view(), name = 'result'),
    path('class/<int:pk>', ClassView, name = 'class'),
    path('favorite/<int:uspk>/<int:clpk>', FavoriteView, name = 'favorite'),
    path('removefavorite/<int:uspk>/<int:clpk>', RemoveFavoriteView, name = 'remove_favorite'),
    path('add_comment/<int:uspk>/<int:clpk>', AddCommentView, name='add_comment'),
]
