from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()
screen.listen()   # Screen banate hi turant listen shuru kar do


def move_forward():
    tim.forward(10)


def turn_left():
    new_heading = tim.heading() + 10
    tim.setheading(new_heading)


def turn_right():
    new_heading = tim.heading() - 10
    tim.setheading(new_heading)


def clear_screen():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


screen.onkey(fun=move_forward, key="Up")
screen.onkey(fun=turn_left, key="Left")
screen.onkey(fun=turn_right, key="Right")
screen.onkey(fun=clear_screen, key="c")

screen.mainloop()   # exitonclick() ki bajaye ye zyada reliable hai listener ke liye