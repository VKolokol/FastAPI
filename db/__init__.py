from db.jobs import jobs
from db.users import users
from db.proposals import proposals
from db.base import metadata, engine

metadata.create_all(bind=engine)
