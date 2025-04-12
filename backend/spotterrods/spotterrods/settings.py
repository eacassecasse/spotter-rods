import os
from dotenv import load_dotenv
from . import ENV

environment = ENV.get('DRF_ENVIRONMENT', 'dev')

if environment == 'dev':
    from .settings_development import *
else:
    from .settings_production import *
