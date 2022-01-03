#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter
import math

robotSpeed = 0.5
robotSize = 150
robotX = 601
robotY = 601

ballSize = 50
ballX = 600
ballY = 600

touchDistance = (robotSize+ballSize)/2

moveFlag = 0

root = tkinter.Tk()
root.geometry("1200x1250")

canvas = tkinter.Canvas(root, bg="#fff", width=1200, height=1200)
canvas.pack()

#軸の描画
canvas

robot = canvas.create_oval(robotX-robotSize/2,robotY-robotSize/2,robotX+robotSize/2,robotY+robotSize/2, fill="#f0f0f0", tags="robot")
canvas.create_oval(ballX-ballSize/2,ballY-ballSize/2,ballX+ballSize/2,ballY+ballSize/2, fill="#f0f0f0")


def motion(r,the):
    if(the < -math.pi):
        while(the < -math.pi):
            the += 2*math.pi
    elif(the >= math.pi):
        while(the >= math.pi):
            the -= 2*math.pi
    x,y = getXY(r,the)
    print(r,360*the/2/math.pi,x,y)
    #以下に回り込みのアルゴリズムを記入
    if(r <= touchDistance):
        print(1)
        return (1,-the + (abs(the)/the)*((r/touchDistance)**2)*3*math.pi/2 )
    elif(r > touchDistance and x >= -touchDistance):
        print(2)
        return (1,-(abs(the)/the)*(math.pi - abs(the) + math.asin(touchDistance/r)))
    elif(r > touchDistance and x < -touchDistance):
        print(3,x/abs(y))
        return (1,-(abs(the)/the)*(math.pi - abs(the) + math.atan((-x/abs(y))) - math.atan(((-x+touchDistance)/abs(y)))))
    #return(1,-the/2)

def getRobotRD(ballR,ballThe):
    return ballR,-ballThe

def getBallRD(robotR,robotThe):
    return robotR,-robotThe


def getXY(r, the):
    x = r * math.cos(the)
    y = r * math.sin(the)
    return x, y

def getRD(x,y):
    r = math.sqrt(x**2+y**2)
    the = math.atan2(y, x)
    return r,the 
    
def draw():
    global robotX
    global robotY
    global robotSize
    global robotSpeed

    #dX,dY = getXY(getBallRD(motion(getRobotRD(getRD(robotX,robotY)))))
    rRD,theRD = getRD(robotX-600,robotY-600)
    rRobotRD,theRobotRD=getRobotRD(rRD,theRD)
    rMotion,theMotion=motion(rRobotRD,theRobotRD)
    rBallRD,theBallRD=getBallRD(rMotion,theMotion)
    dX,dY=getXY(rBallRD,theBallRD)
    
    robotX += robotSpeed * dX 
    robotY += robotSpeed * dY

    canvas.delete("robot")
    canvas.create_oval(robotX-robotSize/2,robotY-robotSize/2,robotX+robotSize/2,robotY+robotSize/2, fill="#f0f0f0", tags="robot")
    #canvas.move(robot, 5, 0)
    if moveFlag == 0:
        canvas.after(2, draw)
        

def clk():
    draw()

Start = tkinter.Button(root, text="Start", command=clk)
Start.pack()

root.mainloop()