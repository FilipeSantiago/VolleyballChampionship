from model.base import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from model.entity.team import Team
from model.entity.person import Person
from model.entity.position import Position


class Player(Base):
    __tablename__ = 'Player'

    id = Column(Integer, primary_key=True)

    person_id = Column(Integer, ForeignKey(Person.id))
    position_id = Column(Integer, ForeignKey(Position.id))
    team_id = Column(Integer, ForeignKey(Team.id))

    score = Column(Float)

    person = relationship('Person')
    position = relationship('Position')

    team = relationship('Team', back_populates='players')
