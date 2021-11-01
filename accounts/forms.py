from django import forms 
from allauth.account.forms import SignupForm


class SignupUserForm(SignupForm):
    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=30)
    def save(self, request):
        user =  super(SignupUserForm, self).save(request)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

