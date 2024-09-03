from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelConversionError
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_marshmallow import Marshmallow

from init_config import InitConfig

config = InitConfig().get_config()
ma = Marshmallow()


DB_USER = config["database_config"]["user"]
DB_PASS = config["database_config"]["pass"]
DB_NAME = config["database_config"]["database"]
DB_SERVICE = config["database_config"]["service"]
DB_PORT = config["database_config"]["port"]
DB_IP = config["database_config"]["ip"]
DB_SCHEMA = config["database_config"]["schema"]

engine = create_engine(f'{DB_SERVICE}://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_NAME}', poolclass=NullPool)

metadata = MetaData(schema=DB_SCHEMA)
session_factory = sessionmaker(bind=engine)

Base = declarative_base(metadata=metadata)

# CREATING DATABASE ....
from model.entity import Team, Group, GroupTeamScore, Match, Championship, Player, Position
Base.metadata.create_all(engine)


def initialize_sql():
    Base.metadata.create_all(engine)


def setup_schema(Base, session):
    # Create a function which incorporates the Base and session information
    def setup_schema_fn():
        for class_ in Base._decl_class_registry.values():
            if hasattr(class_, "__tablename__"):
                if class_.__name__.endswith("Schema"):
                    raise ModelConversionError(
                        "For safety, setup_schema can not be used when a"
                        "Model class ends with 'Schema'"
                    )

                class Meta(object):
                    model = class_
                    sqla_session = session

                schema_class_name = "%sSchema" % class_.__name__
                schema_class = type(schema_class_name, (ma.ModelSchema,), {"Meta": Meta})
                setattr(class_, "__marshmallow__", schema_class)

    return setup_schema_fn
