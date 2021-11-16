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
    RECOMMEND_CNT = 6
    RECENT_COMMENT = 6
    def get(self, request):
        params = {
            'form': ClassSeachForm,
            'recommend_data': self.class_model.objects.all().order_by('a_ratio').reverse()[:self.RECOMMEND_CNT],
            'recent_comments': self.comment_model.objects.all().order_by('created_at').reverse()[:self.RECOMMEND_CNT],
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

    def get(self, request):
        search_params = request.session['search_params']
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
        
        if search_params['keyword']:
            query = query.filter(class_name__contains=search_params['keyword'])
        return query

    def get_params(self, querys, search_params):        
        params = {
            'querys': querys,
            'query_cnt': querys.count(),
            'sort_form': SortForm,
            'search_conditions': [],
        }
        for cond in self.get_conditions():
            if cond in search_params:
                params['search_conditions'].append(search_params[cond])
                # params[cond] = search_params[cond]
            # else:
            #     params[cond] = '指定なし'

        return params

    def get_field_names(self):
        field_names = [
            'day',
            'term',
            'sort',
            'keyword'
        ]
        # return [field.name for field in self.model._meta.get_fields()]
        return field_names

    def get_conditions(self):
        conds = ['day', 'term', 'class_form', 'place']
        return conds

def ClassView(request, pk):
    RELATED_CLASS_CNT = 6
    COMMENT_CNT = 6
    cl = Classes.objects.get(pk=pk)
    related_classs = Classes.objects.filter(place=cl.place)
    comments = Comment.objects.filter(cl=cl)
    params = {
        'cl': cl,
        'related_classes': related_classs[:RELATED_CLASS_CNT],
        'comments': comments[:COMMENT_CNT],
    }
    if request.user.is_authenticated:
        params['checked_favorite'] = request.user.favorite_class.filter(pk=pk).exists()
    return render(request, 'class.html', params)

def FavoriteView(request, uspk, clpk):
    cl = Classes.objects.get(pk=clpk)
    user = CustomUser.objects.get(pk=uspk)
    user.favorite_class.add(cl)
    user.save()

    return redirect('class', clpk)


def RemoveFavoriteView(request, uspk, clpk):
    cl = Classes.objects.get(pk=clpk)
    user = CustomUser.objects.get(pk=uspk)
    user.favorite_class.remove(cl)
    user.save()

    return redirect('class', clpk)


def AddCommentView(request, uspk, clpk):
    if request.method == 'GET':
        params = {
            'cl': Classes.objects.get(pk=clpk),
            'form': CommentForm,
        }
        return render(request, 'add_comment.html', params)
    else:
        text = request.POST['text']
        # cssでstarのindex番号を逆順にしているため
        star = str(6 - int(request.POST['star']))
        cl = Classes.objects.get(pk=clpk)
        user = CustomUser.objects.get(pk=uspk)

        comment = Comment(text=text, star=star, cl = cl, user=user)
        comment.save()

        cl = Classes.objects.get(pk=clpk)
        cl.comment_num += 1
        cl.save()

        return redirect('class', clpk)


def RemoveCommentDoubleCheckView(request, clpk, cmpk):
    if request.method == 'GET':
        com = Comment.objects.get(pk=cmpk)
        initial_dict = {"star":str(6-int(com.star)), "text":com.text}
        params = {
            'cl': Classes.objects.get(id=clpk),
            'comment': com,
            'form': CommentForm(initial=initial_dict)
        }
        return render(request, 'remove_comment_double_check.html', params)


def RemoveCommentView(request, cmpk):
    if request.method == 'GET':
        com = Comment.objects.get(pk=cmpk)
        com.cl.comment_num -= 1
        com.cl.save()
        com.delete()

    return redirect('profile')


def GoodView(request, clpk):
    cl = Classes.objects.get(pk=clpk)
    cl.favorite += 1
    cl.save()

    return redirect('class', clpk)

