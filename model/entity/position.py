from model.base import Base
from sqlalchemy import Column, Integer, String


class Position(Base):
    __tablename__ = 'Position'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)
