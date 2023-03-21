from requests import post, get, put, delete

print(post('http://127.0.0.1:5000/api/v2/jobs', json={
    "job": "test", "team_leader": 1, "is_finished": 0,
    "collaborators": '4, 1, 2', "work_size": 4}).json())