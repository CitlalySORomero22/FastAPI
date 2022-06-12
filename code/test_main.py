from fastapi.testclient import Testclient Import "fastapi.testclient" could not be resolved

from main import app
clientes = Testclient{app}

def test_index():
    response = clientes.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}