from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Team
from model.schema.player_schema import PlayerSchema


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_relationships = True
        load_instance = True

    players = fields.RelatedList(fields.Nested(PlayerSchema))
