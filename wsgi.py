# +++++++++++ DJANGO +++++++++++
# To use your own Django app use code like this:
import os
import sys

# assuming your Django settings file is at /home/NexusSphere/NexusSphere/config/settings.py
# and your manage.py is is at /home/NexusSphere/NexusSphere/manage.py
path = '/home/NexusSphere/NexusSphere'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
