from django import forms

from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User


User = get_user_model()

class ClassSeachForm(forms.Form):
    term = forms.ChoiceField(
        label='学期',
        choices=(
            ('0', '指定なし'),
            ('春', '春'),
            ('秋', '秋'),
        ),
        initial = '0',
        widget=forms.RadioSelect(attrs={'class': 'choice'}),
    )

    day = forms.ChoiceField(label='曜日',
                            choices=(
                                ('0', '指定なし'),
                                ('月', '月'),
                                ('火', '火'),
                                ('水', '水'),
                                ('木', '木'),
                                ('金', '金'),
                                ('土', '土'),
                                ('日', '日'),
                            ),
                            initial='0',
                            widget=forms.RadioSelect(
                                attrs={'class': 'choice'}),
                            )
    period = forms.ChoiceField(label='講時',
                            choices=(
                                ('0', '指定なし'),
                                ('1', '1時限目'),
                                ('2', '2時限目'),
                                ('3', '3時限目'),
                                ('4', '4時限目'),
                                ('5', '5時限目'),
                                ('6', '6時限目'),
                                ('7', '7時限目'),
                            ),
                            initial='0',
                            widget=forms.RadioSelect(
                                attrs={'class': 'choice'})

                            )

    place = forms.ChoiceField(label='場所',
                              choices=(
                                  ('0', '指定なし'),
                                  ('今出川', '今出川'),
                                  ('京田辺', '京田辺'),
                              ),
                                initial='0',

                              widget=forms.RadioSelect(
                                  attrs={'class': 'radio'})

                              )

    class_form = forms.ChoiceField(label='授業形態',
                                choices=(
                                    ('0', '指定なし'),
                                    ('ネット配信', 'ネット配信'),
                                    ('対面', '対面'),
                                ),
                                initial='0',
                                widget=forms.RadioSelect(
                                    attrs={'class': 'radio'})
                                )
    year = forms.ChoiceField(label='年度',
                                choices=(
                                    ('0', '指定なし'),
                                    ('2021', '2021'),
                                ),
                                initial='0',
                                widget=forms.RadioSelect(
                                    attrs={'class': 'radio'})
                                ) 


class SortForm(forms.Form):
    sort = forms.ChoiceField(
        label='並び替え',
        choices=(
            ('0', '指定なし'),
            ('1', 'いいねが多い順番'),
            ('2', 'A率が高い順'),
            ('3', '評定平均が高い順')
        ),
        initial = '0',
    )

class SigninForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=255,
        min_length=3,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'your-email@example.com',
            }
        )
    )
    password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '********',
            }
        )
    )
    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        if 'email' in cleaned_data and 'password' in cleaned_data:
            try:
                user = User.objects.get(email=cleaned_data['email'])
            except:
                raise ValidationError('メールアドレスかパスワードが間違っています。')
            auth_result = authenticate(
                username=str(user),
                password=cleaned_data['password']
            )
            if not auth_result:
                raise ValidationError('メールアドレスかパスワードが間違っています。')
            cleaned_data['username'] = str(user)
            return cleaned_data
    def clean_email(self):
        return self.cleaned_data['email']
    def clean_password(self):
        return self.cleaned_data['password']
    def cleaned_username(self):
        return self.cleaned_data['username']


class SignupForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=255,
        min_length=3,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'your-email@example.com',
            }
        )
    )
    password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '********',
            }
        )
    )