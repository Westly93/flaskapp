import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskapp/")
sys.path.insert(0, '/var/www/flaskapp/venv/lib/python3.10/site-packages/')

from flaskapp import app as application
application.secret_key = 'Dzidzo@MSU2022'
application.debug= True