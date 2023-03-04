from requests import get, put, delete, post

print('Работа ниже не должнай найтись, тк нет ее ид')
print(get("http://127.0.0.1:5000/api/v2/jobs/34534634534").json())
print('теперь удаляем работу с ид 3(если она есть)')
print(delete("http://127.0.0.1:5000/api/v2/jobs/5").json())
print('Теперь добавляем работу')
print(post('http://127.0.0.1:5000/api/v2/jobs', json={
    "job": "test", "team_leader": 'asd', "is_finished": 0,
    "collaborators": '1, 2, 3', "work_size": 4}).json())
print('Смотри какую-то работу')
print(get("http://127.0.0.1:5000/api/v2/jobs/6").json())
print('После редактируем ее')
print(post('http://127.0.0.1:5000/api/v2/jobs/6', json={
    "job": "test", "team_leader": 1, "is_finished": 0,
    "collaborators": '4, 1, 2', "work_size": 4}).json())
print('Снова смотрим')
print(get("http://127.0.0.1:5000/api/v2/jobs/6").json())
print('Отправим некорректный запрос')
print(post('http://127.0.0.1:5000/api/v2/jobs/4', json={
    "job": "test", "team_leader": 2, "is_finished": 0,
    "collaborators": '4, 1, 2', "work_size": 4}).json())
print('Отправим корректный запрос')

