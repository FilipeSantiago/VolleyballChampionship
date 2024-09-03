from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Position


class PositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Position
        include_relationships = True
        load_instance = True
