from sqlalchemy.orm import relationship

from model.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from model.entity.group import Group
from model.entity.team import Team


class GroupTeamScore(Base):
    __tablename__ = 'GroupTeamScore'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.id))
    team_id = Column(Integer, ForeignKey(Team.id))

    score = Column(Integer, default=0)
    point_balance = Column(Integer, default=0)

    team = relationship('Team')
    group = relationship('Group', back_populates='group_teams')
