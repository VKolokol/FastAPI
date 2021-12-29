import datetime

import sqlalchemy

from db.base import metadata


proposals = sqlalchemy.Table(
    "proposals",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),

    sqlalchemy.Column("user_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),

    sqlalchemy.Column("job_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False),

    sqlalchemy.UniqueConstraint('user_id', 'job_id', name='uix_1'),
    sqlalchemy.Column('in_process', sqlalchemy.Boolean, default=True, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=True),
    sqlalchemy.Column('in_archive', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column('updated_at', sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
