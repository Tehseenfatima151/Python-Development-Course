from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

user_guess = screen.textinput(title="Make your guess", prompt="Which turtle will win the race? Enter a color: ")

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
all_turtles = []

y_position = -70
for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_position)
    y_position += 30
    all_turtles.append(new_turtle)

is_race_on = False
if user_guess:
    is_race_on = True

while is_race_on:
    for racing_turtle in all_turtles:
        if racing_turtle.xcor() > 230:
            is_race_on = False
            winning_color = racing_turtle.pencolor()

            if winning_color == user_guess:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")

        random_distance = random.randint(0, 10)
        racing_turtle.forward(random_distance)

screen.exitonclick()