from cement.core.controller import CementBaseController
from util import get_app

class Controller(CementBaseController):
    def register(self):
        self.app = get_app()
