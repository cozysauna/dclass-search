from accounts.models import CustomUser
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CustomUser
from dclass_application.models import Comment
from allauth.account import views
from .forms import SignupUserForm, DuetForm
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
from bs4 import BeautifulSoup
from time import sleep

class ProfileView(LoginRequiredMixin ,TemplateView):
    user_model = CustomUser
    comment_model = Comment
    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        mycomment = self.comment_model.objects.filter(user=user)
        params = {
            'user': user,
            'mycomments': mycomment,
            'form': DuetForm,
            'class_table': self.get_class_table(user.duet_classes)
        }
        return render(request, 'accounts/profile.html', params)

    def get_class_table(self, data):
        # data must_be 7 times 6
        class_table = [['None'] * 6 for _ in range(7)]
        if not data: return class_table
        data = data.split('@')
        # To do 
        for i in range(6 * 7):
            class_table[i//6][i%6] = data[i]
        return class_table


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm


def DuetView(request, uspk):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=uspk)
        USER_ID = request.POST['user_id']
        PASSWORD = request.POST['password']

        try:
            #DUET URL
            URL = "https://duet.doshisha.ac.jp/gakusei/html/fb/fb010/FB01001G.html"
            session = requests.session()
            session.get(URL)

            login_info = {
                "member:loginId": USER_ID,
                "member:password": PASSWORD,
                "member/html/fb/fb010/FB01001G.html": "member",
                "member:__link_clicked__": "member:doLogin"
            }

            res = session.post(URL, data=login_info)
            res.raise_for_status()

            sleep(0.5)
            # 登録科目一覧へ
            subject_url = "https://duet.doshisha.ac.jp/gakusei/html/fb/fb020/FB02001G.html"
            subject_info = {
                "menuform/html/fb/fb020/FB02001G.html": "menuform",
                "menuform:__link_clicked__": "menuform:goFb17001g"
            }

            subject_text = session.post(subject_url, subject_info)

            # 時間割表へ
            subject_bs = BeautifulSoup(subject_text.text, 'html.parser')
            token = subject_bs.find(attrs={'name':'form1:token'}).get('value')

            time_table_url = "https://duet.doshisha.ac.jp/gakusei/html/fb/fb170/FB17001G.html"
            time_table_info = {
                "form1:token": token,
                "form1:selectedIndex": "",
                "form1:topPosition": "0",
                "form1/html/fb/fb170/FB17001G.html": "form1",
                "form1:__link_clicked__": "form1:goZikanwarihyo"
            }
            class_text = session.post(time_table_url, time_table_info)
            class_data = BeautifulSoup(class_text.content, 'html.parser')
            spring = class_data.find(id="form1:kikan1").select_one("table").select("tr")
            winter = class_data.find(id="form1:kikan2").select_one("table").select("tr")
            spring = get_registration_data(spring)
            winter = get_registration_data(winter)
            user.duet_classes = spring 
            user.save()
        except:
            user = CustomUser.objects.get(id=request.user.id)
            mycomment = Comment.objects.filter(user=user)
            params = {
                'user': user,
                'mycomments': mycomment,
                'form': DuetForm,
                'class_table': [[''] * 6 for _ in range(7)],
                'failed': 'LOGIN_ID、またはPASSWORDが違います'
            }
            return render(request, 'accounts/profile.html', params)

        return redirect('profile')

def get_registration_data(season):
    registration_data = [[None] * 6 for _ in range(7) ]
    for class_time in range(1, 8):
        data_by_class_time = season[class_time]
        data_by_day = data_by_class_time.select("td")
        # 1:月-6:土
        for day in range(1, 7):
            class_data = data_by_day[day].text.replace(' ', '').split('\n')
            class_data = [e.replace('\u3000', ' ') for e in class_data if e]
            if len(class_data) == 0: continue 
            registration_data[class_time-1][day-1] = class_data
    ret = []
    for classes in registration_data:
        for one_class in classes:
            if one_class == None:
                ret.append(' ')
            else:
                ret.append(' '.join(map(str, one_class)))
        
    ret = '@'.join(ret)
    return ret 