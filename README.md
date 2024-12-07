# TODO Debug Account Creation 

# python virtual env
python3 -m venv .venv
source .venv/bin/activate

# additional
deactivate
pip3 install -r requirements.txt

# Start authentication service
neverquest-authentication service must be running on port 8080
(hint: python3 authentication.py - run this from neverquest-authentication for local testing)

python3
from client.account import Account
a = Account()
a.create_account()


To login and get token:
a.login()

# TODO
handle server disconnects