from repository.group_repository import GroupRepository
from service.base_service import BaseService
from repository.match_repository import MatchRepository


class MatchService(BaseService):

    def get_repository_type(self):
        return MatchRepository.mro()[0]

    def query_all(self, *args, **kwargs):
        result = self.repository.query_by_filters(*args, **kwargs)
        return result

    def create_championship_initial_matches(self, championship):
        group_repository = GroupRepository()

        groups = group_repository.query_by_filters(championship=championship)

        matches = []
        for group in groups:
            matches += self.__create_group_matches(group['group_teams'])

        self.insert_many(matches)
        return matches

    def create_championship_next_phase_matches(self, championship):
        phases = ['group_phase', 'quarterfinals', 'semifinals', 'third_place', 'finals']

        matches = self.repository.query_by_filters(championship=championship)

        if len(matches) == 0:
            return self.create_championship_initial_matches(championship)

        current_phase, next_phase = self.__get_current_phase(matches)
        matches = list(filter(lambda x: x['phase_group'] == current_phase, matches))

        if self.__can_create_next_phase(matches):
            next_phase_matches = self.__create_next_phase_matches(matches, current_phase, next_phase, championship)
            self.insert_many(next_phase_matches)
            return next_phase_matches

        return False

    def update(self, model):
        bd_match = self.repository.query_by_id(model.id)

        if bd_match['winner'] is not None:
            self.__undo_match_points(bd_match)

        self.__add_match_points(bd_match, model)

        result = self.repository.update(bd_match)
        return result

    @staticmethod
    def __undo_match_points(bd_match):
        if bd_match['team1_score'] > bd_match['team2_score']:
            winner = bd_match['team1']
            loser = bd_match['team2']
        else:
            winner = bd_match['team2']
            loser = bd_match['team1']

        bd_match['winner'] = winner
        if bd_match['phase_group'] == 'group_phase':
            bd_match['team1']['point_balance'] += int(bd_match['team2_score']) - int(bd_match['team1_score'])
            bd_match['team2']['point_balance'] += int(bd_match['team1_score']) - int(bd_match['team2_score'])

            if abs(bd_match['team1_score'] < 20 or bd_match['team2_score']) < 20:
                winner['score'] -= 3
            else:
                winner['score'] -= 2
                loser['score'] -= 1

    @staticmethod
    def __add_match_points(bd_match, model):
        bd_match['team1_score'] = int(model.team1_score)
        bd_match['team2_score'] = int(model.team2_score)

        if bd_match['team1_score'] > bd_match['team2_score']:
            winner = bd_match['team1']
            loser = bd_match['team2']
        else:
            winner = bd_match['team2']
            loser = bd_match['team1']

        bd_match['winner'] = winner

        if bd_match['phase_group'] == 'group_phase':
            bd_match['team1']['point_balance'] += int(model.team1_score) - int(model.team2_score)
            bd_match['team2']['point_balance'] += int(model.team2_score) - int(model.team1_score)

            if abs(bd_match['team1_score'] < 20 or bd_match['team2_score']) < 20:
                winner['score'] += 3
            else:
                winner['score'] += 2
                loser['score'] += 1

    def __create_next_phase_matches(self, matches, current_phase, next_phase, championship):
        next_phase_matches = []

        if current_phase == 'group_phase':
            group_repository = GroupRepository()
            groups = group_repository.query_by_filters(championship=championship)

            if len(groups) > 2:
                raise NotImplementedError

            group_1_teams = sorted(groups[0]['group_teams'], key=lambda x: (x['score'], x['point_balance']),
                                   reverse=True)[:4]
            group_2_teams = sorted(groups[1]['group_teams'], key=lambda x: (x['score'], x['point_balance']),
                                   reverse=True)[:4][::-1]

            for i in range(len(group_1_teams)):
                new_match = {
                    "team1_id": group_1_teams[i]['id'],
                    "team2_id": group_2_teams[i]['id'],
                    'team1': group_1_teams[i],
                    'team2': group_2_teams[i],
                    'phase_group': next_phase,
                    'order': i
                }
                next_phase_matches.append(new_match)

        elif current_phase not in ['third_place', 'finals']:
            matches = sorted(matches, key=lambda x: x['order'])
            i = 0
            while i <= len(matches) / 2:
                new_match = {
                    "team1_id": matches[i]['winner'],
                    "team2_id": matches[i + 1]['winner'],
                    'phase_group': next_phase,
                    'order': i
                }
                i += 2
                next_phase_matches.append(new_match)

        return next_phase_matches

    @staticmethod
    def __create_group_matches(teams):

        matches = []

        i = 0
        while i < len(teams):
            j = i + 1
            while j < len(teams):
                match = {
                    "team1_id": teams[i]['id'],
                    "team2_id": teams[j]['id'],
                    "team1": teams[i],
                    "team2": teams[j],
                    "phase_group": 'group_phase'
                }
                j += 1
                matches.append(match)
            i += 1

        return matches

    @staticmethod
    def __get_current_phase(matches):
        taken_phases = list(set(list(map(lambda x: x['phase_group'], matches))))

        if 'finals' in taken_phases:
            return 'finals', None
        elif 'semifinals' in taken_phases:
            return 'semifinals', 'finals'
        elif 'quarterfinals' in taken_phases:
            return 'quarterfinals', 'semifinals'
        elif 'group_phase' in taken_phases:
            return 'group_phase', 'quarterfinals'

        return 'group_phase', 'quarterfinals'

    @staticmethod
    def __can_create_next_phase(matches):
        unfinished_matches = list(filter(lambda x: x['winner'] is None, matches))
        return len(unfinished_matches) == 0
