#!/usr/bin/env python3 

import sys,time
sys.path.append('..')
import requests,json
from botocore.exceptions import ClientError
from game.config.config import Config

cfg = Config()

class Account():
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.account_endpoint = cfg.ACCOUNT_SERVER
        self.game_server_endpoint = f'{cfg.GAME_SERVER_ENDPOINT}:{cfg.LOGIN_PORT}'

    def _post_request(self, server, endpoint, data):
        url = server + '/' + endpoint 
        return requests.post(url, data=json.dumps(data), headers=self.headers)
    
    def _get_request(self, server, endpoint, data):
        url = server + '/' + endpoint 
        return requests.get(url, data=json.dumps(data), headers=self.headers)
    
    def _delete_request(self, server, endpoint, data):
        url = server + '/' + endpoint 
        return requests.delete(url, data=json.dumps(data), headers=self.headers)
        
    def create_account(self):
        payload = {}
        payload['username'] = input('Enter your account name: ')
        payload['password'] = input('Enter your new password: ')
        payload['email'] = input('Enter your email: ')
        
        try:
            res = self._post_request(self.account_endpoint, 'account/create', payload)
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
            res = self._post_request(self.account_endpoint, 'account/confirm', payload)
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
            res = self._post_request(self.account_endpoint, 'account/request-token', payload)
            if res.status_code == 200:
                tokens = res.json()
                id_token = tokens['IdToken']
                print(f"\nToken successfully retrieved.")
                return id_token, res.status_code
            else:
                print(f"Get request_token failed with response code: {res.status_code}")
                return res.json(), res.status_code
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred while requesting token: {e}")

    def get_characters(self, payload):
        # need to sleep to workaround IAT error (token issued in future error)
        time.sleep(3)
        my_characters = None
        try:
            res = self._get_request('http://' + self.game_server_endpoint, 'game/character', payload)
            if res.status_code == 200 and res != None:
                characters = res.json()
                my_characters = characters['name']
            elif res.status_code == 404:
                print(f"No characters found for this account.")
                my_characters = False
            else:
                print()
                print("Something went wrong getting characters.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        finally:
            return my_characters

    def create_character(self, new_char_name, token):
        try: 
            payload = {}
            payload['NewCharName'] = new_char_name
            if token is None:
                print("Requesting new token.")
                token_res, res_code = self.request_token()
                if res_code == 200:
                    payload['IdToken'] = token_res
                else: 
                    print(f"Character creation failed. Unable to get auth token due to {res_code} error.")
            else:
                payload['IdToken'] = token
            char_res = self._post_request('http://' + self.game_server_endpoint, 'game/character', payload)
            if char_res.status_code == 200:
                return char_res.json()['name'][0], None   
            else:
                char_res_dict = char_res.json()
                return char_res.json()['name'][0], char_res_dict.get('error')
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred during character creation: {e}")

    def delete_character(self, char_name, token):
        try: 
            payload = {}
            payload['CharName'] = char_name
            if token is None:
                print("Requesting new token.")
                token_res, res_code = self.request_token()
                if res_code == 200:
                    payload['IdToken'] = token_res
                else: 
                    print(f"Character deletion failed. Unable to get auth token due to {res_code} error.")
            else:
                payload['IdToken'] = token
                # extra token validation disabled
            # is successful, this returns new list of all account characters after character was deleted
            try:
                del_char_res = self._delete_request('http://' + self.game_server_endpoint, 'game/character', payload)
            except Exception as e:
                print(f"Error deleting character: {e}")
            if del_char_res.status_code == 200:
                return del_char_res.json()
            else:
                print()
                print(f"Something went wrong deleting character {char_name}")
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred during character creation: \n{e}")

    def login(self):
        my_characters = None
        token = None
        try:
            token_res, res_code = self.request_token()
            if res_code == 200:
                payload = {}
                payload['IdToken'] = token_res
                token = token_res
                #print("Token validity check disabled.")
                # res = self._post_request(self.account_endpoint, 'account/login', payload)
                my_characters = self.get_characters(payload)
            else: 
                print(f"Login failed with response code: {res_code}")
        except ClientError as e:
            print("Boto client error:")
            print(e.response())
        except Exception as e:
            print(f"Unexpected error occurred: \n{e}")
        return my_characters, token

    def check_account_exists(self):
        pass

    def reset_password(self):
        pass
