from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Match
from model.schema.group_team_schema import GroupTeamScoreSchema


class MatchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Match
        include_relationships = True
        include_fk = True
        load_instance = True

    team1 = fields.Nested(GroupTeamScoreSchema)
    team2 = fields.Nested(GroupTeamScoreSchema)
