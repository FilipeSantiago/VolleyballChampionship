from service.group_service import GroupService
from controller.base_controller import BaseController
from flask import request


class GroupController(BaseController):

    def __init__(self):
        super().__init__()
        self.service = GroupService()

    def post(self, *args, **kwargs):
        model = request.json

        result = self.get_service().create_groups(**model)
        return result
