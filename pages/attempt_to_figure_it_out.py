"""test_main page"""
from .pages.main_page import MainPage #test_main page подтягивает из папки pages класс для работы со страницей main_page
import pytest #импортирует pytest

#берём один тест кейс на проверку, browser объявлен через фикстуру в conftest
def test_guest_can_go_to_login_page(browser):
    link = "http://selenium1py.pythonanywhere.com/" #ссылка для перехода
    page = MainPage(browser, link) #здесь у нас переменная к которой мы привязали класс с двумя параметрами экземпляр драйвера и передали url адреса
    page.open()  #А вот здесь уже начинается запрос к base_page, к той переменной к который мы привязали класс мы ещё применяем метод которым открываем страницу
    page.go_to_login_page()  # ещё один запрос к методам base_page выполняем метод страницы — переходим на страницу логина
    login_page = LoginPage(browser, browser.current_url) #ссылка на другую страницу (login_page.py)
    login_page.should_be_login_page()


"""base_page"""

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators
import math

class BasePage():
    def __init__(self, browser, url, timeout=10): #всё что обращается к base page должно иметь браузер и урл
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self): #вызвали из test main page
        self.browser.get(self.url) #метод открывает нужную страницу, используя метод get()

    def go_to_login_page(self): #вызвали из test main page
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK) #типа ссылка на файл локаторс, где лежит селектор LOGIN_LINK
        link.click()
        assert "login" in self.browser.current_url, "Link is invalid" #проверка что ссылка на логин содержит в себе слово логин


"""locators"""
from selenium.webdriver.common.by import By

class MainPageLocators(): #здесь все селекторы для main page
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    BASKET_BUTTON = (By.CSS_SELECTOR, ".btn-group .btn.btn-default")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")


"""main_page"""
from .base_page import BasePage
from selenium.webdriver.common.by import By
from .locators import MainPageLocators

class MainPage(BasePage): #этот класс подклаас base Page
    def go_to_login_page(self): #здесь только проверка что по логин линк можно перейти
        assert self.is_element_present(*MainPageLocators.LOGIN_LINK), "Login link is not presented" #символ *, он указывает на то, что мы передали именно пару, и этот кортеж нужно распаковать
        MainPageLocators.LOGIN_LINK.click()

    def should_be_login_link(self):
        assert self.is_element_present(By.CSS_SELECTOR, "#login_link_invalid"), "Login link is not presented"

    def go_to_login_page(self): #чет я перемудрил с наименованием функций
        link = self.browser.find_element(*MainPageLocators.LOGIN_LINK)
        link.click()


# в locators лежат селекторы, их использует BasePage и main_page
# в BasePage методы по работе со страницей (открыть, перейти, проверить)
# в main_page мы подтягиваем методы из BasePage и правильные селекторы из locators, здесь полноценный тест кейс для проверки страницы.
# Ещё раз MainPage - наследник класса BasePage, чтобы можно было пользоваться методами, описанными в base_page.py
# test_main page подтягиваем страницы, например main_page
# Дальше создаём функции, которым:
# выдаём нужный для проверки линк, создаём в функции переменную page, которой передаём браузер из base_page.py(класс BasePage) и линк из шага №1
# следом говорим "page, откройся", но методом из base_page.py(класс BasePage) добавляем проверки, которые создавали методами в main_page.py
#