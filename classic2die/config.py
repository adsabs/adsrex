
# The main endpoint including the version, ie. https://api.adsabs.harvard.edu/v1 
BBB_URL = 'https://dev.adsabs.harvard.edu'
CLASSIC_URL = 'http://legacy.adsabs.harvard.edu'

# e.g. access token to tester@ads (on staging)
AUTHENTICATED_USER_EMAIL = 'tester@ads'
AUTHENTICATED_USER_ACCESS_TOKEN = ''
AUTHENTICATED_USER_COOKIE = ''

BBB_COOKIE = ''
CLASSIC_COOKIE = ''

# Override config with local_config values
try:
    from . import local_config
    
    for x in dir(local_config):
        g = globals()
        if x.upper() == x and x in g:
            g[x] = getattr(local_config, x)
except:
    pass