from django import forms

from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.models import User


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

    keyword = forms.CharField(label='keyword',
                                required=False,
                                widget=forms.TextInput({'class': 'keyword', 'placeholder': '授業名や教師で検索'}))


class SortForm(forms.Form):
    sort = forms.ChoiceField(
        label='',
        choices=(
            ('0', '指定なし'),
            ('1', 'いいねが多い順番'),
            ('2', 'A率が高い順'),
            ('3', '評定平均が高い順')
        ),
        initial = '0',
    )

class CommentForm(forms.Form):
    text = forms.CharField(label='授業コメント', widget=forms.Textarea({'class': 'comment', 'placeholder': 'コメント'}))
    star = forms.ChoiceField(label='星',
                        choices=(
                            ('1', '1'),
                            ('2', '2'),
                            ('3', '3'),
                            ('4', '4'),
                            ('5', '5'),
                        ),
                        initial='3',
                        widget=forms.RadioSelect(
                            attrs={'class': 'radio'}
                        )
                        )