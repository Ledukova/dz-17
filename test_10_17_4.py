import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import string
import os.path

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def get_otstup(txt):
    return int(txt[:2])

def test_example(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_element_by_name("login").click()
    wait = WebDriverWait(driver, 20)
    print()
    rows = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder")  # закрытые активные папки
    l_rows = len(rows)
    # print("закрытых активных папок", l_rows)
    otstup_papki = 0  # для фильтрации товаров текущего уровня
    while l_rows > 0:  # пока есть закрытые активные папки
        #rows_new = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder")  # закрытые активные папки
        images = driver.find_elements_by_css_selector(("tr.row img"))  # картинки товаров
        # print("кол-во картинок", len(images))
        elements = driver.find_elements_by_css_selector("tr.row img+[href*='edit_product']")  # ссылки товаров
        if len(elements) > 0:
            for j in range(0, len(elements)):
                otstup = get_otstup(images[j].value_of_css_property("margin-left"))
                # print("отступ товара", otstup)
                if otstup > otstup_papki:  # непросмотренный товар
                    # print("кликаем на ", elements[j].text)
                    elements[j].click()
                    for l in driver.get_log("browser"):  # проверка появятся ли лги браузера
                        print("логи браузера:", l)
                    wait.until(lambda d: d.find_elements_by_css_selector("[name='cancel']"))
                    driver.find_element_by_css_selector("[name='cancel']").click()
                    elements = wait.until(lambda d: d.find_elements_by_css_selector("tr.row img+[href*='edit_product']"))  # жду появления кнопок Edit
                    images = driver.find_elements_by_css_selector(("tr.row img"))  #  обновляем картинки товаров
        rows_open = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder-open")
        rows_open[-1].click()  # ставим галочку
        driver.find_element_by_css_selector("[name='disable']").click()  # нажимаем кнопку disable - делаем папку неактивной
        rows_open = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder-open")
        ssilki = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder+a")
        if len(ssilki) > 0:
            # print("*кликаем на 1ую папку", ssilki[0].text)
            ssilki[0].click()
            rows_open = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder-open")
            if len(rows_open) > 1:
                otstup_papki = get_otstup(rows_open[-1].value_of_css_property("margin-left"))
                # print("отступ папки", otstup_papki)
        rows = driver.find_elements_by_css_selector("tr.row:not(.semi-transparent) .fa-folder")
        l_rows = len(rows)
        # print("закрытых активных папок", l_rows)
    driver.find_element_by_css_selector("tr.row:not(.semi-transparent) .fa-folder-open").click
    rows = driver.find_elements_by_css_selector("tr.row.semi-transparent .fa-folder")  # закрытые неактивные папки
    l_rows = len(rows)
    # print("закрытых активных папок", l_rows)
    while l_rows > 0:  # пока есть закрытые неактивные папки
        ssilki = driver.find_elements_by_css_selector("tr.row.semi-transparent .fa-folder+a")
        if len(ssilki) > 0:
            # print("*кликаем на 1ую папку", ssilki[0].text)
            ssilki[0].click()
            rows_open = driver.find_elements_by_css_selector("tr.row.semi-transparent .fa-folder-open")
            while len(rows_open) > 0:
                rows_open[-1].click()  # ставим галочку
                driver.find_element_by_css_selector("[name='enable']").click()  # нажимаем кнопку ensable - делаем папку активной
                rows_open = driver.find_elements_by_css_selector("tr.row.semi-transparent .fa-folder-open")
        rows = driver.find_elements_by_css_selector("tr.row.semi-transparent .fa-folder")
        l_rows = len(rows)
        # print("закрытых активных папок", l_rows)





