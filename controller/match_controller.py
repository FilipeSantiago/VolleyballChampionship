from service.match_service import MatchService
from controller.base_controller import BaseController
from flask import request


class MatchController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = MatchService()

    def post(self, *args, **kwargs):
        model = request.json

        result = self.get_service().create_championship_next_phase_matches(**model)

        if result is False:
            return {"motive": "MATCHES_SHOULD_BE_FINISHED"}, 437

        return result
