import os
import sys
from kivy.lang import Builder
from app.factory import create_app

Builder.load_file("kv/common_widgets.kv")

if __name__ == '__main__':
    app = create_app()
    app.run()