import os
import bcrypt

from pony.orm import *

db = Database()


# criação da tabela User
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password_hash = Required(str)

    def set_password(self, password: str):
        password_bytes = bytes(password, 'utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        self.password_hash = hashed_bytes.decode('utf-8')

    def validate_password(self, password: str) -> bool:
        password_bytes = bytes(password, 'utf-8')
        hashed_bytes = bytes(self.password_hash, 'utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)


# criação da tabela Aventura
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


@db_session
def add_user(login: str, password: str) -> User:
    user = User(login=login, password_hash='temp')
    user.set_password(password)
    return user


@db_session
def get_user(id: int) -> User:
    user = User[id]
    return user


@db_session
def verify_password(login: str, password: str) -> User:
    query = select(u for u in User if u.login == login)

    user: User = query.first()
    if user.validate_password(password):
        return user
    return None
