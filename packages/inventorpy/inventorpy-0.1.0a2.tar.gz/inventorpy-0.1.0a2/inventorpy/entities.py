from datetime import datetime
from uuid import uuid4
import bcrypt


class Entity:

    def __init__(self, uuid=None):
        self.uuid = uuid or str(uuid4())
        self.entity_class = self.__class__.__name__

    def to_dict(self):
        """
        Get a dictionary from the objects attributes without private keys.
        """
        _dict = vars(self)
        return {k: _dict[k] for k in _dict if not k.startswith('_')}

    @classmethod
    def from_dict(cls, dictionary):
        """
        Create an instance of a class from a given dictionary.
        """
        return cls(**dictionary)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uuid == other.uuid
        return False

    def __repr__(self):
        class_name = self.__class__.__name__
        params = ', '.join(f'{k}={v}' for k, v in self.to_dict().items())
        return (f'{class_name}('
                f'{params})')

class User(Entity):
    entity_class = 'User'

    def __init__(self, first_name, last_name, email, password, uuid=None):
        super().__init__(uuid)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._hashed_password = bcrypt.hashpw(
            password.encode('utf8'), bcrypt.gensalt(10))

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self._hashed_password)




class Job(Entity):
    entity_class = 'Job'
    ts = datetime.now().isoformat()
    def __init__(self, job_id=None, status=None, created_on=None,
                 location=None, description=None, notes=None,
                 created_by=None, items_used=None, uuid=None):
        super().__init__(uuid)
        self.job_id = job_id
        self.status = status
        self.created_on = created_on or self.ts
        self.created_by = created_by
        self.location = location
        self.description = description
        self.notes = notes
        self.items_used = items_used or list()

    def add_item(self, item):
        if not isinstance(item, Item):
            raise ValueError('item must be Item instance')
        self.items_used.append(item)


class Item(Entity):
    entity_class = 'Item'
    def __init__(self, name, part_number=None, description=None,
                 minimum_quantity=0, quantity=0, uuid=None):
        super().__init__(uuid)
        self.name = name
        self.description = description
        self.part_number = part_number
        self.minimum_quantity = minimum_quantity
        self.quantity = quantity


class ItemTransaction(Entity):
    entity_class = 'ItemTransaction'
    ts = datetime.now().isoformat()

    def __init__(self, item_uuid, item_name, quantity,
                 reference_number=None, reference_uuid=None,
                 user_uuid=None, user_name=None,
                 timestamp=None, uuid=None):
        super().__init__(uuid)
        self.item_uuid = item_uuid
        self.item_name = item_name
        self.timestamp = timestamp or self.ts
        self.quantity = quantity
        self.reference_number = reference_number
        self.reference_uuid = reference_uuid
        self.user_uuid = user_uuid
        self.user_name = user_name

