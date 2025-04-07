import os
from dotenv import load_dotenv
from . import ENV

environment = ENV.get('DRF_ENVIRONMENT', 'dev')

if environment == 'dev':
    print("Development Server")
    from .settings_development import *
else:
    print("Production Server")
    from .settings_production import *
