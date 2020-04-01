import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Kit(SqlAlchemyBase):
    __tablename__ = 'kits'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    prod_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("producers.id"))
    prod = orm.relation('Producer')