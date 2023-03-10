from requests import post

print(post('http://localhost:5000/api/users/4',
           json={
               'name': 'test',
               'surname': 'testov',
               'age': 12,
               'speciality': 'tester',
               'position': 'tester',
               'address': 'test',
               'email': 'testtest2@mail.ru',
               'city_from': 'testovsk'}).json())  # проверяем с помощью адекватного запроса
