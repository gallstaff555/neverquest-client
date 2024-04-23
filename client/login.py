#!/usr/bin/env python3 

import sys
from account import Account


def main():
    user_account = Account()

    print("Welcome to Neverquest!")
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    choice = input("Select an option:")
    if choice == "1":
        user_login(user_account)
    if choice == "2":
        user_create_account(user_account)
    if choice == "3":
        print("Goodbye!")
        sys.exit()

def user_login(user_account):
    user_account.login()

def user_create_account(user_account):
    user_account.create_account()

if __name__ == "__main__":
    main()
    
    

    