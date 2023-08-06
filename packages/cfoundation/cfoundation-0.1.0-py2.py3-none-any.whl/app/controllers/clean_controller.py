from cement.core.controller import expose
from cfoundation import Controller

class CleanController(Controller):
    class Meta:
        label = 'clean'
        description = 'Clean dotfiles'
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        return self.app.services.clean_service.clean()
