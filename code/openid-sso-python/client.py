import requests
from extras import print_json


class Client:
    def __init__(self, config):
        self.config = config
        self.auth_code = None
        self.id_token = None
        self.access_token = None

        hostname = config["issuer"]
        certfile = config['certfile']
        config_url = hostname + "/.well-known/openid-configuration"
        r = requests.get(config_url, verify=certfile)
        self.metadata = r.json()

    def get_token(self, auth_code):
        token_endpoint = self.metadata["token_endpoint"]
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:5000/callback',
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'code': auth_code
        }
        r2 = requests.post(token_endpoint, data=payload, headers=headers, verify=self.config['certfile'])
        return r2.json()
    
    def get_userinfo(self):
        userinfo_endpoint = self.metadata["userinfo_endpoint"]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        r = requests.get(userinfo_endpoint, headers=headers, verify=self.config['certfile'])
        return r.json()