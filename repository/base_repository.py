from abc import abstractmethod
from sqlalchemy import event
from sqlalchemy.orm import mapper, scoped_session
from model.base import Base, setup_schema, initialize_sql
import traceback
from sqlalchemy.sql.functions import ReturnTypeFromArgs

from model.base import session_factory


class unaccent(ReturnTypeFromArgs):
    pass


class BaseRepository:

    def __init__(self):
        initialize_sql()
        self.scoped_session = scoped_session(session_factory)
        self.session = self.scoped_session()

        event.listen(mapper, "after_configured", setup_schema(Base, self.scoped_session))

    @abstractmethod
    def get_entity_type(self):
        pass

    @abstractmethod
    def get_schema_type(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass

    def insert(self, schema):
        try:
            model = self.get_schema().load(schema, session=self.session)
            self.session.add(model)
            self.session.flush()

            schema_type = self.get_schema_type()
            parsed_result = schema_type().dump(model)
            return parsed_result
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def insert_many(self, schema):
        try:
            model = self.get_schema().load(schema, session=self.session, many=True)
            self.session.bulk_save_objects(model)
            self.session.flush()

            schema_type = self.get_schema_type()
            parsed_result = schema_type().dump(model, many=True)
            return parsed_result
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def update(self, schema):
        try:
            model = self.get_schema().load(schema, session=self.session)
            result = self.session.merge(model)
            schema_type = self.get_schema_type()
            parsed_result = schema_type().dump(result)
            return parsed_result
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def delete(self, schema):
        try:
            model = self.get_schema().load(schema, session=self.session)
            entity_type = self.get_entity_type()
            result = self.session.query(entity_type).filter(entity_type.id == model.id).update({"is_deleted": True})
            return result
        except:
            traceback.print_exc()
            self.session.rollback()
        finally:
            self.commit_and_close()

    def query_by_id(self, identifier):
        try:
            entity_type = self.get_entity_type()
            result = self.session.query(entity_type).filter(entity_type.id == identifier).one()
            schema_type = self.get_schema_type()
            parsed_result = schema_type().dump(result)
            return parsed_result
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def query_all(self, page, size, *args, **kwargs):
        try:
            entity_type = self.get_entity_type()
            results = self.session.query(entity_type).limit(size).offset(page * size)
            schema_type = self.get_schema_type()
            parsed_results = schema_type(many=True).dump(results)
            return parsed_results
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def query_num_records(self, *args, **kwargs):
        try:
            entity_type = self.get_entity_type()
            result = self.session.query(entity_type).count()
            return result
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def commit_and_close(self):
        self.session.commit()
        self.scoped_session.remove()

    @staticmethod
    def convert_to_dict(result):
        rows = {}
        fields = enumerate(result._real_fields)

        for index, field in fields:
            rows[field] = result[index]

        return rows
