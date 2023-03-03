from requests import get, put, delete, post

print('Пользователь ниже не должен найтись, тк его ид отсутствует')
print(delete("http://127.0.0.1:5000/api/v2/users/34534634534").json())
print('теперь удаляем пользователя с ид 3(если он есть)')
print(delete("http://127.0.0.1:5000/api/v2/users/3").json())
print('Проверяем, что его больше нет')
print(get("http://127.0.0.1:5000/api/v2/users/3").json())
print('Теперь добавляес пользователя с ид 3')
print(post('http://127.0.0.1:5000/api/v2/users/3', json={
    "surname": "tester", "name": "test", "age": 18, "position": "test", "speciality": "test", "address": "module_11",
    "city_from": 'Москва', "email": "test1111@yandex.ru"
}).json())
print('Отправим неправильный запрос')
print(put('http://127.0.0.1:5000/api/v2/users/12', json={
    "surname": 0
}).json())
print('Отправим корректный запрос')
print(put('http://127.0.0.1:5000/api/v2/users/4', json={
    "surname": "tester", "name": "test", "age": 18, "position": "test", "speciality": "test", "address": "module_11",
    "city_from": 'Москва', "email": "test23@yandex.ru"
}).json())
