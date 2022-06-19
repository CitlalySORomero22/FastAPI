from fastapi import FastAPI 
from typing import Union 
import sqlite3 
from typing import List 
from pydantic import BaseModel 
  
class Respuesta (BaseModel) : 
     message: str 
          
  
class Cliente (BaseModel): 
     id_cliente: int 
     nombre: str 
     email: str 
  
class ClienteINS (BaseModel):
     nombre: str
     email: str

app =FastAPI() 
  
@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 
  
@app.get("/clientes/") 
async def clientess(): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("SELECT * FROM clientes") 
         response=cursor.fetchall() 
         return response 
         return {"message": "API REST"} 
  
@app.get("/clientes/{id}") 
async def clientes(id): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
         response=cursor.fetchall() 
         return response

@app.post("/clientes/", response_model=Respuesta)
def post_cliente(cliente: ClienteINS):
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email))
        cursor.fetchall()
        response = {"message":"Cliente insertado"}
        return response

      