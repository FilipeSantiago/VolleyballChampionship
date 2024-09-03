from model.base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from model.entity import GroupTeamScore


class Match(Base):
    __tablename__ = 'Matches'

    id = Column(Integer, primary_key=True)

    team1_id = Column(Integer, ForeignKey(GroupTeamScore.id))
    team1_score = Column(Integer, default=0)
    
    team2_id = Column(Integer, ForeignKey(GroupTeamScore.id))
    team2_score = Column(Integer, default=0)

    winner_id = Column(Integer, ForeignKey(GroupTeamScore.id))

    team1 = relationship('GroupTeamScore', foreign_keys=[team1_id])
    team2 = relationship('GroupTeamScore', foreign_keys=[team2_id])
    winner = relationship('GroupTeamScore', foreign_keys=[winner_id])

    phase_group = Column(String)
    phase_group_order = Column(Integer)

    order = Column(Integer)
