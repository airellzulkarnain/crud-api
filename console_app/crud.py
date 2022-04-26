from enum import Enum
import requests
import sys

# just leaving something so that i can push to github XD
# add another line
URL = 'https://pkl-crud-api.herokuapp.com'

class Column(str, Enum):
    Name = "name"
    Username = "username"
    Password = "password"

if __name__ == '__main__': 
    if len(sys.argv) > 1 :
        if sys.argv[1] == '--insert' and len(sys.argv) > 4:
            print(requests.post(f'{URL}/insert/', 
            json={'name': f'{sys.argv[2]}', 'username':f'{sys.argv[3]}', 'password':f'{sys.argv[4]}'}).json()['message'])
        elif sys.argv[1] == '--update':
            valid_column = any([x.value == sys.argv[2] for x in Column])
            if len(sys.argv) > 4 and valid_column and sys.argv[3].isnumeric():
                a = requests.put(f'{URL}/update/{sys.argv[2]}/{sys.argv[3]}/', 
                json={'value': sys.argv[4]})
                print(a.status_code, a.text, sep=" | ")
        elif sys.argv[1] == '--delete':
            if sys.argv[2].isnumeric():
                print(requests.delete(f'{URL}/delete/{sys.argv[2]}/').json()['message'])
        elif sys.argv[1] == '--select':
            rows = requests.get(f'{URL}/select/').json()['row']
            for row in rows:
                print(row)
        else:
            print("""
            Insert Operation: 
                python crud.py --insert value1 value2 value3 ...
            Update Operation:
                python crud.py --update column id value1 ...
            Delete Operation: 
                python crud.py --delete id
            Select Operation: 
                python crud.py --select
            """)
