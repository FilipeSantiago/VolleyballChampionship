from model.schema.match_schema import MatchSchema
from repository.base_repository import BaseRepository, unaccent
from model.entity import Player, Team, Position, Person, Championship, Match, GroupTeamScore, Group
from sqlalchemy import desc
import traceback


class MatchRepository(BaseRepository):

    def get_entity_type(self):
        return Match.mro()[0]

    def get_schema(self):
        return MatchSchema()

    def get_schema_type(self):
        return MatchSchema

    def query_by_filters(self, page=None, size=None, championship=None, *args, **kwargs):
        try:
            query = self.base_query(championship=championship)

            if page is not None and size is not None:
                query = self.base_query(championship=championship) \
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

    def query_num_records_with_filters(self, championship, *args, **kwargs):
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

        results = self.session.query(Match) \
            .join(GroupTeamScore, Match.team1) \
            .join(Group, GroupTeamScore.group) \
            .join(Championship, Group.championship) \
            .filter(Championship.id == championship).order_by(Match.phase_group_order)

        results = results.order_by(Match.winner_id, Match.order)

        return results
