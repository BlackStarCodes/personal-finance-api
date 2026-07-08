from dotenv import dotenv_values


v = dotenv_values('.env')


URL=v['DATABASE_URL']
SECRET_KEY=v["SECRET_KEY"]
ALGO=v["ALGORITHM"]
TOKEN_EXPIRE_MINS=30