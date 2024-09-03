from model.base import Base
from sqlalchemy import Column, Integer, Float, String


class Person(Base):
    __tablename__ = 'Person'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    cpf = Column(String)
    height = Column(Float)
