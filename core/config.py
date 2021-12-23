from starlette.config import Config

config = Config(".env.dev")

DATABASE_URL = config("PG_DATABASE_URL", cast=str, default='')

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)
ALGORITHM = config("ALGORITHM", cast=str, default='HS256')
SECRET_KEY = config("PR_SECRET_KEY", cast=str, default='')
