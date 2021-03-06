import sqlalchemy

from db.base import metadata
import datetime


jobs = sqlalchemy.Table(
    "jobs",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('email', sqlalchemy.String,  unique=True),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('owner_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    sqlalchemy.Column('salary_from', sqlalchemy.Integer),
    sqlalchemy.Column('salary_to', sqlalchemy.Integer),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column('updated_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
