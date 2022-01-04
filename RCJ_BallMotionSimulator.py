#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter
import math

scale = 4

robotSpeed = 6
robotSize = 22 * scale 
robotX = 600
robotY = 600
robotCatchZone = 30
robotForwarding = 4

ballSize = 7.4 * scale
ballX = 600
ballY = 600

touchDistancingDeg = 1 #内側からの距離補正の次数.2以上だと加速度が滑らかに,1だと無駄な安定な点ができない
touchDistance = (robotSize+ballSize)/2
root = tkinter.Tk()
root.geometry("1200x1250")

canvas = tkinter.Canvas(root, bg="#fff", width=1200, height=1200)
canvas.pack()

#軸の描画

robot = canvas.create_oval(robotX-robotSize/2,robotY-robotSize/2,robotX+robotSize/2,robotY+robotSize/2, fill="#f0f0f0", tags="robot")
canvas.create_oval(ballX-ballSize/2,ballY-ballSize/2,ballX+ballSize/2,ballY+ballSize/2, fill="#f0f0f0",tags="ball")


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
    if(the == 0):
        theSign = 1
    else:
        theSign = (abs(the)/the)

    if(r <= touchDistance):
        m = (1,-the + theSign*((r/touchDistance)**touchDistancingDeg)*3*math.pi/2 )
    elif(r > touchDistance and x >= -touchDistance):
        m = (1,-theSign*(math.pi - abs(the) + math.asin(touchDistance/r)))
    elif(r > touchDistance and x < -touchDistance):
        m = (1,-theSign*(math.pi - abs(the) + math.atan((-x/abs(y))) - math.atan(((-x-touchDistance)/abs(y)))))

    return m

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

def mouse(event):
    global ballX
    global ballY
    ballX = event.x
    ballY = event.y
    
def draw():
    global robotX
    global robotY
    global robotSize
    global robotSpeed
    global robotCatchZone

    #dX,dY = getXY(getBallRD(motion(getRobotRD(getRD(robotX,robotY)))))
    rRD,theRD = getRD(robotX-ballX,robotY-ballY)
    rRobotRD,theRobotRD=getRobotRD(rRD,theRD)
    rMotion,theMotion=motion(rRobotRD,theRobotRD)
    rBallRD,theBallRD=getBallRD(rMotion,theMotion)
    dX,dY=getXY(rBallRD,theBallRD)
    
    robotX += robotSpeed * dX 
    robotY += robotSpeed * dY

    canvas.delete("all")
    canvas.create_oval(ballX-ballSize/2,ballY-ballSize/2,ballX+ballSize/2,ballY+ballSize/2, fill="#f0f0f0",tags="ball")
    canvas.create_oval(robotX-robotSize/2,robotY-robotSize/2,robotX+robotSize/2,robotY+robotSize/2, fill="#f0f0f0", tags="robot")
    #canvas.move(robot, 5, 0)
    canvas.after(10, clk)
        

def clk():
    canvas.bind("<Motion>", mouse)
    draw()

Start = tkinter.Button(root, text="Start", command=clk)
Start.pack()


root.mainloop()