from service.championship_service import ChampionshipService
from controller.base_controller import BaseController


class ChampionshipController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = ChampionshipService()
