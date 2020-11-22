#PythonDraw.py
import turtle
turtle.setup(650, 350, 200, 200)
turtle.penup()
turtle.fd(0)
turtle.right(90)
turtle.fd(200)
turtle.left(90)
turtle.pendown()
turtle.pensize(5)
turtle.pencolor(0.714,0.135,0.151)
turtle.seth(0)

for i in range(8):
    turtle.circle(50, 45)
    turtle.circle(-100, 45)
    turtle.circle(50, 45)
#**********外圈**********
turtle.penup()
turtle.left(90)
turtle.fd(30)
turtle.right(90)
turtle.pendown()

turtle.circle(170, 360)
#**********中圈**********
turtle.penup()
turtle.left(90)
turtle.fd(60)
turtle.right(90)
turtle.pendown()

turtle.circle(110,45)
turtle.penup()
turtle.circle(110,20)
turtle.pendown()
turtle.circle(110,145)
#*****45+20+145*****
turtle.penup()
turtle.circle(110,5)
turtle.pendown()
turtle.right(90)
turtle.circle(10,360)
turtle.left(90)
turtle.penup()
turtle.circle(110,15)
turtle.pendown()
#*****20*****
turtle.circle(110,15)
turtle.penup()
turtle.circle(110,10)
turtle.pendown()
turtle.circle(110,120)
#*****15+10+120*****
#**********内圈**********
turtle.penup()
turtle.circle(110,50)
turtle.pendown()

turtle.seth(-45)
turtle.circle(-20,90)
turtle.seth(180)
turtle.fd(70)
turtle.seth(45)
turtle.circle(20,90)
turtle.seth(0)
turtle.fd(70)
#*****Dian外围*****
turtle.penup()
turtle.right(90)
turtle.fd(15)
turtle.right(90)
turtle.fd(5)
turtle.pendown()
turtle.fd(50)
#*****Dian内部*****
#**********Dian**********
turtle.penup()
turtle.left(90)
turtle.fd(15)
turtle.right(90)
turtle.fd(15)
turtle.pendown()

turtle.fd(30)
turtle.right(45)
turtle.fd(15)
turtle.left(90)
turtle.fd(15)
turtle.right(45)
turtle.fd(30)
turtle.right(135)
#下
turtle.fd(15)
turtle.circle(15,85)
turtle.fd(120)
turtle.right(135)
#左
turtle.fd(65)
turtle.seth(-45)
turtle.fd(15)
turtle.circle(45,90)
turtle.fd(15)
turtle.seth(5)
turtle.fd(65)
turtle.right(135)
#上
turtle.fd(120)
turtle.circle(15,85)
turtle.fd(15)
turtle.right(135)
#右
#*****Xi外围*****
turtle.penup()
turtle.fd(10)
turtle.pendown()

turtle.right(45)
turtle.fd(20)
turtle.circle(-10,60)
#捺
turtle.penup()
turtle.right(180)
turtle.circle(10,60)
turtle.fd(20)
turtle.right(135)
turtle.fd(20)
turtle.right(45)
turtle.fd(15)
turtle.left(90)
turtle.fd(15)
turtle.right(45)
turtle.fd(20)
turtle.right(135)
turtle.pendown()

turtle.fd(20)
turtle.circle(10,60)
#撇
#*****Xi内部*****
#**********Xi**********
turtle.done()
