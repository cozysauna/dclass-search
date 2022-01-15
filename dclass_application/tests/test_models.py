from django.test import TestCase
from dclass_application.models import Classes

class ClassesModelTests(TestCase):    

    def test_is_empty(self):
        saved_classes = Classes.objects.all()
        self.assertEqual(saved_classes.count(), 0)

    def test_is_count_one(self):
        class_count = Classes.objects.all().count()
        cls = Classes(
            class_name='test_class_name',
            term = 'test_term',
            place = 'test_place',
            class_form = 'test_class_form',
            day = 'test_day',
            time = 'test_time',
            textbook = 'test_textbook',
            code = 'test_code',
            faculty = 'test_faculty',
            teacher = 'test_teacher',
            syllabus_link = 'test_syllabus_link',
        )
        cls.save()
        new_class_count = Classes.objects.all().count()
        self.assertEqual(class_count+1, new_class_count)

    def test_save_retrieve(self):
        cls = Classes()
        class_name='test_class_name'
        term = 'test_term'
        place = 'test_place'
        class_form = 'test_class_form'
        day = 'test_day'
        time = 'test_time'
        textbook = 'test_textbook'
        code = 'test_code'
        faculty = 'test_faculty'
        teacher = 'test_teacher'
        syllabus_link = 'test_syllabus_link'
        cls.class_name = class_name
        cls.term = term 
        cls.place = place 
        cls.class_form = class_form
        cls.day = day 
        cls.time = time 
        cls.textbook = textbook
        cls.code = code 
        cls.faculty = faculty
        cls.teacher = teacher
        cls.syllabus_link = syllabus_link
        cls.save()
        saved_post = Classes.objects.first()
        self.assertEqual(saved_post.class_name, class_name)
        self.assertEqual(saved_post.term, term)
        self.assertEqual(saved_post.place, place)
        self.assertEqual(saved_post.class_form, class_form)
        self.assertEqual(saved_post.day, day)
        self.assertEqual(saved_post.time, time)
        self.assertEqual(saved_post.textbook, textbook)
        self.assertEqual(saved_post.code, code)
        self.assertEqual(saved_post.faculty, faculty)
        self.assertEqual(saved_post.teacher, teacher)
        self.assertEqual(saved_post.syllabus_link, syllabus_link)
