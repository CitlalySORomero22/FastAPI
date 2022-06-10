DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes(
    id_cliente integer PRIMARY KEY AUTOINCREMENT,
    nombre varchar(50) NOT NULL,
    email varchar (50) NOT NULL
);

INSERT INTO clientes(nombre, email) VALUES ('Alondra', 'alo@email.com');
INSERT INTO clientes(nombre, email) VALUES ('Alice', 'ali@email.com');
INSERT INTO clientes(nombre, email) VALUES ('Alison', 'alis@email.com');

.headers ON

SELECT * FROM clientes;