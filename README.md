# TODO Debug Account Creation 

# python virtual env
python3 -m venv .venv
source .venv/bin/activate

# Start authentication service
neverquest-authentication service must be running on port 8080
(hint: python3 authentication.py - run this from neverquest-authentication for local testing)

python3
from client.account import Account
a = Account()
a.create_account()


To login and get token:
a.login()