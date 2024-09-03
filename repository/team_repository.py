from repository.base_repository import BaseRepository, unaccent
from model.entity import Team, Championship
from model.schema.team_schema import TeamSchema
import traceback


class TeamRepository(BaseRepository):

    def get_entity_type(self):
        return Team.mro()[0]

    def get_schema_type(self):
        return TeamSchema

    def get_schema(self):
        return TeamSchema()

    def query_by_filters(self, page=None, size=None, championship=None):
        try:
            query = self.base_query(championship)

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

    def query_num_records_with_filters(self):
        try:
            num_results = self.base_query().count()
            return num_results
        except Exception as e:
            traceback.print_exc()
            self.session.rollback()
            raise e
        finally:
            self.commit_and_close()

    def base_query(self, championship=None):
        results = self.session.query(Team)

        if championship:
            results.join(Championship, Team.championship)
            results.filter(Championship.id == championship)

        return results
