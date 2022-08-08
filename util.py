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

def make_http_request(url:str,method:str,headers:Dict[str,str],body:Dict[str,Any]|bytes|None=None)->Dict[str,Any]:
    if type(body) == dict:
        body = bytes(json.dumps(body,indent=4),"utf-8")

    request = urllib.request.Request(url=url,data=body,method=method,headers=headers)

    if body and not request.has_header('Content-Type'):
        request.add_header("Content-Type","application/json")

    request.add_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0")
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

class AuthenticatedHTTPRequestManager:
    def __init__(self,token:Dict[str,str],refresh_func:Callable[[str],Dict[str,str]]):
        self.generator = token_generator(token,refresh_func)

    @log_time    
    def __call__(self,*args,**kwargs):
        headers=None
        if len(args)>=3:
            headers = args[2]
        elif 'headers' in kwargs:
            headers=kwargs['headers']
        else:
            headers = {}
            kwargs['headers']=headers
        
        headers['Authorization'] = "Bearer {}".format(next(self.generator))
        try:
            return make_http_request(*args,**kwargs)
        except urllib.error.HTTPError as e:
            print(e.status,e.reason)
            if e.status == 401:
                print("refreshing token\n\n")
                headers['Authorization'] = "Bearer {}".format(next(self.generator))
                return make_http_request(*args,**kwargs)



