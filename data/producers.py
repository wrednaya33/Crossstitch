import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Producer(SqlAlchemyBase):
    __tablename__ = 'producers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    logo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kits = orm.relation("Kit", back_populates='prod')
    books = orm.relation("Booklet", back_populates='prod')


