from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Player
from model.schema.person_schema import PersonSchema
from model.schema.position_schema import PositionSchema


class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        include_relationships = True
        load_instance = True

    person = fields.Nested(PersonSchema)
    position = fields.Nested(PositionSchema)
