"""
Authors: Asher Kassinove, Ben Dickerman, Leonardo Cruz
Date: 04-12-2023

Description: StockTracker application that allows user to track, add, edit, delete 
stock watchlists. 
"""

import os
import pandas_datareader as pdr 
import sys
from time import sleep, time 


def display_menu():
    print("""
StockTracker Menu:
1. Track watchlist
2. Add watchlist 
3. Edit watchlist 
4. Delete watchlist
5. Exit
    """)

def read_directory():
    """
    Read Watchlist Directory
    If no directory exists create directory 
    Else return files in directory if anys
    """
    if not os.path.exists("watchlists"):
        print("\nNo saved watchlists")
        os.mkdir("watchlists")
    else:
        files = sorted(os.listdir("watchlists"))
        if not files:
            print("\nNo available watchlists")
        else:
            print("Available watchlists:")
            print("-" * 21)
            for number, name in enumerate(files, 1):
                if name.endswith('watchlist'):
                    name = name.replace('.watchlist', '')
                    print(f"{number} - {name}")
            return files

def read_list(prompt, option = "open"):
    """
    Read Watchlist File
    Parameters: 
        prompt - str: Pass in different prompts for different scenarios
        option - str: Keyword to control for return based on what is needed 
    """
    watchlists = read_directory()
    if watchlists:
        choice = int(input(f"{prompt}"))
        chosen_file = watchlists[choice - 1]
        if option == "name":
            return chosen_file
        elif option == "edit":
            return chosen_file, open(f"watchlists/{chosen_file}", "r").read().split(",")
        else:
            return open(f"watchlists/{chosen_file}", "r").read().split(",")
    else:
        return print("Select add a list from the menu...")

def track(watchlist):
    """Track Watchlist"""
    start_time = time()
    prompt = ''
    while True:
        for symbol in watchlist:
            try:
                print(f'{symbol:8}{pdr.get_quote_yahoo(symbol)["price"].values[0]}')
            except:
                print(f"{symbol} not found")
        sleep(1)
        if time() - start_time >= 10:
            start_time = time()
            prompt = input("To continue press enter, any key to quit ")
            if prompt.isalpha():
                break

def add_list():
    symbols = []
    print("\nEnter stock symbols then press enter to continue: ")
    
    while True: 
        symbols_prompt = input("Please enter a stock symbol: ").upper()

        if symbols_prompt != "":
            symbols.append(symbols_prompt)
        else:
            break

    while True:
        watchlist_name_input = input("\nWhat would you like to name your watchlist: ")
        watchlist_path = watchlist_name_input + ".watchlist"

        if watchlist_path in os.listdir("watchlists"): 
            print("\nPlease enter a watchlist name that you haven't already used")
        else:
            print("\nWatchlist added!")
            break

    with open(f"watchlists/{watchlist_path}", "w") as file:
        file.write(",".join(symbols))

def edit_list():
    watchlist_name, chosen_watchlist = read_list("\nEnter list to edit: ", "edit")

    while True:
        add_or_delete_symbol = input("Would you like to add or delete symbols: ").lower()

        if add_or_delete_symbol == "a":
            add_symbol = input("Enter symbol to add to watchlist: ").upper()

            if add_symbol != "":
                chosen_watchlist.append(add_symbol)
                with open(f"watchlists/{watchlist_name}", "w") as file:
                    file.write(",".join(chosen_watchlist))
        elif add_or_delete_symbol == "d":
            print("Available Symbols:")
            print("-" * 21)
            for num, symbol in enumerate(chosen_watchlist, 1):
                print(f"{num} - {symbol}")
            
            choice = int(input("Enter symbol to delete: "))
            chosen_symbol = chosen_watchlist[choice - 1]
            chosen_watchlist.remove(chosen_symbol)
            with open(f"watchlists/{watchlist_name}", "w") as file:
                    file.write(",".join(chosen_watchlist))
        else:
            break

def delete_list():
    while True: 
        chosen_file = read_list("Enter list to delete: ", "name")
        watchlist_name = chosen_file.replace(".watchlist", "")
        check_deletion = input(f"Are you sure you would like to delete the watchlist - {watchlist_name}: ").lower()
        
        if check_deletion == "y":
            os.remove(f"watchlists/{chosen_file}")
            print(f"\n{watchlist_name} watchlist succesfully deleted")
            break
        else:
            print("\nWatchlist not deleted.\n")
            continue

options = {
    "1" : track,
    "2" : add_list,
    "3" : edit_list,
    "4" : delete_list,
}

def main():
    while True: 
        display_menu()
        choice = input("Enter your selection: ")

        if choice == "1":
            watchlist = read_list("Enter list to track: ")
            if watchlist:
                options[choice](watchlist)

        elif choice in "234":
            options[choice]()

        elif choice == "5":
            print("Goodbye!")
            sleep(1)
            sys.exit()

        else: 
            print("\nEnter a valid selection")
            continue

if __name__ == "__main__":
    main()