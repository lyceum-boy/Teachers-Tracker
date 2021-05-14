import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("teachers.id"))
    students_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timetable = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    teacher = orm.relation('Teacher')

    def __repr__(self):
        return f'<Group> {self.id} {self.title}'
