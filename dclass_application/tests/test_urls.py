from django.test import TestCase
from django.urls import reverse, resolve 
from ..views import IndexView, ResultView 

class TestUrls(TestCase):

    def test_index_url(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, IndexView)

    def test_result_url(self):
        view = resolve('/result')
        self.assertEqual(view.func.view_class, ResultView)