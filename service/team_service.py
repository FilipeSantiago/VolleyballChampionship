from service.base_service import BaseService
from repository.team_repository import TeamRepository


class TeamService(BaseService):

    def get_repository_type(self):
        return TeamRepository.mro()[0]

    def query_all(self, *args, **kwargs):
        result = self.repository.query_by_filters(*args, **kwargs)
        return result
