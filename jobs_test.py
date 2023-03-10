from requests import post, get, put

print(post('http://localhost:5000/api/jobs/12',
           json={
               'team_leader': 11,
               'job': 'не работа',
               'start_date': '2005-04-01', 'end_date': '2007-04-01',
               'collaborators': '0', 'work_size': 222,
               'is_finished': 1}).json())  # проверяем с помощью адекватного запроса

