FEI_WS_USERNAME = ''
FEI_WS_PASSWORD = ''
FEI_WS_BASE_URL = 'https://data.fei.org/'

try:
    from django.conf import settings
    if hasattr(settings, 'FEI_BASE_URL'):
        FEI_WS_BASE_URL = settings.FEI_WS_BASE_URL
    if hasattr(settings, 'FEI_WS_USERNAME'):
        FEI_WS_USERNAME = settings.FEI_WS_USERNAME
    if hasattr(settings, 'FEI_WS_PASSWORD'):
        FEI_WS_PASSWORD = settings.FEI_WS_PASSWORD
except ImportError as e:
    print "Import error ", e.message

