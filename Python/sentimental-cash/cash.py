# TODO
from cs50 import get_float

# Prompt user for change input
while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

# Round to nearest whole number
change = round(change * 100)

# Declare variable for tracking increments of each coin type
count = 0

while change > 0:
    # Calculate the number of quarters to give the customer
    if change >= 25:
        change -= 25
        count += 1

    # Calculate the number of dimes to give the customer
    elif change >= 10:
        change -= 10
        count += 1

    # Calculate the number of nickels to give the customer
    elif change >= 5:
        change -= 5
        count += 1

    # Calculate the number of pennies to give the customer
    elif change >= 1:
        change -= 1
        count += 1

# Prints number of coins required for user input of change
print(count)