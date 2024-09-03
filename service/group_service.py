import math
import random

from model.schema.group_schema import GroupSchema
from service.base_service import BaseService
from repository.group_repository import GroupRepository
from repository.team_repository import TeamRepository


class GroupService(BaseService):

    def get_repository_type(self):
        return GroupRepository.mro()[0]

    def query_all(self, *args, **kwargs):
        result = self.repository.query_by_filters(*args, **kwargs)
        return result

    def create_groups(self, number_of_groups, championship):
        team_repository = TeamRepository()
        teams = team_repository.query_by_filters(championship=championship)

        teams_per_group = math.ceil(len(teams) / number_of_groups)
        random.shuffle(teams)

        i = 0
        created_groups = []
        while i < number_of_groups:
            group = {'name': f'Grupo {i + 1}',
                     'championship': championship,
                     'group_teams': \
                         list(map(lambda x: {'team': x}, teams[i * teams_per_group:(i + 1) * teams_per_group]))}
            inserted_group = self.repository.insert(group)
            created_groups.append(inserted_group)
            i += 1

        return created_groups
