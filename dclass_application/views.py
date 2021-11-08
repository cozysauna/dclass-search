from typing import Sequence
from django.http.response import Http404
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .forms import ClassSeachForm, CommentForm, SortForm 
from .models import Classes, Comment
from accounts.models import CustomUser
from django.http.response import HttpResponseRedirect


class IndexView(TemplateView):
    class_model = Classes
    comment_model = Comment
    RECOMMEND_CNT = 5
    RECENT_COMMENT = 5
    def get(self, request):
        params = {
            'form': ClassSeachForm,
            'recommend_data': self.class_model.objects.all().order_by('a_ratio').reverse()[:self.RECOMMEND_CNT],
            'recent_comments': self.comment_model.objects.all().order_by('created_at')[:self.RECOMMEND_CNT],
        }
        return render(request, 'index.html', params)

class ResultView(ListView):
    model = Classes
    def post(self, request):
        if 'day' in request.POST:
            search_params = {key: request.POST[key] for key in request.POST.keys() if key in self.get_field_names() and request.POST[key] != '0'}
            request.session['search_params'] = search_params
        else:
            search_params = request.session['search_params']
            search_params['sort'] = request.POST['sort']

        querys = self.get_queryset(search_params)
        params = self.get_params(querys, search_params)
        request.session['seach_params'] = search_params
        return render(request, 'result.html', params)

    def get_queryset(self, search_params):
        if 'sort' in search_params:
            if search_params['sort'] == '1':
                query = self.model.objects.all().order_by('favorite').reverse()
            elif search_params['sort'] == '2': 
                query = self.model.objects.all().order_by('a_ratio').reverse()
            elif search_params['sort'] == '3':
                query = self.model.objects.all().order_by('average_evaluation').reverse()
            else:
                query = self.model.objects.all()
        else:
            query = self.model.objects.all()

        if 'day' in search_params:
            query = query.filter(day=search_params['day'])
        if 'term' in search_params:
            query = query.filter(term=search_params['term'])
        return query

    def get_params(self, querys, search_params):        
        params = {
            'querys': querys,
            'query_cnt': querys.count(),
            'sort_form': SortForm
        }
        for cond in self.get_conditions():
            if cond in search_params:
                params[cond] = search_params[cond]
            else:
                params[cond] = '指定なし'
        return params

    def get_field_names(self):
        return [field.name for field in self.model._meta.get_fields()]

    def get_conditions(self):
        conds = ['day', 'term', 'class_form', 'place']
        return conds

def ClassView(request, pk):
    RELATED_CLASS_CNT = 5
    cl = Classes.objects.get(pk=pk)
    related_classs = Classes.objects.filter(place=cl.place)
    comments = Comment.objects.filter(cl=cl)
    params = {
        'cl': cl,
        'related_classes': related_classs[:RELATED_CLASS_CNT],
        'comments': comments,
    }
    if request.user.is_authenticated:
        params['checked_favorite'] = request.user.favorite_class.filter(pk=pk).exists()
    return render(request, 'class.html', params)

def FavoriteView(request, uspk, clpk):
    cl = Classes.objects.get(pk=clpk)
    user = CustomUser.objects.get(pk=uspk)
    user.favorite_class.add(cl)
    user.save()
    params = {
        'cl': cl,
    }
    params['checked_favorite'] = True
    return render(request, 'class.html', params)


def RemoveFavoriteView(request, uspk, clpk):
    cl = Classes.objects.get(pk=clpk)
    user = CustomUser.objects.get(pk=uspk)
    user.favorite_class.remove(cl)
    user.save()
    params = {
        'cl': cl,
    }
    params['checked_favorite'] = False
    return render(request, 'class.html', params)


def AddCommentView(request, uspk, clpk):
    if request.method == 'GET':
        params = {
            'cl': Classes.objects.get(pk=clpk),
            'form': CommentForm,
        }
        return render(request, 'add_comment.html', params)
    else:
        text = request.POST['text']
        star = request.POST['star']
        
        cl = Classes.objects.get(pk=clpk)
        user = CustomUser.objects.get(pk=uspk)

        comment = Comment(text=text, star=star, cl = cl, user=user)
        comment.save()


        RELATED_CLASS_CNT = 5
        related_classs = Classes.objects.filter(place=cl.place)
        params = {
            'cl': cl,
            'related_classes': related_classs[:RELATED_CLASS_CNT],
        }
        if request.user.is_authenticated:
            params['checked_favorite'] = request.user.favorite_class.filter(pk=clpk).exists()
        return render(request, 'class.html', params)

