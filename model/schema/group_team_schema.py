from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import GroupTeamScore
from model.schema.group_schema import GroupSchema
from model.schema.team_schema import TeamSchema


class GroupTeamScoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GroupTeamScore
        include_relationships = True
        load_instance = True

    team = fields.Nested(TeamSchema)
    group = fields.Nested(GroupSchema, exclude=['group_teams'])
