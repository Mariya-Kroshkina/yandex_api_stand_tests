import data
import sender_stand_request_post
import sender_stand_request_get


def get_user_body(first_name):
    current_body = data.user_body.copy()  # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body["firstName"] = first_name
    return current_body  # возвращается новый словарь с нужным значением firstName


#  позитивные проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request_post.post_new_user(user_body)  # переменная для сохранения результатов запроса
    assert user_response.status_code == 201  # проверка статус.кода
    assert user_response.json()["authToken"] != ""  # проверка токена
    users_table_response = sender_stand_request_get.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1  # Проверка, что такой пользователь есть, и он единственный


#  Негативные проверки (есть символ)
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request_post.post_new_user(user_body)  # переменная для сохранения результатов запроса
    assert user_response.status_code == 400  # проверка статус.кода
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                              "Имя может содержать только русские или латинские буквы, " \
                                              "длина должна быть не менее 2 и не более 15 символов"
# Негативные проверки 2 (нет символа)
def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request_post.post_new_user(user_body)  # переменная для сохранения результатов запроса
    assert user_response.status_code == 400  # проверка статус.кода
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"


#  Тест 1
def test_create_user_2_letter_in_first_name():
    positive_assert("Аа")

#  Тест 2
def test_create_user_15_letter_in_first_name():
    positive_assert("Ааааааааааааааа")

#  Тест 3
def test_create_user_english_letter_in_first_name():
    positive_assert("QWErty")

#  Тест 4
def test_create_user_russian_letter_in_first_name():
    positive_assert("Мария")

#  Тест 5
def test_create_user_1_letter_in_first_name():
    negative_assert_symbol("А")

# Тест 6
def test_create_user_16_letter_in_first_name():
    negative_assert_symbol("Аааааааааааааааа")

#  Тест 7
def test_create_user_space_letter_in_first_name():    #FAILED
    negative_assert_symbol("Человек и Ко")

#  Тест 8
def test_create_user_special_symbol_letter_in_first_name():
    negative_assert_symbol("№%@")

#  Тест 9
def test_create_user_number_letter_in_first_name():
    negative_assert_symbol("123")

#  Тест 10
def test_create_user_no_first_name():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

#  Тест 11
def test_create_user_empty_first_name():
    user_body = data.user_body.copy()
    user_body["firstName"] = "" #  Или # В переменную user_body сохраняется обновлённое тело запроса user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

#  Тест 12
def test_create_user_number_type_first_name():
    user_body = get_user_body(12)
    response = sender_stand_request_post.post_new_user(user_body)
    assert response.status_code == 400

