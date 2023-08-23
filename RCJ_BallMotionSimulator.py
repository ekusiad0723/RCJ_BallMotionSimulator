"""
This program simulates the motion of a robot and a ball on a canvas using tkinter library. 
The robot moves towards the ball and catches it when it enters its catch zone. 
The ball then moves in the direction of the robot's motion until it hits the wall or the robot catches it again. 
The program uses the motion() function to calculate the robot's motion based on the ball's position. 
The getXY() function is used to convert polar coordinates to cartesian coordinates. 
The getRD() function is used to convert cartesian coordinates to polar coordinates. 
The getRobotRD() and getBallRD() functions are used to convert the robot's and ball's polar coordinates to cartesian coordinates. 
The draw() function is used to update the positions of the robot and the ball on the canvas. 
The mouse() function is used to update the position of the ball based on the mouse movement. 
"""

import tkinter
import math

# Constants
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

# Create the tkinter window and canvas
root = tkinter.Tk()
root.geometry("1200x1250")
canvas = tkinter.Canvas(root, bg="#fff", width=1200, height=1200)
canvas.pack()

# Create the robot and ball objects on the canvas
robot = canvas.create_oval(robotX-robotSize/2,robotY-robotSize/2,robotX+robotSize/2,robotY+robotSize/2, fill="#f0f0f0", tags="robot")
canvas.create_oval(ballX-ballSize/2,ballY-ballSize/2,ballX+ballSize/2,ballY+ballSize/2, fill="#f0f0f0",tags="ball")

def motion(r,the):
    """
    Calculates the robot's motion based on the ball's position.
    """
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
    """
    Converts the ball's polar coordinates to cartesian coordinates.
    """
    return ballR,-ballThe

def getBallRD(robotR,robotThe):
    """
    Converts the robot's polar coordinates to cartesian coordinates.
    """
    return robotR,-robotThe

def getXY(r, the):
    """
    Converts polar coordinates to cartesian coordinates.
    """
    x = r * math.cos(the)
    y = r * math.sin(the)
    return x, y

def getRD(x,y):
    """
    Converts cartesian coordinates to polar coordinates.
    """
    r = math.sqrt(x**2+y**2)
    the = math.atan2(y, x)
    return r,the 

def mouse(event):
    """
    Updates the position of the ball based on the mouse movement.
    """
    global ballX
    global ballY
    ballX = event.x
    ballY = event.y
    
def draw():
    """
    Updates the positions of the robot and the ball on the canvas.
    """
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
    root.after(10, draw)
        

def clk():
    """
    Starts the simulation.
    """
    canvas.bind("<Motion>", mouse)
    draw()

# Create the Start button
Start = tkinter.Button(root, text="Start", command=clk)
Start.pack()

# Start the tkinter mainloop
root.mainloop()