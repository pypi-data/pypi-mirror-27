from collections import Set


class Database:
    pass


class MemoryDB(Database):
    def __init__(self, data=None):
        self._saved_data = data or dict()

    def create(self, obj):
        """
        Save the given object for persistence, if the object
        already exists with the primary key, raise exception.
        :param obj:
        """
        key = obj.entity_class
        self._saved_data.setdefault(key, list())

        if obj in self._saved_data[key]:
            raise ValueError("Object already exists")

        self._saved_data[key].append(obj)
        return obj

    def retrieve(self, **kwargs):
        """
        Finds and returns a collection of objects that match
        the given kwargs used as filters.
        kwargs must include 'entity_class'.
        """
        if 'entity_class' not in kwargs:
            raise ValueError('entity_class not provided in kwargs')

        key = kwargs.pop('entity_class')
        original = self._saved_data.get(key)
        if not original:
            return []

        if not kwargs:
            return original

        results = []
        for obj in original:
            obj_ok = True
            for k, v in kwargs.items():
                if getattr(obj, k) != v:
                    obj_ok = False
            if obj_ok:
                results.append(obj)

        return results

    def update(self, data):
        """Updates a given object
        raises an exception if the object is not found"""
        store = self._saved_data[data['entity_class']]
        for item in store:
            if item.uuid == data['uuid']:
                item.__dict__.update(data)
                return item





