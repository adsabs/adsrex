import requests
import copy
import logging
from . import config


class BaseUser(object):

    def __init__(self, base_url, cookie=None, access_token=None):
        self.base_url = base_url
        self.cookie = cookie
        self.access_token = access_token
    
    def get(self, *args, **kwargs):
        return requests.get(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def post(self, *args, **kwargs):
        return requests.post(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def put(self, *args, **kwargs):
        return requests.put(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def options(self, *args, **kwargs):
        return requests.options(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def head(self, *args, **kwargs):
        return requests.head(*self.update_args(args), **self.update_kwargs(kwargs))
    
    def update_args(self, args):
        args = list(args)
        if len(args) > 0:
            url = args[0]
            if not (url[0:4] == 'http' or url[0:2] == '//'):
                url = self.base_url + (url[0] == '/' and url or ('/' + url))
            args[0] = url
        return args
    
    def update_kwargs(self, kwargs):
        if 'headers' in kwargs:
            headers = kwargs['headers']
        else:
            headers = {}
            
        if hasattr(self, 'access_token') and self.access_token:
            headers['Authorization'] = headers.get('Authorization', 'Bearer:' + self.access_token)
        
        if headers:
            kwargs['headers'] = headers
            
        if hasattr(self, 'cookie') and self.cookie:
            if not kwargs.get('cookies', None):
                kwargs['cookie'] = self.cookie
        kwargs.setdefault('allow_redirects', False)
        return kwargs
    
    def get_config(self, name):
        if hasattr(config, name):
            return copy.deepcopy(getattr(config, name))
        raise Exception('Non-existent config value: %s' % name)



            
anonymous_user_classic = BaseUser(config.CLASSIC_URL)
authenticated_user_classic = BaseUser(config.CLASSIC_URL, cookie=config.CLASSIC_COOKIE)
anonymous_user_bbb = BaseUser(config.BBB_URL)
authenticated_user_bbb = BaseUser(config.BBB_URL, cookie=config.BBB_COOKIE)
