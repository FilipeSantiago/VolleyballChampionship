from repository.base_repository import BaseRepository, unaccent
from model.entity import Championship, Group
from model.schema.group_schema import GroupSchema
import traceback


class GroupRepository(BaseRepository):

    def get_entity_type(self):
        return Group.mro()[0]

    def get_schema(self):
        return GroupSchema()

    def get_schema_type(self):
        return GroupSchema

    def query_by_filters(self, page=None, size=None, championship=None):
        try:
            query = self.base_query(championship=championship)

            if page is not None and size is not None:
                query = query.limit(size).offset(page * size)

            results = query.all()

            schema_type = self.get_schema_type()
            parsed_results = []
            for result in results:
                parsed_result = schema_type().dump(result)
                parsed_results.append(parsed_result)
            return parsed_results
        except:
            traceback.print_exc()
            self.session.rollback()
            raise Exception()
        finally:
            self.commit_and_close()

    def query_num_records_with_filters(self, championship, position, team):
        try:
            num_results = self.base_query(championship=championship).count()
            return num_results
        except Exception as e:
            traceback.print_exc()
            self.session.rollback()
            raise e
        finally:
            self.commit_and_close()

    def base_query(self, championship=None):

        results = self.session.query(Group) \
            .join(Championship, Group.championship) \
            .filter(Championship.id == championship)

        return results
