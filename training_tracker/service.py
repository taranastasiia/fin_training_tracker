

class BaseService:
    def __init__(self, request=None):
        self._request = request
        self._user = request.user if request else None

