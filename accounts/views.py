from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CustomUser
from allauth.account import views
from .forms import SignupUserForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin ,TemplateView):
    model = CustomUser
    def get(self, request, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        params = {
            'user': user,
        }

        return render(request, 'accounts/profile.html', params)

class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')

class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm
