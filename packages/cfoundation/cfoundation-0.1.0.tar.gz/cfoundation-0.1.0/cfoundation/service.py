from util import get_app
from pydash import _

class Service():
    def register(self):
        self.app = get_app()
