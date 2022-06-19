from fastapi.testclient import TestClient

from code.main import app

clientes = TestClient(app)

def test_index():
    response = clientes.get("/") # request,
    data = {"message": "API REST"}
    assert response.status_code == 200
    assert response.json() == data

def test_post_clientes():
    payload = {"id_cliente":1, "nombre": "Alondra", "email": "alo@email.com"}
    response = clientes.post("/clientes/", json=payload)
    data = {"message": "Cliente agregado"}
    assert response.status_code == 200
    assert response.json() == data

def test_put_clientes():
    payload = {"id_cliente":1, "nombre": "Alondra", "email": "alo@email.com"}
    response = clientes.put("/clientes/", json=payload)
    data = {"message": "Cliente actualizado"}
    assert response.status_code == 200
    assert response.json() == data

def test_delete_clientes():
    payload = {"id_cliente":1, "nombre": "Alondra", "email": "alo@email.com"}
    response = clientes.delete("/clientes/1", json=payload)
    data = {"message": "Cliente borrado"}
    assert response.status_code == 200
    assert response.json() == data


