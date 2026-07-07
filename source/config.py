from dotenv import dotenv_values


v = dotenv_values('.env')


URL=v['DATABASE_URL']