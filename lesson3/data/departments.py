import sqlalchemy
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    """модель департамент"""

    __tablename__ = 'departments'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')
    )
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    user = sqlalchemy.orm.relationship('User')
