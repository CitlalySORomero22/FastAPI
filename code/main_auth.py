import hashlib  # importa la libreria hashlib 
import sqlite3 
import os 
from typing import List 
from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from pydantic import BaseModel 
from typing import Union  

app = FastAPI() 

DATABASE_URL = os.path.join("sql/clientes.sqlite") 

security = HTTPBasic() 

class Usuarios(BaseModel): 
    username: str 
    level: int 

class Respuesta (BaseModel) :  
     message: str  
           
class Cliente (BaseModel):  
     id_cliente: int  
     nombre: str  
     email: str  
   
class ClienteIN(BaseModel): 
    nombre: str 
    email : str 

@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 
  
@app.get("/clientes/") 
async def clientes(): 
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
def post_cliente(cliente: ClienteIN):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email))
        cursor.fetchall()
        response = {"message":"Cliente insertado"}
        return response



@app.put("/clientes/", response_model=Respuesta)
async def clientes_update(nombre: str="", email:str="", id_cliente:int=0):
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(nombre, email, id_cliente))
        cursor.fetchall()
        response = {"message":"Cliente actualizado"}
        return response

@app.delete("/clientes/{id}") 
async def clientes(id): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(int(id))) 
         cursor.fetchall() 
         response = {"message":"Cliente eliminado"}
         return response

#GET  
 
def get_current_level(credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[1] 
@app.get( 
    "/clientes/", 
    response_model=List[Usuarios], 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Regresa una lista de todos los clientes", 
    description="Regresa una lista de todos los clientes", 
) 
async def get_clientes(level: int = Depends(get_current_level)): 
    if level == 1:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )

#Get id
def getid_current_level(id:int=0,credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "SELECT * FROM clientes WERE WHERE id_cliente =?" (id),
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[1] 
@app.get( 
    "/clientes/{id}", 
    response_model=List[Usuarios], 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Regresa lista del cliente que especificaste", 
    description="Regresa lista del cliente que especificaste", 
) 
async def get_clientes(level: int = Depends(getid_current_level)): 
    if level == 1:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )


# POST

 
def post_current_level(cliente: ClienteIN, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.post( 
    "/clientes/", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Muestra el cliente insertado", 
    description="Muestra el cliente insertado", 
    
)       
    
async def post_clientes(level: int = Depends(post_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )

#PUT
def put_current_level(nombre: str="", email:str="", id_cliente:int=0, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.put( 
    "/clientes/", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Regresa al usuario actualizado", 
    description="Regresa al usuario actualizado", 
    
)       
    
async def put_clientes(level: int = Depends(put_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(nombre, email, id_cliente)) 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )

       

#DELETE
def delete_current_level(id: int=0, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "DELETE FROM clientes WHERE id_cliente=?;",(id)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.delete( 
    "/clientes/{id}", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Muestra que ya no esta el cliente, por que fue eliminado", 
    description="Muestra que ya no esta el cliente, por que fue eliminado", 
) 
async def delete_clientes(level: int = Depends(delete_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )