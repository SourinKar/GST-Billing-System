# Import pickle
import pickle
# Import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
# Import datetime
import datetime

# File name to store the users,passwords and product details
file_name = "users.pkl"
products_file = "products.pkl"

# Products and their values
products = {
    "apple": 50,
    "banana": 20,
    "orange": 30,
    "mango": 40,
    "pineapple": 50,
    "rice": 60,
    "wheat flour": 40,
    "sugar": 45,
    "salt": 20,
    "milk (1lt)": 50,
    "eggs(1dz)": 60,
    "butter": 120,
    "cheese": 120,
    "bread": 30,
    "tea": 150,
    "coffee": 200,
    "oil(1lt)": 120,
    "toy":30
}

# To save products into the file
def save_products(products):
    with open(products_file, "wb") as f:
        pickle.dump(products, f)

# Function to load values from the file
def load_products():
    try:
        with open(products_file, "rb") as f:
            return pickle.load(f)
    # If the file does not exist, returning the default products dictionary
    except FileNotFoundError:
        return products

# Function to add and modify items of the dictionary
def add_and_modify_items(items):
    while True:
        user_input = input("Enter a new item and its price (format: item:price) or type 'done' to finish: ")
        
        # Checking if the user wants to finish entering items
        if user_input.lower() == 'done':
            break

        item, price = user_input.split(":")
        
        # Converting the price string to a float
        price = float(price)
        
        # Checking if the item is already in the dictionary
        if item in items:
            # If the item exists, modify its price
            items[item] = price
        else:
            # If the item does not exist, add it to the dictionary
            items[item] = price

    # Saving the modified dictionary to a file
    save_products(items)
    return items

# Bill making
def get_user_input(prompt, input_type=str, error_message="Invalid input."):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print(error_message)

def calculate_price(quantity, price_per_unit, GST=0.18):
    price = round(price_per_unit * quantity, 2)
    gst = round(price * GST, 2)
    total = round(price + gst, 2)
    return price, gst, total

def get_product_details(products):
    product_name = get_user_input("Enter the product name: ").lower()
    while product_name not in products:
        print("Invalid product name. Please enter a valid product name.")
        product_name = get_user_input("Enter the product name: ").lower()

    quantity = get_user_input("Enter the quantity: ", input_type=int, error_message="Quantity must be a positive integer.")
    while quantity <= 0:
        print("Invalid quantity. Please enter a positive integer.")
        quantity = get_user_input("Enter the quantity: ", input_type=int, error_message="Quantity must be a positive integer.")

    return product_name, quantity

def print_table_headers(c, headers, x_coords):
    for i, header in enumerate(headers):
        c.drawString(x_coords[i], 9.5 * inch, f"{header}")

def print_table_line(c, x_start, x_end, y):
    c.line(x_start, y * inch, x_end, y * inch)

def print_customer_info(c, customer_name, customer_mobile, date, time):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, 10.6 * inch, f"Customer: {customer_name}")
    c.drawString(1 * inch, 10.4 * inch, f"Mobile: {customer_mobile}")
    c.drawString(1 * inch, 10.2 * inch, f"Date: {date}")
    c.drawString(1 * inch, 10.0 * inch, f"Time: {time}")

def print_grand_total(c, y, grand_total):
    c.line(1 * inch, y * inch, 8 * inch, y * inch)
    c.drawString(1 * inch, (y - 0.3) * inch, f"{'Grand Total: ' :}")
    c.drawString(2.2 * inch, (y - 0.3) * inch, f"{round(grand_total, 2)}")
    c.line(1 * inch, (y - 0.5) * inch, 8 * inch, (y - 0.5) * inch)

def generate_invoice(products):
    customer_name = get_user_input("Enter the name of the customer: ")
    customer_mobile = get_user_input("Enter the mobile number of the customer: ")

    # Current date and time
    date = datetime.date.today()
    time = datetime.datetime.now().strftime("%H:%M:%S")

    # Creating a unique file name for the PDF document
    file_name = f"bill_{customer_name}.pdf"

    # Creating a canvas object with the file name
    c = canvas.Canvas(file_name)

    # Creating an empty list to store the items purchased
    items = []

    # Asking the user how many items they want to buy
    num_items = get_user_input("How many products do you want to buy: ", input_type=int, error_message = "Number of products must be a positive integer.")
    if num_items < 0:
        print("Number of products must be a positive integer.")
        return

    # Loop through each item and asking the user for the product name and quantity
    for _ in range(num_items):
        product_name, quantity = get_product_details(products)
        price_per_unit = products[product_name]
        price, gst, total = calculate_price(quantity, price_per_unit)
        items.append((product_name, quantity, price, gst, total))

    # Printing the bill header on the PDF document
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(4 * inch, 11 * inch, "INVOICE")
    c.line(1 * inch, 9.8 * inch, 8 * inch, 9.8 * inch)
    c.setFont("Helvetica", 14)

    # Column headers
    headers = ['Product', 'Quantity', 'Price', 'GST(18%)', 'Total']

    # x-coordinate for each column
    x_coords = [1 * inch + i * 1.5 * inch for i in range(len(headers))]

    # Drawing column headers
    print_table_headers(c, headers, x_coords)

    # Printing the customer details and date and time on the left side
    print_customer_info(c, customer_name, customer_mobile, date, time)

    # Printing each item on the bill
    y = 8.5  
    grand_total = 0  
    for item in items:
        # Unpacking the item tuple
        product, quantity, price, gst, total = item

        # Drawing each item detail on the PDF document with formatting
        for i, value in enumerate([product, quantity, price, gst, total]):
            c.drawString(x_coords[i], y * inch, f"{value}")

        # Updating the grand total
        grand_total += total

        # Decreasing the y coordinate for drawing text
        y -= 0.4

    # Printing the grand total on the PDF document
    print_grand_total(c, y, grand_total)

    # Saving the PDF document
    c.save()

    print("Invoice generated:\n")
    print("Customer: ", customer_name)
    print("Mobile no: ", customer_mobile)
    print("Date: ", date)
    print("Time: ", time)
    print("{:<15}{:<15}{:<15}{:<15}{:<15}".format('Product', 'Quantity', 'Price', 'GST(18%)', 'Total'))
    for item in items:
        product, quantity, price, gst, total = item
        print("{:<15}{:<15}{:<15}{:<15}{:<15}".format(product, quantity, price, gst, total))
    print("\n Grand total: ", grand_total)
    print("\n Saved invoice as PDF with filename ", file_name)

# Function to load the users and passwords from the file
def load_users():
    try:
        with open(file_name, "rb") as f:
            return pickle.load(f)
    # If the file does not exist, returning an empty dictionary
    except FileNotFoundError:
        return {}

# Function to save the users and passwords to the file
def save_users(users):
    with open(file_name, "wb") as f:
        pickle.dump(users, f)

# Function to register a new user
def register():
    print("Please enter your details to register.")

    # Loading the users and passwords from the file
    users = load_users()  

    while True:
        user_id = input("Enter a user ID: ")
        password = input("Enter a password: ")

        # Checking if the user ID already exists
        if user_id in users and users[user_id] == password:
            print("\nUser ID and password already exist. Please choose another combination.\n")
        else:
            print("\n User successfully registered. Please login now. \n")
            break

    # Adding the user to the dictionary
    users[user_id] = password

    # Saving the users and passwords to the file
    save_users(users)

    print("Registration successful. You can now login.")

# Function to login an existing user
def login():
    print("Please enter your credentials to login.")

    # Loading the users and passwords from the file
    users = load_users()  
    while True:
        user_id = input("Enter your user ID: ")
        password = input("Enter your password: ")

        # Checking if the user ID and password match
        if user_id in users and users[user_id] == password:
            print("\nLogin successful. Welcome, " + user_id + ".")
            break
        else:
            print("\nInvalid user ID or password. Please try again.")

# Function to display the main menu
def main():
    while True:
        print("\n\n\t\t\t\t\t\tWelcome to Billing System \n")
        print("Please choose an option:\n")
        print("1. Register")
        print("2. Login")
        print("3. Display products")
        print("4. Exit\n")
        print("Note:-  \nM or m -> for Modifing product price or Adding new product")
        print("B or b -> for Billing")

        choice = input("\nEnter your choice: ")

        # For register
        if choice == "1":
            register()
            login()
            choice = input("Enter your choice (b or m): ")

            while choice.lower() not in ["b", "m"]:
                print("Invalid choice. Please try again.")
                choice = input("Enter your choice (b or m): ")

            if choice == "b":
                generate_invoice(products)  
            elif choice == "m":
                add_and_modify_items(products)  
                choice = input("Do you want to continue billing (press Y/N or y/n): ")
                if choice.lower() == "y":
                    generate_invoice(products)
                elif choice.lower() == "n":
                    print("Thank you for using the system. Goodbye.")
                    exit()
        # For login
        elif choice == "2":
            login()
            choice = input("Enter your choice (b or m): ")

            while choice not in ["b", "m"]:
                print("Invalid choice. Please try again.")
                choice = input("Enter your choice (b or m): ")

            if choice == "b":
                generate_invoice(products)  
            elif choice == "m":
                add_and_modify_items(products)  
                choice = input("Do you want to continue billing (press Y/N or y/n): ")
                if choice.lower() == "y":
                    generate_invoice(products)
                elif choice.lower() == "n":
                    print("Thank you for using the system. Goodbye.")
                    exit()
        elif choice == "3":
            print("\n{:<20} {:<10}".format("Item name", "Price"))
            for key in products:
              print("{:<20} {:<10}".format(key,products[key]))
            print("\n\n")
        elif choice == "4":
            print("Thank you for using the system. Goodbye.")
            exit()
        else:
            print("Invalid choice.")
            return

# _main_
main()