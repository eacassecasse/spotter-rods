import os

if 'DJANGO_SETTINGS' in os.environ:
    if os.environ['DJANGO_SETTINGS'] == 'dev':
        print("Development Server")
        from .settings_development import *
    else:
        print("Production Server")
        from .settings_production import *
