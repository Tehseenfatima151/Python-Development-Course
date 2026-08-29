from turtle import Turtle
import random


class Food(Turtle):
    """Models a piece of food that appears at random positions for the snake to eat."""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.8, stretch_wid=0.8)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Moves the food to a new random position on the screen."""
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)