from service.base_service import BaseService
from repository.championship_repository import ChampionshipRepository


class ChampionshipService(BaseService):

    def get_repository_type(self):
        return ChampionshipRepository.mro()[0]

    def query_all(self, *args, **kwargs):
        result = self.repository.query_by_filters(*args, **kwargs)
        return result
