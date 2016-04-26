ERROR_404_HELP = False

import os

# Secret authorization key
AUTHORIZATION_KEY = os.environ.get('AUTHORIZATION_KEY', 'secret_token')

# PostgreSQL parameters
POSTGRE_USERNAME = os.environ.get('POSTGRE_USERNAME', 'postgres')
POSTGRE_PASSWORD = os.environ.get('POSTGRE_PASSWORD', 'postgres')
POSTGRE_HOST = os.environ.get('POSTGRE_HOST', 'localhost')
POSTGRE_DATABASE = os.environ.get('POSTGRE_DATABASE', 'td-limpo')

SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s/%s" % (POSTGRE_USERNAME, POSTGRE_PASSWORD, POSTGRE_HOST, POSTGRE_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True