import datetime
from sqlalchemy_serializer import SerializerMixin
import sqlalchemy

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now())
    end_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now())
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f'Работа {self.job}, лидером является {self.team_leader}. На нее уйдет примерно {self.work_size} дней,' \
               f' если участовавть будут {self.collaborators}. Дата начала: {self.start_date},' \
               f' дата заврешения: {self.end_date}'
