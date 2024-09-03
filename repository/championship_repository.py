from repository.base_repository import BaseRepository, unaccent
from model.entity import Championship
from model.schema.championship_schema import ChampionshipSchema
import traceback


class ChampionshipRepository(BaseRepository):

    def get_entity_type(self):
        return Championship.mro()[0]

    def get_schema_type(self):
        return ChampionshipSchema

    def get_schema(self):
        return ChampionshipSchema()

    def query_all_with_filters(self, page=None, size=None):
        try:
            query = self.base_query()

            if page is not None and size is not None:
                query = self.base_query() \
                    .limit(size) \
                    .offset(page * size)

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

    def base_query(self):
        results = self.session.query(Player)
        return results
