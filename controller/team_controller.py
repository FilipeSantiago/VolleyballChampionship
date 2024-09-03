from service.team_service import TeamService
from controller.base_controller import BaseController


class TeamController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = TeamService()
