from abc import abstractmethod


class BaseService:

    def __init__(self):
        repository_type = self.get_repository_type()
        self.repository = repository_type()

    @abstractmethod
    def get_repository_type(self):
        pass

    def insert(self, model):
        result = self.repository.insert(model)
        return result

    def insert_many(self, model):
        result = self.repository.insert_many(model)
        return result

    def update(self, model):
        result = self.repository.update(model)
        return result

    def delete(self, model):
        result = self.repository.delete(model)
        return result

    def query_by_id(self, identifier):
        result = self.repository.query_by_id(identifier)
        return result

    def query_all(self, page, size):
        result = self.repository.query_all(page=page, size=size)
        return result

    def query_num_records(self, *args, **kwargs):
        result = self.repository.query_num_records(*args, **kwargs)
        return result

    def get_entity_type(self):
        result = self.repository.get_entity_type()
        return result
