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


DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username);

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);

SELECT * FROM usuarios;

