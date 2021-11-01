from typing import Sequence
from django.http.response import Http404
from django.views.generic import TemplateView, ListView, FormView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .forms import ClassSeachForm, SortForm, SigninForm, SignupForm
from .models import Classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect


class IndexView(TemplateView):
    model = Classes
    def get(self, request):
        params = {
            'form': ClassSeachForm,
            'recommend_data': self.model.objects.all().order_by('a_ratio').reverse(),
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

def LikeView(request, pk):
        try:
            cl = Classes.objects.get(pk=pk)
        except:
            return Http404
        cl.favorite += 1
        cl.save()
        return redirect('index')

def ClassView(request, pk):
    cl = Classes.objects.get(pk=pk)
    return render(request, 'class.html', {'cl': cl})


 
# def SigninView(request):
#     if request.method == 'GET':
#         form = SigninForm()
#     else:
#         form = SigninForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = form.cleaned_data['username']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 pass
#     params = {
#         'form': form
#     }
#     return render(request, 'signin.html', params)

# def SignoutView(request):
#     logout(request)
#     return redirect('index')

# def SignupView(request):
#     params = {
#         'form': SignupForm()
#     }
#     return render(request, 'signup.html', params)

# def ProfileView(request, pk):
#     model = User
#     params = {
#         'user': model.objects.get(pk=pk)            
#     }
#     return render(request, 'profile.html', params)