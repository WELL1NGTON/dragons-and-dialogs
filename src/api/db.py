import os

from pony.orm import *

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password = Required(str)


class Aventura(db.Entity):
    id = PrimaryKey(int, auto=True)
    cenario = Required(str)
    classe = Required(str)
    objetivo = Required(str)
    nome_personagem = Required(str)


# informações para conexão do banco
db.bind(
    provider='postgres',
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    database='dragons-and-dialogs',
    port=int(os.getenv('POSTGRES_PORT')),
)

# printa comandos sql no terminal
set_sql_debug(True)

# salva em memória os vinculos com as tabelas, criando se não existir
db.generate_mapping(create_tables=True)

# #passagem de parâmetros para adicionar as tabelas
# user_info = User(login='admin', password='123456')
# user_adventure = Aventura(cenario='cyberpunk', classe='hacker', objetivo='matar o iwata',
#                           nome_personagem='samurai')
# commit()


@db_session
def add_user(login, password):
    login = User(login=login, password=password)
    return login


@db_session
def get_user(id: int) -> User:
    user = User[id]
    return user
