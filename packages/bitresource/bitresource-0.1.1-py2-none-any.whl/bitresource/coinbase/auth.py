# coding: utf-8
import hashlib
import hmac
import time

from requests.auth import AuthBase
from requests.utils import to_native_string


class HMACAuth(AuthBase):
    def __init__(self, **kwargs):
        self.api_key = kwargs.get('api_key')
        self.api_secret = kwargs.get('api_secret')
        self.api_version = kwargs.get('api_version')

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        secret = self.api_secret

        if not isinstance(message, bytes):
            message = message.encode()
        if not isinstance(secret, bytes):
            secret = secret.encode()

        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        request.headers.update({
            to_native_string('CB-VERSION'): self.api_version,
            to_native_string('CB-ACCESS-KEY'): self.api_key,
            to_native_string('CB-ACCESS-SIGN'): signature,
            to_native_string('CB-ACCESS-TIMESTAMP'): timestamp,
        })
        return request
