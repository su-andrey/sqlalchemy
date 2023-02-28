from requests import get
import requests

def test():
    s = requests.session()
    s.keep_alive = False  # disable keep alive
    print('НИЖЕ ДОЛЖЕН ВЫВЕСТИ СПИСОК ВСЕХ РАБОТ')
    print(s.get('http://localhost:5000/api/jobs', timeout=12).json())
    print()
    print('НИЖЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД 0')
    print(s.get('http://localhost:5000/api/jobs/1').json())
    print()
    print('НИЖЕ НЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД 999')
    print(s.get('http://localhost:5000/api/jobs/999').json())
    print()
    print('НИЖЕ НЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД asd')
    print(s.get('http://localhost:5000/api/jobs/asd').json())
    print()

