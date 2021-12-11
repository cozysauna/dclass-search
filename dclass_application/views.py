from typing import Sequence
from django.http.response import Http404, HttpResponse
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .forms import ClassSeachForm, CommentForm, SortForm 
from .models import Classes, Comment
from accounts.models import CustomUser
from django.http.response import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator


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
    paginate_by = 9
    def post(self, request):
        if 'keyword' in request.POST: # To Do
            search_params = {key: request.POST[key] for key in request.POST.keys() if request.POST[key] != '0'}
            if not request.POST['keyword']: 
                del search_params['keyword']
            request.session['search_params'] = search_params
        else:
            search_params = request.session['search_params']
            search_params['sort'] = request.POST['sort']


        querys = self.get_queryset(search_params)
        querys = Paginator(querys, self.paginate_by)

        params = self.get_params(querys, search_params)
        request.session['seach_params'] = search_params
        return render(request, 'result.html', params)

    def get(self, request):
        search_params = request.session['search_params']

        querys = self.get_queryset(search_params)
        querys = Paginator(querys, self.paginate_by)

        page_num = request.GET.get('page', 1)

        params = self.get_params(querys, search_params, page_num)
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
                query = self.model.objects.all().order_by('a_ratio').reverse()
        else:
            query = self.model.objects.all().order_by('a_ratio').reverse()

        if 'day' in search_params:
            query = query.filter(day=search_params['day'])
        if 'term' in search_params:
            query = query.filter(term=search_params['term'])
        if 'place' in search_params:
            query = query.filter(place=search_params['place'])
        if 'faculty' in search_params:
            query = query.filter(faculty=search_params['faculty'])
        if 'class_form' in search_params:
            query = query.filter(class_form=search_params['class_form'])
        if 'keyword' in search_params:
            query = query.filter(
                Q(class_name__contains=search_params['keyword']) | Q(teacher__contains=search_params['keyword'])
            ).distinct()
        return query

    def get_params(self, querys, search_params, page_num = 1):        
        params = {
            'querys': querys.get_page(page_num),
            'query_cnt': querys.count,
            'sort_form': SortForm,
            'search_conditions': [],
        }
        for cond in self.get_field_names():
            if cond in search_params:
                params['search_conditions'].append(search_params[cond])

        return params

    def get_field_names(self):
        field_names = [
            'term',
            'day',
            'place',
            'faculty',
            'class_form',
            'keyword'
        ]
        return field_names


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
        'form': ClassSeachForm,
    }
    if request.user.is_authenticated:
        params['checked_favorite'] = request.user.favorite_class.filter(pk=pk).exists()
    return render(request, 'class.html', params)


def AjaxFavoriteView(request):
    if request.method == 'GET':
        uspk = request.user.id
        clpk = request.GET['clpk']
        cl = Classes.objects.get(pk=clpk)
        user = CustomUser.objects.get(pk=uspk)
        if request.user.favorite_class.filter(pk=clpk).exists():
            user.favorite_class.remove(cl)
        else:
            user.favorite_class.add(cl)
        user.save()
        return HttpResponse('Completed')
    return HttpResponse('NotCompleted')


def AddCommentView(request, clpk):
    uspk = request.user.id
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


def RemoveCommentView(request, cmpk):
    if request.method == 'GET':
        com = Comment.objects.get(pk=cmpk)
        com.cl.comment_num -= 1
        com.cl.save()
        com.delete()

    return redirect('profile')


def AjaxGoodView(request):
    if request.method == "GET":
        clpk = request.GET['clpk']
        check_bool = request.GET['check_bool']
        cl = Classes.objects.get(pk=clpk)
        if check_bool == 'true':
            cl.favorite -= 1
        else:
            cl.favorite += 1
        cl.save()
        return HttpResponse('Completed')

    return HttpResponse('NotCompleted')

