from requests import get, put, delete, post

print('Работа ниже не должнай найтись, тк нет ее ид')
print(get("http://127.0.0.1:5000/api/v2/jobs/34534634534").json())
print('теперь удаляем работу с ид 3(если она есть)')
print(delete("http://127.0.0.1:5000/api/v2/jobs/5").json())
print('Проверяем, что её больше нет')
print(get("http://127.0.0.1:5000/api/v2/jobs/3").json())
print('Теперь добавляем работу')
print(post('http://127.0.0.1:5000/api/v2/jobs/3', json={
    "job": "test", "team_leader": 1, "is_finished": 0,
    "collaborators": '4, 6, 7', "work_size": 4}).json())
print('Отправим неправильный запрос')
print(put('http://127.0.0.1:5000/api/v2/jobs/12', json={
    "team_leader": 0
}).json())
print('Отправим корректный запрос')
print(put('http://127.0.0.1:5000/api/v2/jobs/5', json={
    "job": "test_put", "team_leader": 7, "is_finished": 1,
    "collaborators": '4, 6, 5', "work_size": 11}).json())

