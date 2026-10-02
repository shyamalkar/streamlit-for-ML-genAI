from turtle import *
from colorsys import *


setposition(50, -50)
speed(0)
bgcolor('black')
pensize(2)

h = 0  


for j in range(120):
    for i in range(4):  
        color(hsv_to_rgb(h, 1, 1))
        h += 0.003
        circle(40 + i * 5, 90)
        forward(250)
        left(90)
    rt(10)

hideturtle()
done()
