# Data Warehousing HW1
# Patrick Richeal and Benny Liang

import datetime
import random
import operator

# Constants
DAILY_CUSTOMERS_LOW = 1140
DAILY_CUSTOMERS_HIGH = 1180
PRICE_MULTIPLIER = 1.1
START_DATE = datetime.datetime(2017, 1, 1)
MAX_CUSTOMER_ITEMS = 100
WEEKEND_CUSTOMER_INCREASE = 50

# Statistics
total_customers = 0
total_sales = 0
total_items_bought = 0
items_purchased_by_sku = {}

# Files
PRODUCTS_FILE = 'Products1.txt'
OUTPUT_FILE = 'output.csv'

# Load product file
products_file = open(PRODUCTS_FILE, 'r', encoding = 'ISO-8859-1').readlines()[1:]

# Remove contents of current output file if exists, then reopen for appending
open(OUTPUT_FILE, 'w').close()
output_file = open(OUTPUT_FILE, 'a')

# List for holding all products
products_list = []

# Dictionary for holding lists of products by type
products = {}

# Create products dictionary
for product in products_file:
    product = product.rstrip().split('|')
    product_obj = {
        'manufacturer': product[0],
        'name': product[1],
        'size': product[2],
        'type': product[3],
        'sku': product[4],
        'price': float(product[5][1:]) # [1:0] to remove the dollar sign
    }

    # Add product to list
    products_list.append(product_obj)

    # Add product to correct type in products dictionary
    if product_obj['type'] in products:
        products[product_obj['type']].append(product_obj)
    else:
        products[product_obj['type']] = [product_obj]

# Return a random product, optionally within a specific product type
def get_random_product(product_type = None):
    if product_type is None:
        # No product type passed in, send back a random product from any type
        return random.choice(products_list)
    else:
        # Product type passed in, send back a random product from that type specifically
        return random.choice(products[product_type])

# Write a purchased product to output file
def write_record(date, customer, product):
    global total_sales

    sale_price = round(product['price'] * PRICE_MULTIPLIER, 2)

    total_sales += sale_price

    if product['sku'] in items_purchased_by_sku:
        items_purchased_by_sku[product['sku']] += 1
    else:
        items_purchased_by_sku[product['sku']] = 1

    output_string = date.strftime('%x') + ',' + str(customer) + ',' + product['sku'] + ',' + str(sale_price) + '\n'
    output_file.write(output_string)

def get_item_by_sku(sku):
    for product in products_list:
        if product['sku'] == sku:
            return product
    return None

# For every day of the year
for day in range(365):
    # Current date is start date plus number of days
    current_date = START_DATE + datetime.timedelta(days = day)

    # Get random customer count for the day
    customer_count = random.randint(DAILY_CUSTOMERS_LOW, DAILY_CUSTOMERS_HIGH)

    # If its a weekend, add 50 customers
    if current_date.weekday() > 4:
        customer_count += WEEKEND_CUSTOMER_INCREASE

    total_customers += customer_count
    
    # For every one of today's customers
    for customer in range(1, customer_count):
        # Get random number of items for customer to purchase today
        items_to_purchase = random.randint(1, MAX_CUSTOMER_ITEMS)
        items_purchased = 0

        total_items_bought += items_to_purchase

        # 70% chance of buying milk
        if items_purchased < items_to_purchase and random.randint(1, 100) <= 70:
            write_record(current_date, customer, get_random_product('Milk'))
            items_purchased += 1

            # 50% chance of buying cereal
            if items_purchased < items_to_purchase and random.randint(1, 100) <= 50:
                write_record(current_date, customer, get_random_product('Cereal'))
                items_purchased += 1
        elif items_purchased < items_to_purchase and random.randint(1, 100) <= 5:
            # 5% chance of buying cereal
            write_record(current_date, customer, get_random_product('Cereal'))
            items_purchased += 1
        
        # 20% chance of buying baby food
        if items_purchased < items_to_purchase and random.randint(1, 100) <= 20:
            write_record(current_date, customer, get_random_product('Baby Food'))
            items_purchased += 1

            # 80% chance of buying diapers
            if items_purchased < items_to_purchase and random.randint(1, 100) <= 80:
                write_record(current_date, customer, get_random_product('Diapers'))
                items_purchased += 1
        elif items_purchased < items_to_purchase and random.randint(1, 100) == 1:
            # 1% chance of buying diapers
            write_record(current_date, customer, get_random_product('Diapers'))
            items_purchased += 1
        
        # 50% chance of buying bread
        if items_purchased < items_to_purchase and random.randint(1, 100) <= 50:
            write_record(current_date, customer, get_random_product('Bread'))
            items_purchased += 1
        
        # 10% chance of buying peanut butter
        if items_purchased < items_to_purchase and random.randint(1, 100) <= 10:
            write_record(current_date, customer, get_random_product('Peanut Butter'))
            items_purchased += 1

            # 90% change of buying jam or jelly
            if items_purchased < items_to_purchase and random.randint(1, 100) <= 90:
                write_record(current_date, customer, get_random_product('Jelly/Jam'))
                items_purchased += 1
            # 5% change of buying jam or jelly
        elif items_purchased < items_to_purchase and random.randint(1, 100) <= 5:
            write_record(current_date, customer, get_random_product('Jelly/Jam'))
            items_purchased += 1

        # Random items for the rest
        for i in range(items_purchased + 1, items_to_purchase):
            write_record(current_date, customer, get_random_product())

sorted_purchases = dict(sorted(items_purchased_by_sku.items(), key=operator.itemgetter(1), reverse=True))

print("Total customers: " + str(total_customers))
print("Total sales: $" + str(round(total_sales, 2)))
print("Total items bought: " + str(total_items_bought))
print("==== Top 10 Selling Items ====")
print("1. " + str(get_item_by_sku(list(sorted_purchases)[0])['name']) + " (SKU #" + str(list(sorted_purchases)[0]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[0]]) + " times")
print("2. " + str(get_item_by_sku(list(sorted_purchases)[1])['name']) + " (SKU #" + str(list(sorted_purchases)[1]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[1]]) + " times")
print("3. " + str(get_item_by_sku(list(sorted_purchases)[2])['name']) + " (SKU #" + str(list(sorted_purchases)[2]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[2]]) + " times")
print("4. " + str(get_item_by_sku(list(sorted_purchases)[3])['name']) + " (SKU #" + str(list(sorted_purchases)[3]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[3]]) + " times")
print("5. " + str(get_item_by_sku(list(sorted_purchases)[4])['name']) + " (SKU #" + str(list(sorted_purchases)[4]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[4]]) + " times")
print("6. " + str(get_item_by_sku(list(sorted_purchases)[5])['name']) + " (SKU #" + str(list(sorted_purchases)[5]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[5]]) + " times")
print("7. " + str(get_item_by_sku(list(sorted_purchases)[6])['name']) + " (SKU #" + str(list(sorted_purchases)[6]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[6]]) + " times")
print("8. " + str(get_item_by_sku(list(sorted_purchases)[7])['name']) + " (SKU #" + str(list(sorted_purchases)[7]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[7]]) + " times")
print("9. " + str(get_item_by_sku(list(sorted_purchases)[8])['name']) + " (SKU #" + str(list(sorted_purchases)[8]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[8]]) + " times")
print("10. " + str(get_item_by_sku(list(sorted_purchases)[9])['name']) + " (SKU #" + str(list(sorted_purchases)[9]) + ") purchased " + str(sorted_purchases[list(sorted_purchases)[9]]) + " times")