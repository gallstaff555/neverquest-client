#!/usr/bin/env python3 

import sys
sys.path.append('..')
import requests,json
from botocore.exceptions import ClientError
from game.config.config import Config

cfg = Config()

class Account():
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.account_endpoint = f'http://{cfg.ACCOUNT_SERVER}:{cfg.ACCOUNT_PORT}'

    def _post_request(self, endpoint, data):
        url = self.account_endpoint + '/' + endpoint 
        return requests.post(url, data=json.dumps(data), headers=self.headers)
        
    def create_account(self):
        payload = {}
        payload['username'] = input('Enter your account name: ')
        payload['password'] = input('Enter your new password: ')
        payload['email'] = input('Enter your email: ')
        
        try:
            res = self._post_request('create_account', payload)
            print(res.status_code)
            if (res.status_code == 200 or res.status_code == 201):
                self.verify_account(payload)
            else: 
                print("Something went wrong.")
                print(res.text)
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred: \n{e}")

    def verify_account(self, payload):
        payload['confirmation_code'] = input(f'Enter your confirmation code sent to {payload.get("email")}: ')
        
        try:
            res = self._post_request('confirm_account', payload)
            print(res.status_code)
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred: \n{e}")

    def request_token(self):
        payload = {}
        payload['username'] = input('Enter your account name: ')
        payload['password'] = input('Enter your password: ')
        try:
            res = self._post_request('request_token', payload)
            if res.status_code == 200:
                tokens = res.json()
                print(res.status_code)
                id_token = tokens['IdToken']
                #print(f'id_token: {id_token}')
                print("Token successfully retrieved.")
                return id_token, res.status_code
            else:
                return res.json(), res.status_code
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


    def login(self):

        try:
            res, res_code = self.request_token()
            if res_code == 200:
                payload = {}
                payload['IdToken'] = res
                # This tests if Cognito ID token is valid 
                res = self._post_request('login', payload)
                print("ID token is valid. Login successful.")
            else: 
                print(res)
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred: \n{e}")

    def check_account_exists(self):
        pass

    def reset_password(self):
        pass
