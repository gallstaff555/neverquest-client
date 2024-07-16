#!/usr/bin/env python3 

import sys
from account import Account

def main_menu():
    user_account = Account()
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    choice = input("Select an option: ")
    if choice == "1":
        user_login(user_account)
    if choice == "2":
        user_create_account(user_account)
    if choice == "3":
        print("Goodbye!")
        sys.exit()
    else: 
        print(f"\nSelect a valid option.")
        main_menu()

def user_login(user_account):
    my_characters = user_account.login()
    if my_characters != None:
        print(f"Characters: {my_characters[0]}")
        sys.exit()
    # TODO create new character if none exist
    else:
        print("Something went wrong logging in. Unable to retrieve your character list.")
    

def user_create_account(user_account):
    user_account.create_account()

def main():
    print("Welcome to Neverquest!")
    main_menu()

if __name__ == "__main__":
    main()
    
    

    