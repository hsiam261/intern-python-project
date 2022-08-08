import time
import json
import urllib.request 
import urllib.error 
from typing import Any, Callable, Dict

"""
TODO: Write whatever class or function you may need
but, don't use any third party library
feel free to make any changes in the given class and its methods' arguments or implementation as you see fit
"""

def make_http_request(url:str,method:str,headers:Dict[str,str],body:Dict[str,Any]|bytes|None=None,
        token:str|None=None)->Dict[str,Any]:
    if type(body) == dict:
        body = bytes(json.dumps(body,indent=4),"utf-8")

    request = urllib.request.Request(url=url,data=body,method=method,headers=headers)

    if body and not request.has_header('Content-Type'):
        request.add_header("Content-Type","application/json")
    
    if token:
        request.add_header("Authorization","Bearer {}".format(token))

    result = {}

    with urllib.request.urlopen(request) as response:
        result['body'] = json.loads(response.read().decode('utf-8'))
        result['code'] = response.status
    return result


def token_generator(token:Dict[str,str],refresh_func:Callable[[str],Dict[str,str]]):
    while True:
        yield token['access_token']
        
        try:
            token = refresh_func(token['refresh_token']) # type : ignore
            print(token['refresh_token'])
        except urllib.error.HTTPError as e:
            print(e.status,e.reason)
            print(e)
            raise StopIteration
        except Exception as e:
            print(e)
            raise StopIteration


def log_time(fn):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        ans=fn(*args,**kwargs)
        end_time = time.time()
        print("elapsed time : ",end_time-start_time)
        return ans
    return wrapper



def _get_args_dict(fn,*args,**kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}

def refresh_and_try_again(fn):
    def wrapper(*args,**kwargs):
        args_dict = _get_args_dict(fn,*args,**kwargs)
        self = args_dict['self']

        try:
            return fn(*args,**kwargs)
        except urllib.error.HTTPError as e:
            print(e.status,e.reason)
            if e.status==401:
                print("Refreshing Token")
                self.token = next(self.generator)
                return fn(**args_dict)
    return wrapper


class AuthenticatedHTTPRequestManager:
    def __init__(self,token:Dict[str,str],refresh_func:Callable[[str],Dict[str,str]]):
        self.token = token
        self.generator = token_generator(token,refresh_func)

    
    
    @log_time
    @refresh_and_try_again
    def get(self,url:str,headers:Dict[str,str],body:Dict[str,Any]|bytes|None=None)->Dict[str,Any]:
        return make_http_request(url,"GET",headers,body,token=self.token)
    
    @log_time
    @refresh_and_try_again
    def post(self,url:str,headers:Dict[str,str],body:Dict[str,Any]|bytes|None=None)->Dict[str,Any]:
        return make_http_request(url,"POST",headers,body,token=self.token)



 

