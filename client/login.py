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
        character_menu(my_characters[0], user_account, token)
        sys.exit()
    else:
        print("Something went wrong logging in. Unable to retrieve your character list.")

def character_menu(character_list, user_account, token): 
    print(f"\nThis is the character menu!")
    print(f"1. Enter world with one of following characters: {character_list}")
    print("2. Create new character")
    print("3. Go back to main menu")
    print("4. Delete character.")
    print("5. Exit")
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
        user_delete_character(character_list, user_account, token)
    if choice == "5":
        print("Goodbye!")
        sys.exit()
    else: 
        print(f"\nSelect a valid option.")
        main_menu(user_account)

def user_create_account(user_account):
    user_account.create_account()

def user_create_character(user_account, character_list, token):
    new_char_name = input("Enter name: ")
    new_character_list, error = user_account.create_character(new_char_name, token)
    if new_character_list != None and error == None:
        print(f"\nNew character {new_char_name} created successfully!")
        character_menu(new_character_list, user_account, token)
    else:
        print(f"\nCharacter name {new_char_name} already in use!") if 'Integrity' in error else print("Error creating character.")
        character_menu(character_list, user_account, token)

def user_delete_character(character_list, user_account, token):
    character_to_delete = input("Enter character name to delete: ")
    if character_to_delete not in character_list:
        print(f"Character named {character_to_delete} not found!")
        character_menu(character_list, user_account, token)
    else:
        print(f"Attempting to delete {character_to_delete}")
        updated_character_list= user_account.delete_character(character_to_delete, token)
        print(f"Updated list: {updated_character_list}")
        character_menu(updated_character_list, user_account, token)

def main():
    print("Welcome to Neverquest!")
    user_account = Account()
    main_menu(user_account)

if __name__ == "__main__":
    main()
    
    

    