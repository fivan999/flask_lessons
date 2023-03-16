import sqlalchemy
import sqlalchemy.orm


SqlAlchemyBase = sqlalchemy.orm.declarative_base()

__factory = None


def global_init(db_file: str) -> None:
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('Укажите файл базы данных')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sqlalchemy.create_engine(conn_str, echo=True)
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> sqlalchemy.orm.Session:
    global __factory
    return __factory()
