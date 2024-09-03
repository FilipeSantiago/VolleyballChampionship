from service.player_service import PlayerService
from controller.base_controller import BaseController


class PlayerController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = PlayerService()
