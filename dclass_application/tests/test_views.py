from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.test import LiveServerTestCase
from ..views import IndexView
import traceback
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.webdriver import WebDriver

class LoginTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # options = webdriver.ChromeOptions()
        # driver = webdriver.Chrome(options=options)
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://localhost:8000/accounts/login/')

        #ログイン情報入力
        username_input = self.selenium.find_element(by=By.NAME, value= "login")
        username_input.send_keys('username')
        password_input = self.selenium.find_element(by=By.NAME, value="password")
        password_input.send_keys('password')
        self.selenium.find_element_by_class_name('btn').click()
        self.assertEqual('同志社大学授業検索サーチ', self.selenium.title)