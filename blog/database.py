from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://blog:blog@127.0.0.1:3306/blog"

# ここを True / False で切り替えて autobegin の挙動を試す
AUTOBEGIN = True

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine, autobegin=AUTOBEGIN)
