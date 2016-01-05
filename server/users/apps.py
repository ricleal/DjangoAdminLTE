from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'server.users'

    def ready(self):
        import server.users.signals