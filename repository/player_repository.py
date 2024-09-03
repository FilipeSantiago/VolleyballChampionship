from repository.base_repository import BaseRepository, unaccent
from model.entity import Player, Team, Position, Person, Championship
from model.schema.player_schema import PlayerSchema
import traceback


class PlayerRepository(BaseRepository):

    def get_entity_type(self):
        return Player.mro()[0]

    def get_schema(self):
        return PlayerSchema()

    def get_schema_type(self):
        return PlayerSchema

    def query_by_filters(self, page=None, size=None, championship=None, position=None, team=None, *args, **kwargs):
        try:
            query = self.base_query()

            if page is not None and size is not None:
                query = self.base_query(championship=championship, position=position, team=team) \
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

    def query_num_records(self, championship=None, position=None, team=None, *args, **kwargs):
        try:
            num_results = self.base_query(championship=championship, position=position, team=team).count()
            return num_results
        except Exception as e:
            traceback.print_exc()
            self.session.rollback()
            raise e
        finally:
            self.commit_and_close()

    def base_query(self, championship=None, position=None, team=None):

        results = self.session.query(Player) \
            .join(Team, Player.team) \
            .join(Championship, Team.championship) \
            .join(Person, Player.person) \
            .join(Position, Player.position) \
            .filter(Championship.id == championship)

        if position is not None:
            results = results.filter(Position.id == position)

        if team is not None:
            results = results.filter(Team.id == team)

        results = results.order_by(Position.id, Person.name)

        return results
