#!/usr/bin/env python3 

import sys
from account import Account

def main_menu(user_account):
    
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
        main_menu(user_account)

def user_login(user_account):
    my_characters, token = user_account.login()
    if my_characters == False or my_characters != None:
        print("Login successful")
        character_menu(my_characters, user_account, token)
        sys.exit()
    else:
        print("Something went wrong logging in. Unable to retrieve your character list.")

def character_menu(character_list, user_account, token): 
    print(f"\nThis is the character menu!")
    print(f"1. Enter world with one of following characters: {character_list}")
    print("2. Create new character")
    print("3. Go back to main menu")
    print("4. Exit")
    choice = input("Select an option: ")
    if choice == "1":
        print("feature not implemented yet")
        sys.exit()
        # enter world
    if choice == "2":
        user_create_character(user_account, character_list, token)
    if choice == "3":
        main_menu(user_account)
    if choice == "4":
        print("Goodbye!")
        sys.exit()
    else: 
        print(f"\nSelect a valid option.")
        main_menu(user_account)

def user_create_account(user_account):
    user_account.create_account()

def user_create_character(user_account, character_list, token):
    new_char_name = input("Enter name: ")
    new_character_list = user_account.create_character(new_char_name, token)
    if new_character_list != None:
        print(f"New character {new_char_name} created successfully!")
        character_menu(new_character_list, user_account, token)
    else:
        character_menu(character_list, user_account, token)

def main():
    print("Welcome to Neverquest!")
    user_account = Account()
    main_menu(user_account)

if __name__ == "__main__":
    main()
    
    

    