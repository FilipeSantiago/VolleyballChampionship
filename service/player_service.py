from service.base_service import BaseService
from repository.player_repository import PlayerRepository


class PlayerService(BaseService):

    def get_repository_type(self):
        return PlayerRepository.mro()[0]

    def query_all(self, *args, **kwargs):
        result = self.repository.query_by_filters(*args, **kwargs)
        return result
