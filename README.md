# FastApi do Zero

## A API
  Possui 4 endpoints principais:
  1. **Users** - contém dados do usuário para que possar ser usando durante a autenticação e tipo de permissão.
  2. **Clients** - dados dos clientes
  3. **Products** - dados de produtos com imagens
  4. **Orders** - dados de pedidos dos clientes


## O banco de dados / ORM
  A modelagem do banco deve contar com quatro tabelas: User, Client, Product e Order. Onde Order e o Product se relacionam da forma que os produtos podem estar relacionado a diversos pedidos e diversos pedidos devem ser associados a um único cliente.

## Requisitos

  1. Python 3.12+
  2. FastAPI
  3. SQLAlchemy
  4. Poetry
  5. PostgreSQL
  6. Docker
  7. Pytest

## Setup
Create an `.env` file like `.env.example` and set values and run:

### Without Docker
  #### Using Terminal
    $ poetry install
    $ poetry shell
    $ task test
    $ task run

### With Docker
  #### Using Terminal
    $ docker compose up -d
    $ docker compose down


- Serving at: http://0.0.0.0:8000
- API docs: http://0.0.0.0:8000/docs
- API redoc: http://0.0.0.0:8000/redoc

