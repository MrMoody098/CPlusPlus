import turtle

# Create a turtle object
t = turtle.Turtle()
t.speed(10000)
#remove the arrow icon
t.hideturtle()
for i in range(5):
    x= 87
    t.forward(80)
    
    for i in range(x):
        t.forward(1*x)
        t.left(90*x+4)
        x = x-1
        t.color("red") if i % 2 == 0 else t.color("blue")
    
# Close the turtle graphics window
turtle.done()