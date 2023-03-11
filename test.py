from requests import get, delete, post

# print(get("http://127.0.0.1:5000/api/v2/jobs/34534634534").json())
# print(get("http://127.0.0.1:5000/api/v2/jobs/7").json())
# print(get("http://127.0.0.1:5000/api/v2/jobs").json())
# print('------------------------------------------------------------------')
# print(delete("http://127.0.0.1:5000/api/v2/jobs/8").json())
# print(delete("http://127.0.0.1:5000/api/v2/jobs/123125125").json())
# print(delete("http://127.0.0.1:5000/api/v2/jobs").json())
# print('------------------------------------------------------------------')
print(post('http://127.0.0.1:5000/api/v2/jobs', json={
    "job": "test", "team_leader": 14, "is_finished": 0,
    "collaborators": '1, 2, 3', "work_size": 4}).json())
# print(post('http://127.0.0.1:5000/api/v2/jobs/7', json={
#     "job": "test", "team_leader": 1, "is_finished": 0,
#     "collaborators": '4, 1, 2', "work_size": 4}).json())

