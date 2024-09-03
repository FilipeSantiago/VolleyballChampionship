from model.base import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from model.entity.championship import Championship


class Team(Base):
    __tablename__ = 'Team'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Float)
    championship_id = Column(Integer, ForeignKey(Championship.id))

    championship = relationship('Championship', back_populates='teams')

    players = relationship('Player', back_populates='team')
