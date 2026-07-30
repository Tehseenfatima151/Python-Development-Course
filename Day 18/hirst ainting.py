from turtle import Turtle, Screen
import random

tim = Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

screen = Screen()
screen.colormode(255)

color_list = [
    (247, 216, 55), (242, 226, 12), (242, 202, 12), (240, 65, 35),
    (237, 28, 36), (196, 40, 27), (26, 90, 44), (10, 136, 61),
    (69, 176, 78), (13, 152, 186), (27, 91, 156), (33, 63, 145),
    (240, 65, 35), (69, 176, 78), (247, 216, 55), (26, 90, 44),
    (18, 82, 154), (196, 40, 27), (242, 226, 12), (10, 136, 61),
]

tim.setheading(225)
tim.forward(300)
tim.setheading(0)

number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)

screen.exitonclick()