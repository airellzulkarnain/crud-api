from enum import Enum
from fastapi import FastAPI, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import psycopg2
import os


origins = [
    'http://127.0.0.1:8080', 
]

DATABASE_URL = os.environ['DATABASE_URL']

class Column(str, Enum):
    Name = "name"
    Username = "username"
    Password = "password"

class User(BaseModel):
    name: str
    username: str
    password: str

db = psycopg2.connect(DATABASE_URL, sslmode='require')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cursor = db.cursor()

@app.post('/insert/')
async def insert_db(user: User):
    cursor.execute('INSERT INTO user (name, username, password) VALUES (%s,%s, MD5(%s))', (user.name, user.username, user.password))
    db.commit()
    return {'message': f'added user row with {user.name}|{user.username}', 'status':'oke'}

@app.put('/update/{column}/{id}/')
async def update_db(column:Column, id: int, value: str = Body(..., embed=True)):
    if column.value == Column.Password.value:
        cursor.execute('UPDATE user SET password=MD5(%s) WHERE ID=%s', (value, id))
    if column.value == Column.Name.value:
        cursor.execute('UPDATE user SET name=%s WHERE ID=%s', (value, id))
    if column.value == Column.Username.value:
        cursor.execute('UPDATE user SET username=%s WHERE ID=%s', (value, id))
    db.commit()
    return {'message': f'successfully update {column.value} of table with ID: {id} to {value}'}

@app.delete('/delete/{id}/')
async def delete_db(id: int):
    cursor.execute('DELETE FROM user WHERE ID=%s',(id, ))
    db.commit()
    return {'message': f'table with ID: {id} have been deleted'}

@app.get('/select/')
async def select_db():
    cursor.execute('SELECT ID, name, username FROM user')
    return {"message": "query success", "row": cursor.fetchall()}
