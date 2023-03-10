import sqlalchemy
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    """модель категории"""

    __tablename__ = 'categories'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(sqlalchemy.String)
    jobs = sqlalchemy.orm.relationship('Jobs', back_populates='category')
