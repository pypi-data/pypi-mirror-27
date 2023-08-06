from inventorpy.storage import MemoryDB
from inventorpy import interactors


class Inventorpy:
    """Implementation of the Inventorpy API for use by the client
    """

    def __init__(self, storage=None, user_email=None):
        self.storage = storage or MemoryDB()
        self.user = None

        if user_email:
            self.set_user(user_email)

    def set_user(self, email):
        try:
            self.user = self.storage.retrieve(
                entity_class='User', email=email
            )[0]
        except IndexError:
            pass

    def create_or_update(self, data):
        r = interactors.create_or_update(
            storage=self.storage, data=data
        )
        return r

    def query(self, params):
        r = interactors.query(
            self.storage, params
        )
        return r



