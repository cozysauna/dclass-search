from django.db import models
from django.db.models.base import Model
from django.utils import timezone
# from accounts.models import CustomUser

class Classes(models.Model):
    """
    授業名: class_name
    A率: a_ratio
        B率: b_ratio
        C率: c_ratio
        D率: d_ratio
        F率: f_ratio
        O率: o_ratio
    評定平均:  average_evaluation
    学期（春 or 秋）: term
    年度: year
    場所（今出川 or 京田辺）: place
    授業形態（対面 or オンライン）: class_form
    曜日 : day
    時間帯 : time
    いいね数 : favorite
    教科書 : textbook
    授業コード : code
    学部: faculty
    教師: teacher
    生徒数: num_student
    シラバスリンク:　syllabus_link
    テスト率: test_ratio
    レポート率: report_ratio
    出席率: paticipation_ratio
    """
    class_name = models.CharField(max_length=100)
    a_ratio = models.FloatField(default=0.0)
    b_ratio = models.FloatField(default=0.0)
    c_ratio = models.FloatField(default=0.0)
    d_ratio = models.FloatField(default=0.0)
    f_ratio = models.FloatField(default=0.0)
    o_ratio = models.FloatField(default=0.0)
    average_evaluation = models.FloatField(default=0.0)
    term = models.CharField(max_length=100)
    year = models.IntegerField(default=2021)
    place = models.CharField(max_length=100)
    class_form = models.CharField(max_length=100) 
    day = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    favorite = models.IntegerField(default=0)
    textbook = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100) 
    teacher = models.CharField(max_length=100)
    syllabus_link = models.CharField(max_length=100)
    test_ratio = models.IntegerField(default=0)
    report_ratio = models.IntegerField(default=0)
    participation_ratio = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    num_student = models.IntegerField(default=0)

    def get_round_a_ratio(self):
        return int(self.a_ratio)

    def __str__(self):
        return self.class_name +':'+ str(self.year)+':'+str(self.code)

class Comment(models.Model):
    text = models.TextField()
    cl = models.ForeignKey(Classes, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.DO_NOTHING)
    star = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def get_star(self):
        return '★' * self.star

    def get_left_star(self):
        return '★' * (5 - self.star)

    def __str__(self):
        return str(self.user.id) +':'+ str(self.cl.id) +':'+ self.text