# Debug Account Creation 

neverquest-authentication service must be running on port 8080

python3
from client.account import Account
a = Account()
a.create_account()


To login and get token:
a.login()