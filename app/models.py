from sqlalchemy import Column, Integer,String,Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):           #whenever we statr our application alchemy will check if that table exists, if no it will create one based on the code we wrote and if yes it won't do anything
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False )
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User") # sets a relationship between this variable and the chosen table(we need to update the schema we want to relate)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False )
    email = Column(String , nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Vote(Base):  # creating a table that connects between user and a post (like) and when they are post primery so the enry is a primary key 
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
