import csv
import os

#  Hardcoded credentials
Users = {
    "PILOT": "FLYBOY",
    "GROUNDCREW": "WINGIT"
}

CSV_FILE = 'inventory.csv'

#  Create CSV with set headers if non-existant
def check_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            fieldnames = ['name', 'type', 'quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


#  Login Menu
def login_menu():
    while True:
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        if username in Users and Users[username] == password:
            print(f"Welcome {username}!")
            if username == "PILOT":
                pilot_menu()
            else:
                groundcrew_menu()
            break
        else:
            print("Invalid details. Please try again.\n")

#  Load CSV Inventory
def load_inventory():
    with open(CSV_FILE, mode='r', newline='') as file:
        return list(csv.DictReader(file))

#  Save CSV Inventory
def save_inventory(inventory):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['name', 'type', 'quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

#  Search Weapon (Available to both users)
def search_weapon(name):
    inventory = load_inventory()
    for item in inventory:
        if item['name'].lower() == name.lower():
            print(f"{item['name']} has {item['quantity']} units.")
            return
    print("Weapon not found.")

#  Fire! (Pilot Only)
def fire(name):
    inventory = load_inventory()
    for item in inventory:
        if item['name'].lower() == name.lower():
            if int(item['quantity']) > 0:
                item['quantity'] = str(int(item['quantity']) - 1)
                save_inventory(inventory)
                print(f"Fired one {item['name']}. Remaining: {item['quantity']}")
            else:
                print("Ammunition Empty!")
            return
    print("Weapon not found.")

#  Edit Weapon (Groundcrew Only)
def edit_weapon(name):
    inventory = load_inventory()
    for item in inventory:
        if item['name'].lower() == name.lower():
            # Fix to address Bug B3- Added a check to only allow numeric digits (positive and negative) to be inputted
            # and added a text prompt if anything else is tried.
            while True:
                change_input = input("Enter quantity to add or remove (use negative for removal): ")
                try:
                    change = int(change_input)
                    break
                except ValueError:
                    print("Invalid input. Please use a number")
            current_quantity = int(item['quantity'])
            new_quantity = current_quantity + change
            if new_quantity < 0:
                print(f"Can't remove {abs(change)} units. Only {current_quantity} available.")
                return
            item['quantity'] = str(max(0, int(item['quantity']) + change))
            save_inventory(inventory)
            print(f"{item['name']} updated to {item['quantity']} units.")
            return
    print("Weapon not found.")

#  Add New Weapon (Groundcrew Only)
def add_new_weapon():
    name = input("Enter weapon name: ")
    type_ = input("Enter weapon type: ")
    # Fix to address Bug B3- Added a check to only allow numeric digits (positive only) to be inputted
    # and added text prompts if anything else is tried.
    while True:
        quantity_input = input("Enter numeric quantity: ")
        try:
            quantity = int(quantity_input)
            if quantity < 0:
                print("Invalid input. Quantity cannot be negative")
                continue
            break
        except ValueError:
            print("Invalid input. Quantity must be a number")
    inventory = load_inventory()
    inventory.append({'name': name, 'type': type_, 'quantity': quantity})
    save_inventory(inventory)
    print(f"{name} added to inventory.")

#  Remove Weapon (Groundcrew Only)
def remove_weapon(name):
    inventory = load_inventory()
    new_inventory = [item for item in inventory if item['name'].lower() != name.lower()]
    if len(new_inventory) == len(inventory):
        print("Weapon not found.")
    else:
        save_inventory(new_inventory)
        print(f"{name} removed from inventory.")

#  Overall Report (Groundcrew Only)
def overall_report():
    inventory = load_inventory()
    if not inventory:
        print ("Inventory Empty.")   # Fix to address Bug B1- Overall Report is blank when a new CSV created.
        return
    print("\nInventory Report:")
    for item in inventory:
        print(f"{item['name']} ({item['type']}): {item['quantity']} units")

#  Pilot Menu
def pilot_menu():
    while True:
        print("\nPILOT MENU:")
        print("1. Search Weapon")
        print("2. Fire Weapon")
        print("3. Logout")
        choice = input("Choose an option: ")
        if choice == '1':
            search_weapon(input("Enter weapon name: "))
        elif choice == '2':
            fire(input("Enter weapon name: "))
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

#  Groundcrew Menu
def groundcrew_menu():
    while True:
        print("\nGROUNDCREW MENU:")
        print("1. Search Weapon")
        print("2. Edit Weapon")
        print("3. Add Weapon")
        print("4. Remove Weapon")
        print("5. Overall Report")
        print("6. Logout")
        choice = input("Choose an option: ")
        if choice == '1':
            search_weapon(input("Enter weapon name: "))
        elif choice == '2':
            edit_weapon(input("Enter weapon name: "))
        elif choice == '3':
            add_new_weapon()
        elif choice == '4':
            remove_weapon(input("Enter weapon name: "))
        elif choice == '5':
            overall_report()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

#  Start Program
if __name__ == "__main__":
    check_csv()
    login_menu()