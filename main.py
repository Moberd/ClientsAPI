from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import pymysql.cursors


app = FastAPI()
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='clients',
                             cursorclass=pymysql.cursors.DictCursor)

# Pydantic model for item data
class Client(BaseModel):
    name: str
    surname: str
    age: int


@app.get("/api_description")
async def get_api_description():
    description = [
        {"route":"/clients/", "method": "GET","type": "list", "fields":[]},
        {"route":"/new_client/", "method": "POST", "type": "form", "fields": ["name", "surname", "age"]},
        {"route":"/delete_client/{client_id}", "method": "DELETE", "type": "form", "fields": ["client_id"]}
    ]
    return description


@app.get("/clients", response_model=List[Client])
def get_all_clients():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM clients"
        cursor.execute(sql)
        res = cursor.fetchall()
    return res


@app.post("/new_client", response_model=Client)
async def add_new_client(client: Client):
    with connection.cursor() as cursor:
        sql = f"INSERT INTO clients (name, surname, age) VALUES('{client.name}', '{client.surname}', '{client.age}');"
        cursor.execute(sql)
    connection.commit()
    return client


@app.delete("/delete_client/{client_id}", response_model=Client)
async def delete_client(client_id: int):
    with connection.cursor() as cursor:
        sql_get = f"SELECT * FROM clients WHERE id={client_id}"
        cursor.execute(sql_get)
        client = cursor.fetchone()
        sql_del = f"DELETE FROM clients WHERE id = {client_id};"
        cursor.execute(sql_del)
    connection.commit()
    return client

