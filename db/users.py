import datetime

import sqlalchemy

from db.base import metadata


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('hash_password', sqlalchemy.String),
    sqlalchemy.Column('is_company', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, nullable=False, default=True),
    sqlalchemy.Column('is_stuff', sqlalchemy.Boolean, nullable=False, default=False),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column('updated_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
