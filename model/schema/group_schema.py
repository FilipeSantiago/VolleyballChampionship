from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Group


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        include_relationships = True
        load_instance = True

    group_teams = fields.RelatedList(fields.Nested('GroupTeamScoreSchema'))
