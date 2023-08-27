from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine
from sqlalchemy import Text, DateTime, Boolean, select, insert, update, delete, or_, and_
from icecream import ic
connection_string = "sqlite:///D:\pythonProject\VTI-Python-2\BTL_DJANGO\django_HTA_Todo\db.sqlite3"
engine = create_engine(connection_string, echo= True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class base_task(Base):
    __tablename__ = 'base_task'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    complete = Column(Integer)
    created = Column(DateTime)
    user_id = Column(Integer)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()



result = session.query(base_task).all()

def show_all():
    for row in result:
        print("ID:", row.id,"Title:", row.title,"Description:",row.description,"Complete:",row.complete,"Created:",row.created,"User_id:",row.user_id,)

def query_filter():
    result = session.query(base_task).filter(base_task.id >30)
    print(result)

def equals():
    result = session.query(base_task).filter(base_task.id == 30)
    for row in result:
        print("ID:", row.id,"Title:", row.title,"Description:",row.description,"Complete:",row.complete,"Created:",row.created,"User_id:",row.user_id,)
def not_equals():
    result = session.query(base_task).filter(base_task.id != 28)
    for row in result:
        print("ID:", row.id,"Title:", row.title,"Description:",row.description,"Complete:",row.complete,"Created:",row.created,"User_id:",row.user_id,)

def like():
    result = session.query(base_task).filter(base_task.title.like('Play%'))
    for row in result:
        print("ID:", row.id,"Title:", row.title,"Description:",row.description,"Complete:",row.complete,"Created:",row.created,"User_id:",row.user_id,)

def In():
    result = session.query(base_task).filter(base_task.id.in_([25,30]))
    for row in result:
        print("ID:", row.id,"Title:", row.title,"Description:",row.description,"Complete:",row.complete,"Created:",row.created,"User_id:",row.user_id,)

def All():
    result = session.query(base_task).all()
    print(result)


if __name__ == "__main__":
    ic("------ show_all() ------")
    show_all()
    ic("------ query_filter() ------")
    query_filter()
    ic("------ equals() ------")
    equals()
    ic("------ not_equals() ------")
    not_equals()
    ic("------ like() ------")
    like()
    ic("------ In() ------")
    In()
    ic("------ ALL() ------")
    All()