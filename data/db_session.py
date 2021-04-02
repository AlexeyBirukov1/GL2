import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# абстрактную декларативную базу
SqlAlchemyBase = dec.declarative_base()
# сессии подключения к базе данных
__factory = None

# начальная инициализация БД
def global_init(db_file):
    global __factory
    # если уже вызывали, то завершить работу
    if __factory:
        return
    # проверяем адрес БД
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    # создаем строку подключения conn_str (она состоит из типа базы данных,
    # адреса до базы данных и параметров подключения)
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

# Функция create_session нужна для получения сессии подключения к базе данных.
def create_session() -> Session:
    global __factory
    return __factory()