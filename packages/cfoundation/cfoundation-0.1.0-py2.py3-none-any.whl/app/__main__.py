from cement.core.foundation import CementApp
from config import NAME, BANNER
from controllers import (
    BaseController,
    CleanController
)
from cfoundation import register

class App(CementApp):
    class Meta:
        label = NAME
        base_controller = BaseController
        handlers = [
            CleanController
        ]

def main():
    with App() as app:
        register(app)
        app.run()

if __name__ == '__main__':
    main()
