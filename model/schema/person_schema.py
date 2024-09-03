from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from model.entity import Person


class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True
