from http import HTTPStatus


class Response:
    """Response class used by the http api"""

    def __init__(self, code=None, results=None, messages=None,
                 status=None, auth_token=None):
        self.code = code
        self.results = results or dict()
        self.messages = messages or list()
        self.status = status
        self.auth_token = auth_token

        if code:
            self.status_code = code

    def add_message(self, message):
        self.messages.append(message)

    def update_results(self, results):
        self.results.update(results)


    @property
    def status_code(self):
        return self.code

    @status_code.setter
    def status_code(self, code):
        self._obj = HTTPStatus(code)
        self.code = self._obj.value
        self.add_message(self._obj.description)

        if code < 400:
            self.status = "success"
        else:
            self.status = "error"



    def to_dict(self):
        """
        Get a dictionary from the objects attributes without private keys.
        """
        _dict = vars(self)
        return {k: _dict[k] for k in _dict if not k.startswith('_')}


    def __call__(self):
        return self.to_dict(), self.code

