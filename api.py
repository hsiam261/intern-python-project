import util
from typing import Dict,Any
import urllib.parse

PROTOCOL = "HTTP"
HOST_NAME = "intern-test-server.herokuapp.com"

def login(username:str,password:str)->Dict[str,Any]:
    endpoint = "/api/auth"
    method = "POST"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    body = {"username":username,"password":password}
    return util.make_http_request(url,method,{},body)['body']

def refresh_token(refresh_token:str)->Dict[str,str]:
    endpoint = "/api/auth/token"
    method = "POST"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    body = {"refresh_token":refresh_token}

    return util.make_http_request(url,method,{},body)['body']


def get_tweets(request_manager:util.AuthenticatedHTTPRequestManager)->Dict[str,str]:
    endpoint = "/api/tweets"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    return request_manager.get(url,{})['body']

def create_tweets(request_manager:util.AuthenticatedHTTPRequestManager,text:str)->Dict[str,str]:
    endpoint = "/api/tweets"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    body = {"text":text}

    return request_manager.post(url,{},body)['body']


