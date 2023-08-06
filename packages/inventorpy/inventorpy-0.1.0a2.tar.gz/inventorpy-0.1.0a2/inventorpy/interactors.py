from inventorpy.entities import Item, User
import sys


class Response:
    def __init__(self, data=None):
        self.data = data
        self.errors = []

    @property
    def has_error(self):
        return len(self.errors) > 0


def _class_from_string_name(name):
    return getattr(sys.modules[__name__], name)


def _entity_factory(data):
    """Builds and returns an entity object from the 'entity_class
    key included in the given data dictionary"""
    data_copy = data.copy()
    class_name = data_copy.pop('entity_class')
    class_ = _class_from_string_name(class_name)
    return class_(**data_copy)


def _build_response(data=None, errors=None):
    response = Response()
    response.data = data
    if errors:
        response.errors.extend(errors)
    return response


def create_or_update(storage, data):
    return_data = {}
    errors = list()

    try:
        new_entity = _entity_factory(data)
        entity = storage.create(new_entity)

    except ValueError:
        entity = storage.update(data)

    except Exception as e:
        errors.append(str(e))

    if not errors:
        return_data = entity.to_dict()

    return _build_response(data=return_data, errors=errors)


def query(storage, params):
    """Searches the database based on the given parameter dictionary
    """
    return_data = {}
    errors = []

    try:
        return_data = [obj.to_dict() for obj in storage.retrieve(**params)]
    except ValueError as e:
        errors.append(str(e))

    return _build_response(data=return_data, errors=errors)





