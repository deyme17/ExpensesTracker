from kivy.app import App

def get_static_data_service():
    app = App.get_running_app()
    return getattr(app, "static_data_service", None)
