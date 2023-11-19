import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()

    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Вводим email
    driver.find_element(By. ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.implicitly_wait(10)
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    driver.implicitly_wait(10)
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    driver.implicitly_wait(10)
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        assert image_source != ''  # (image_source не должен быть пустым.)
        assert names[i].text != ''  # (name_text не должен быть пустым.)
        assert descriptions[i].text != ''  # (descriptions[i] не должен быть пустым.)
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(
            parts[0]) > 0  # (первая часть текста descriptions[i], разделенная запятой) должна иметь длину больше 0.
        assert len(
            parts[1]) > 0  # (вторая часть текста descriptions[i], разделенная запятой) должна иметь длину больше 0.


# Заходим на страницу моих питомцев
def test_show_my_pets(driver):
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Нажимаем на кнопку мои питомцы
    driver.find_element(By.CSS_SELECTOR, 'a.nav-link').click()
    # Проверяем, что мы оказались на странице мои питомцы
    assert driver.find_element(By.TAG_NAME, 'h2').text == 'Vasya'

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, './/.col-sm-4 left')))

    # Находим статистику с кол-вом питомцев

    statistics_my_pets = driver.find_elements(By.CSS_SELECTOR, './/.col-sm-4 left')

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table table-hover tr')))

    # Находим кол-во созданых пользователем питомцев
    created_my_pets = driver.find_elements(By.CSS_SELECTOR, '.table.table table-hover tr')


    # Проверяем, что количество созданых пользователем питомцев равно количеству, указанному в статистике пользователя:
    number = statistics_my_pets[0].text.split('/n')
    number = number[1].split(' ')
    number = int(number[1])

    number_of_pets = len(created_my_pets)

    assert number_of_pets == number

