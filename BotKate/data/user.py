import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_vk = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    condition_photo = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)