from cement.core.controller import expose
from cfoundation import Controller

class BaseController(Controller):
    class Meta:
        label = 'base'
        description = 'A foundation made with cement'

    @expose(hide=True)
    def default(self):
        return
