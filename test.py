from requests import get

def test():
    print('НИЖЕ ДОЛЖЕН ВЫВЕСТИ СПИСОК ВСЕХ РАБОТ')
    print(get('http://localhost:5000/api/jobs').json())
    print()
    print('НИЖЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД 0')
    print(get('http://localhost:5000/api/jobs/1').json())
    print()
    print('НИЖЕ НЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД 999')
    print(get('http://localhost:5000/api/jobs/999').json())
    print()
    print('НИЖЕ НЕ ДОЛЖНА ПОЯВИТСЯ РАБОТА С ИД asd')
    print(get('http://localhost:5000/api/jobs/asd').json())
    print()

