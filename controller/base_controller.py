from flask.views import MethodView
from flask import request


class BaseController(MethodView):

    size_default = 10
    page_default = 0

    def __init__(self):
        self.desired_claims = {
            "get": None,
            "patch": None,
            "put": None,
            "post": None,
            "delete": None
        }

    def get_service(self):
        return self.service

    def get(self, id=None, list=None, *args, **kwargs):
        if id is not None:
            result = self.get_service().query_by_id(id)
        else:
            size = int(request.args['_size']) if '_size' in request.args else self.size_default
            page = int(request.args['_page']) if '_page' in request.args else self.page_default
            num_records = self.get_service().query_num_records(**request.args)

            result = self.get_service().query_all(**request.args, page=page, size=size)
            result = self._encapsulate_response(response=result, page=page, size=size, num_records=num_records)

        return result

    def patch(self, *args, **kwargs):
        return None

    def post(self, *args, **kwargs):
        model = request.json
        result = self.get_service().insert(model)
        return result

    def delete(self, *args, **kwargs):
        model = request.json

        if request.json is None:
            model = {'id': request.base_url.split('/')[-1]}

        entity_type = self.get_service().get_entity_type()
        entity = entity_type(**model)
        result = self.get_service().delete(entity)
        return {"result": result}

    def put(self, *args, **kwargs):
        model = request.json
        entity_type = self.get_service().get_entity_type()
        entity = entity_type(**model)
        result = self.get_service().update(entity)
        return result

    @staticmethod
    def _encapsulate_response(response, page, size, num_records):
        result = {
            'content': response,
            'totalElements': num_records,
            'pageable': {
                'pageSize': size,
                'pageNumber': page
            }
        }

        return result

    @staticmethod
    def options():
        return {
            "statusCode": "200",
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            }
        }
