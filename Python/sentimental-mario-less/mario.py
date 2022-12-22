# TODO

# ensure valid input; prompt user if height is < 1 or > 8
while True:
    try:
        height = int(input("height: "))
    except ValueError:
        print("That is not a valid integer!")
        continue
    else:
        if height >= 1 and height <= 8:
            break
        else:
            print("Please input an integer between 1 and 8.")

# iterate through height
for i in range(height):
    print((height - 1 - i) * " ", end="")
    print((i + 1) * "#")