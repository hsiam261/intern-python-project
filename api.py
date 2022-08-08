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


def get_tweets(token:Dict[str,str])->Dict[str,str]:
    endpoint = "/api/tweets"
    method = "GET"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    http_requestor = util.AuthenticatedHTTPRequestManager(token,refresh_token)
    return http_requestor(url,method,{})['body']

def create_tweets(token:Dict[str,str],text:str)->Dict[str,str]:
    endpoint = "/api/tweets"
    method = "POST"

    url = urllib.parse.urlunsplit((PROTOCOL,HOST_NAME,endpoint,'',''))

    body = {"text":text}

    http_requestor = util.AuthenticatedHTTPRequestManager(token,refresh_token)
    return http_requestor(url,method,{},body)['body']


