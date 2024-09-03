from model.base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from model.entity.championship import Championship


class Group(Base):
    __tablename__ = 'Group'

    id = Column(Integer, primary_key=True)
    championship_id = Column(Integer, ForeignKey(Championship.id))

    name = Column(String)
    championship = relationship('Championship', back_populates='groups')

    group_teams = relationship('GroupTeamScore', back_populates='group')
