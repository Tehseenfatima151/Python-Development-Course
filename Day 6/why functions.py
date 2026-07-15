# Bina function ke - code repeat ho raha hai
print("Area of rectangle 1:", 5 * 3)
print("Area of rectangle 2:", 8 * 2)
print("Area of rectangle 3:", 10 * 4)

# Function ke sath - clean aur reusable
def rectangle_area(length, width):
    return length * width

print("Area of rectangle 1:", rectangle_area(5, 3))
print("Area of rectangle 2:", rectangle_area(8, 2))
print("Area of rectangle 3:", rectangle_area(10, 4))