from model.base import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Championship(Base):
    __tablename__ = 'Championship'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    date = Column(Date)

    teams = relationship('Team', back_populates='championship')
    groups = relationship('Group', back_populates='championship')
