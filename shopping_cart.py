import datetime

user_accounts = {}
shopping_history = {}



def show_history():
    if shopping_history[current_user]:
        print(f'\nShopping history for {current_user}:')
        
        # Sort transactions by timestamp in descending order
        sorted_transactions = sorted(shopping_history[current_user], key=lambda x: x['timestamp'], reverse=True)
        
        # Initialize the previous final amount to None for the first iteration
        prev_final_amount = None

        for entry in sorted_transactions:
            current_final_amount = entry.get('final_amount', entry['total_amount'])

            # Print the entry only if the final amount is different from the previous one
            if current_final_amount != prev_final_amount:
                print()
                print(f"Timestamp: {entry['timestamp']}")
                print('Items:')
                for item in entry['items']:
                    print(f"{item['quantity']} {item['phone']} - ${item['item_amount']:.2f}")

            # Update the previous final amount for the next iteration
            prev_final_amount = current_final_amount
    else:
        print(f'\n{current_user} has no shopping history currently\n')

DISCOUNT = 0.10  # You can adjust this value based on your discount percentage


def save_data():
    with open('user_accounts.txt', 'w') as user_accounts_file:
        for username, account_info in user_accounts.items():
            user_accounts_file.write(f'{username}:{account_info["password"]}:{account_info["first_name"]}:{account_info["last_name"]}:{account_info["phone"]}\n')

    with open('shopping_history.txt', 'w+') as shopping_history_file:
        for username, transactions_list in shopping_history.items():
            for transaction in transactions_list:
                timestamp = transaction['timestamp']
                items = transaction['items']
                total_amount = transaction['total_amount']
                promo_code = transaction.get('promo_code', 'N/A')
                review = transaction.get('review', 'N/A')
                final_amount = transaction.get('final_amount', total_amount)

                # Convert items to a string for saving
                items_str = ', '.join([f"{{'phone': '{item['phone']}', 'quantity': {item['quantity']}, 'item_amount': {item['item_amount']}}}" for item in items])

                # Write the transaction details to the file
                shopping_history_file.write(f"{username};{{'timestamp': '{timestamp}', 'items': [{items_str}], 'total_amount': {total_amount}, 'promo_code': '{promo_code}', 'final_amount': {final_amount}, 'review': '{review}'}}\n")

def load_data():
    global user_accounts, shopping_history

    try:
        with open('user_accounts.txt', 'r') as user_accounts_file:
            lines = user_accounts_file.readlines()
            user_accounts = {}
            for line in lines:
                parts = line.split(':')
                if len(parts) == 5:
                    username, password, first_name, last_name, phone = parts
                    user_accounts[username] = {'password': password, 'first_name': first_name,
                                                'last_name': last_name,
                                                'phone': phone.strip()}
    except FileNotFoundError:
        pass

    try:
        with open('shopping_history.txt', 'r') as shopping_history_file:
            lines = shopping_history_file.readlines()
            shopping_history = {}
            for line in lines:
                parts = line.split(';')
                if len(parts) == 2:
                    username, transaction_str = parts[0], parts[1].strip()
                    transaction_dict = eval(transaction_str)
                    shopping_history.setdefault(username, []).append(transaction_dict)
    except FileNotFoundError:
        pass
load_data()

print('\t\t\U0001F30CWelcome to ZAF\n\tGood service is our utmost priority!\U0001F30C\n\t')


def create_account():
    global user_accounts, shopping_history
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()
    first_name = input('Enter your first name: ').strip()
    last_name = input('Enter your last name: ').strip()
    while True:
        phone_number = input('Enter your phone number: ').strip()
        if len(phone_number)==11:
            break
        else:
            print()
            print('Phone number must be of 11 digits with no characters ')
            print()
    if username in user_accounts:
        print()
        print('Username already exists, please choose a different one ')
        print()
    else:
        user_accounts[username] = {'password': password, 'first_name': first_name, 'last_name': last_name,
                                   'phone': phone_number}
        shopping_history.setdefault(username, [])  # Initialize an empty list for shopping history if not exists
        save_data()  # Save the entire dictionary to the file
        print()
        print('Account created successfully!')
        print()

def login():
        username = input('Enter username: ').strip()
        password = input('Enter password: ').strip()
        if username in user_accounts:
            if user_accounts[username]["password"] == password:
                print(f'\nLogin successful, Welcome {username}!')
                print("\nToday's promo code is 'cis'\n")
                
                shopping_history.setdefault(username, [])
                return username
            else:
                print()
                print("Invalid password!")
                print()
                return None

        else:
            print()
            print("Account does not exist!")
            print()
            return None







while True:
    print('\t\033[4m Welcome to Login Page\033[0m\n')  # used this for underlining
    print('\t1. Create account\n\t2. Login into an existing account')  # Aligned the options
    choice = input('\tEnter choice number (1 or 2): ')
    if choice == '1':
        create_account()
    elif choice == '2':
        current_user = login()
        if current_user:
            break  # Exit the loop if login is successful
    else:
        print('\nInvalid choice!')

print(
    '\n==================================================\nAVAILABLE PHONES\n==================================================')


phones = {'ZAF Fusion X': 1000, 'ZAF Odyssey Ultra': 799, 'ZAF Odyssey': 749, 'ZAF Nexus Pro': 599, 'ZAF Nexus': 549,
          'ZAF Horizon Elite': 499, 'ZAF Horizon': 399,'ZAF Galaxy Z':349,'ZAF Xperia':300,'ZAF Lynx':200}
cart = {}


def display_phones():
    print(f"{'Name':<26} | {'Price':<15}")
    print('----------------------------------------')
    count = 1
    for phone, price in phones.items():
        if count == 10:
            print(f'{count} - {phone:<23} | ${price:<10}')
            count+=1
        else:
            print(f'{count}  - {phone:<23} | ${price:<10}')
            count+=1

    # for phone, price in phones.items():
    #     print(f'{count}- {phone:<23} | ${price:<10}')
    #     count += 1


def remove_cart():
    global cart

    phone_lst = ['ZAF Fusion X', 'ZAF Odyssey Ultra', 'ZAF Odyssey', 'ZAF Nexus Pro', 'ZAF Nexus',
                 'ZAF Horizon Elite', 'ZAF Horizon','ZAF Galaxy Z','ZAF Xperia','ZAF Lynx']
    index = ["1", "2", "3", "4", "5", "6", "7","8","9","10","1.0","2.0","3.0","4.0","5.0","6.0","7.0","8.0","9.0","10.0"]
    # print('\n==================================================\nAvailable Options\n==================================================')

    while True:
        print(
            '\n==================================================\nYour Cart\n==================================================')  # Added dashes before cart display
        for idx, (phone, quantity) in enumerate(cart.items(), start=1):
            # For the index of the phone in phone_lst
            serial_number = phone_lst.index(phone) + 1

            print(f'{idx}. {quantity} {phone} (Serial Number: {serial_number})')

        rem_choice = input(
            '* Enter the serial number(1,2,3..) of the phone you wish to remove\n'
            '* Type "del" to empty your cart\n'
            '* Type "e" to exit remove cart \nYour choice: ').strip()

        if rem_choice == "e":
            break
        if rem_choice.lower() == "del":
            print("\n* Your cart is now empty")
            cart = {}
            break
        elif rem_choice in index:
            selected_phone = phone_lst[int(rem_choice) - 1]
            if selected_phone in cart:
                qnty = input(f'\nEnter the number of {selected_phone} you want to remove: ')
                if qnty.isalnum():
                    if qnty.isalpha():
                        print("\nEnter an integer!")
                    else:
                        qnty=float(qnty)
                        qnty=int(qnty)
                        if qnty > cart[selected_phone]:
                            print("\nYou can't remove more than what you have")
                        else:
                            cart[selected_phone] -= qnty
                            print(f'{qnty} {selected_phone} removed from cart')
                            view = input(
                                "Do you want to view your cart?\n* Type 'y' to view your cart\n* Type 'n' to continue shopping: ")
                            if view.lower() == "y":
                                view_cart()
                else:
                    print("\nEnter an integer!")
            else:
                print(f"\nYou don't have {selected_phone} in your cart")
        else:
            print("\nInvalid choice !")

        exit_choice = input("\nDo you want to exit remove cart? (y/n): ").lower()
        if exit_choice == "y":
            break


def view_cart():
    global user_accounts, shopping_history, current_user

    if current_user not in shopping_history:
        shopping_history[current_user] = []  # Initialize an empty list for shopping history if not exists

    print(f"{'Items':<30} | {'Quantity':<10} | {' Amount ($)'}")
    print('-' * 65)

    total_amount = 0  # Initialize total amount
    items_in_cart = []

    for phone, quantity in cart.items():
        if quantity > 0:
            item_amount = quantity * phones[phone]
            print(f'{phone:<30} | {quantity:<10} | ${item_amount}')
            total_amount += item_amount
            items_in_cart.append({'phone': phone, 'quantity': quantity, 'item_amount': item_amount})

    if total_amount > 0:
        # Append the current cart to the user's shopping history with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shopping_history[current_user].append({'timestamp': timestamp, 'items': items_in_cart, 'total_amount': total_amount})
        print(f'Total Amount: ${total_amount}')
    else:
        print('Your cart is empty.')

def add_to_cart():
    display_phones()
    global rem_in
    while True:
        phone_lst = ['ZAF Fusion X', 'ZAF Odyssey Ultra', 'ZAF Odyssey', 'ZAF Nexus Pro', 'ZAF Nexus',
                     'ZAF Horizon Elite', 'ZAF Horizon','ZAF Galaxy Z','ZAF Xperia','ZAF Lynx']
        print(
            '\n==================================================\nAVAILABLE OPTIONS\n==================================================')

        serial_num = input(
            '* Enter the serial number (1,2,3..) of the phone you want to buy:\n'
            '* Enter "view" to view your cart:\n'
            '* Enter "rem" to remove item from your cart\n'
            '* Enter "done" to checkout\n'
            '* Enter "history" to view past shopping history\nYour choice: ').strip()
        index = ["1", "2", "3", "4", "5", "6", "7","8","9","10","1.0","2.0","3.0","4.0","5.0","6.0","7.0","8.0","9.0","10.0"]
        if serial_num.lower() == "rem":
            if cart:
                remove_cart()
            else:
                print("Your cart is empty! :(")
        elif serial_num.lower() == 'history' :
            show_history()
        elif serial_num.lower() == 'done':
            break

        elif serial_num.lower() == "view":
            view_cart()
        elif serial_num in index:
            selected_phone = phone_lst[int(serial_num) - 1]

            if selected_phone in phones:

                quantity = input(f'Enter quantity for {selected_phone}: ')
                if quantity.isalnum():
                    if quantity.isalpha() or quantity == "0":
                        print("\nEnter a natural number! :) ")
                    else:
                        quantity=int(quantity)
                        cart[selected_phone] = cart.get(selected_phone, 0) + quantity
                        print(f'\n{quantity} {selected_phone}(s) added to your cart')

                else:
                    print("\nEnter an integer!")

            else:
                print('\nInvalid phone, please try again!')
        else:
            print("\ninvalid choice!")

add_to_cart()




view_cart()

# Print the total amount spent on all transactions for the current user
total_amount_all_transactions = sum(
    transaction.get("total_amount", 0) for transaction in shopping_history[current_user])

# Print only the shopping history of the last transaction for the current user
if shopping_history[current_user]:
    last_transaction = shopping_history[current_user][-1]
else:
    last_transaction = {'timestamp': 'N/A', 'items': [], 'total_amount': 'N/A'}

# After printing total amount, make it a variable
total_amount = last_transaction.get("total_amount", "N/A")
# print(f'Total Amount: ${total_amount}\n')

# Ask the user if they have a promo code
promo_code = input("Do you have a promo code? Enter it here (or press Enter to skip): ").strip()

# Check if the promo code is valid
if promo_code.lower() == "cis":
    discount = 0.10  # 10% discount for the promo code "cis"
    discounted_amount = total_amount * (1 - discount)
    saved_amount = total_amount - discounted_amount  # Calculate the amount saved
    print(f'10% Discount applied! You saved: ${saved_amount:.2f}')
    print(f'Total Amount after discount: ${discounted_amount: .2f}')
    total_amount = discounted_amount

# Append the promo code information to the last transaction in shopping history
last_transaction['promo_code'] = promo_code
last_transaction['discounted_amount'] = total_amount



if shopping_history[current_user]:
    last_transaction = shopping_history[current_user][-1]

# After printing total amount, make it a variable
initial_amount = last_transaction.get("total_amount", "N/A")
discounted_amount = last_transaction.get("discounted_amount", "N/A")
saved_amount = initial_amount - discounted_amount if initial_amount != "N/A" and discounted_amount != "N/A" else "N/A"

# Print the shopping history for the current user
print(f'\nShopping history for {current_user} (Last Transaction):')
print(f"Timestamp: {last_transaction['timestamp']}")
print('Items:')
for item in last_transaction['items']:
    print(f"{item['quantity']} {item['phone']} - ${item['item_amount']:.2f}")
print(f'Initial Amount: ${initial_amount}')
print(f'Discounted Amount: ${discounted_amount}')
# print(f'Saved Amount: ${saved_amount}' if saved_amount != "N/A" else "Saved Amount: N/A")
print()  # for aesthetic purposes
review_choice = input('Do you want to leave a review on our products (y/n): ')
if review_choice == 'y'or review_choice == 'Y':
    review = input('Your Review: ')
    last_transaction['review'] = review
    print('\n\t Hope you Liked our shopping marvel :)')
else:
    print('\n\t Hope you Liked our shopping marvel :)')
# Save data before exiting the program
save_data()