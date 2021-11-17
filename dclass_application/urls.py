from django.urls import path
from .views import IndexView, ResultView, ClassView, AddCommentView, RemoveCommentView, GoodView, AjaxFavoriteView, AjaxGoodView
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('result', ResultView.as_view(), name = 'result'),
    path('class/<int:pk>', ClassView, name = 'class'),
    path('class/ajaxfavorite/', AjaxFavoriteView, name='ajaxfavorite'),
    path('add_comment/<int:clpk>', AddCommentView, name='add_comment'),
    path('remove_comment/<int:cmpk>', RemoveCommentView, name='remove_comment'),
    path('good/<int:clpk>', GoodView, name='good'),
    path('class/ajaxgood', AjaxGoodView, name='ajaxgood'),
]
