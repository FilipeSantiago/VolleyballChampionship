from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Championship
from model.schema.team_schema import TeamSchema


class ChampionshipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Championship
        include_relationships = True
        load_instance = True

    teams = fields.RelatedList(fields.Nested(TeamSchema))
