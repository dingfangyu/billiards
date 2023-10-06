from Tkinter import *
from time import *
from math import *


class Ball:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.r=10
        self.u=600
    def change_u(self):
        if self.vx==0:return
        temx=self.u*0.01*self.vx/((self.vx*self.vx+self.vy*self.vy)**0.5)
        temy=self.u*0.01*self.vy/((self.vx*self.vx+self.vy*self.vy)**0.5)
        if self.vx*(self.vx-temx)<=0:
            self.stop()
            return
        self.vx-=temx
        self.vy-=temy
    def stop(self):
        self.vx=0
        self.vy=0
    def hitx(self):
        self.vx=-self.vx
    def hity(self):
        self.vy=-self.vy
    def in_hole(self):
        if ((self.x-450)**2+(self.y-450)**2)**0.5<=12:
            L.remove(self)
            c.delete(D[self])
            l=Label(root,text="nice shot!!!")
            l.pack()
        
class white(Ball):
    def in_hole(self):
        if ((self.x-450)**2+(self.y-450)**2)**0.5<=12:
            L.remove(self)
            c.delete(D[self])
            l=Label(root,text="The white ball in hole!!!Please restart")
            l.pack()
        
def hit1(x,vx):
    if x<=10 and vx<0:return True
    return False
def hit3(x,vx):
    if x>=490 and vx>0:return True
    return False
def hit4(y,vy):
    if y<=10 and vy<0:return True
    return False
def hit2(y,vy):
    if y>=490 and vy>0:return True
    return False

def loop(event):
    if not stop():
        c.delete(lb,le,_e)
        return
    c.delete(lb,le,_e)
    global number
    number=number+1
    l.config(text='Pole number:'+str(number))
    l.pack()
    ballw.vx=(event.x-ballw.x)*10
    ballw.vy=(event.y-ballw.y)*10
    
    while L!=[]:
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                if hite(L[i],L[j]):
                    v1x,v1y,v2x,v2y=away(L[i],L[j])
                    L[i].vx,L[i].vy,L[j].vx,L[j].vy=v1x,v1y,v2x,v2y
        for ball in L:
          one(ball)
        root.update()
        sleep(0.03)
    l.config(text='YOU WIN! The total Pole number is'+str(number))
    l.pack()

_e,lb,le=False,False,False
def extraball(event):
    global _e,lb,le
    if _e!=0:
        c.delete(_e)
    if lb!=0:
        c.delete(lb)
    if le!=0:
        c.delete(le)

    bbox_e=event.x-10,event.y-10,event.x+10,event.y+10
    _e=c.create_oval(bbox_e,outline="aliceblue",width=3)
    
    vex=event.x-ballw.x
    vey=event.y-ballw.y
    e=Ball(ballw.x,ballw.y,vex,vey)
    
    for b in [ball1,ball2,ball3,ball4,ball5,ball6]:
        if ((b.x-event.x)**2+(b.y-event.y)**2)**0.5<=22:
            while not hite(b,e):
                e.x+=e.vx*0.001
                e.y+=e.vy*0.001
            vbx,vby,vex,vey=away(b,e)
            lb=c.create_line(b.x,b.y,b.x+vbx,b.y+vby,fill=c.itemcget(D[b],'fill'),width=2)
            le=c.create_line(e.x,e.y,e.x+vex,e.y+vey,fill='white',width=2)

def one(ball):
    ball.in_hole()
    dx=ball.vx*0.01
    dy=ball.vy*0.01
    ball.x+=dx
    ball.y+=dy
    c.move(D[ball],dx,dy)
    if hit1(ball.x,ball.vx) or hit3(ball.x,ball.vx):ball.hitx()
    if hit2(ball.y,ball.vy) or hit4(ball.y,ball.vy):ball.hity()
    ball.change_u()
def hite(ball1,ball2):
    if ((ball1.x-ball2.x)**2+(ball1.y-ball2.y)**2)**0.5<=22:return True
    return False
def away(ball1,ball2):
    theta=atan(float(ball2.x-ball1.x)/(ball1.y-ball2.y+0.000000000000001))
    tem1p=ball1.vx*cos(theta)+ball1.vy*sin(theta)
    tem1v=-ball2.vx*sin(theta)+ball2.vy*cos(theta)
    tem2p=ball2.vx*cos(theta)+ball2.vy*sin(theta)
    tem2v=ball1.vx*sin(theta)-ball1.vy*cos(theta) 
    v1x=tem1p*cos(theta)-tem1v*sin(theta)
    v1y=tem1p*sin(theta)+tem1v*cos(theta)
    v2x=tem2p*cos(theta)+tem2v*sin(theta)
    v2y=tem2p*sin(theta)-tem2v*cos(theta)
    if ((ball1.x+v1x*0.01-ball2.x-v2x*0.01)**2+(ball1.y+v1y*0.01-ball2.y-v2y*0.01)**2)**0.5<=22:return ball1.vx,ball1.vy,ball2.vx,ball2.vy
    return v1x,v1y,v2x,v2y
def stop():
    for i in L:
        if i.vx!=0:return False
    return True

def restart(event):
    global number,ballw,_ballw,ball1,_ball1,ball2,_ball2,ball3,_ball3,ball4,_ball4,ball5,_ball5,ball6,_ball6,hole,L,D
    for i in [_ballw,_ball1,_ball2,_ball3,_ball4,_ball5,_ball6]:
        c.delete(i)
    number=0
    ballw=white(250,150,0,0)
    _ballw=c.create_oval(ballw.x-10,ballw.y-10,ballw.x+10,ballw.y+10,fill='white',outline='white')
    ball1=Ball(110,300,0,0)
    _ball1=c.create_oval(ball1.x-10,ball1.y-10,ball1.x+10,ball1.y+10,fill='red',outline='red')
    ball2=Ball(140,100,0,0)
    _ball2=c.create_oval(ball2.x-10,ball2.y-10,ball2.x+10,ball2.y+10,fill='blue',outline='blue')
    ball3=Ball(170,200,0,0)
    _ball3=c.create_oval(ball3.x-10,ball3.y-10,ball3.x+10,ball3.y+10,fill='grey',outline='grey')
    ball4=Ball(200,100,0,0)
    _ball4=c.create_oval(ball4.x-10,ball4.y-10,ball4.x+10,ball4.y+10,fill='yellow',outline='yellow')
    ball5=Ball(250,300,0,0)
    _ball5=c.create_oval(ball5.x-10,ball5.y-10,ball5.x+10,ball5.y+10,fill='orange',outline='orange')
    ball6=Ball(400,100,0,0)
    _ball6=c.create_oval(ball6.x-10,ball6.y-10,ball6.x+10,ball6.y+10,fill='purple',outline='purple')
    hole=c.create_oval(450-11,450-11,450+11,450+11,fill='black')
    L=[ballw,ball1,ball2,ball3,ball4,ball5,ball6]
    D={ballw:_ballw,ball1:_ball1,ball2:_ball2,ball3:_ball3,ball4:_ball4,ball5:_ball5,ball6:_ball6}



number=0
root=Tk()
c=Canvas(root,width=500,height=500,bg='green')
c.pack()
ballw=white(250,150,0,0)
_ballw=c.create_oval(ballw.x-10,ballw.y-10,ballw.x+10,ballw.y+10,fill='white',outline='white')
ball1=Ball(110,300,0,0)
_ball1=c.create_oval(ball1.x-10,ball1.y-10,ball1.x+10,ball1.y+10,fill='red',outline='red')
ball2=Ball(140,100,0,0)
_ball2=c.create_oval(ball2.x-10,ball2.y-10,ball2.x+10,ball2.y+10,fill='blue',outline='blue')
ball3=Ball(170,200,0,0)
_ball3=c.create_oval(ball3.x-10,ball3.y-10,ball3.x+10,ball3.y+10,fill='grey',outline='grey')
ball4=Ball(200,100,0,0)
_ball4=c.create_oval(ball4.x-10,ball4.y-10,ball4.x+10,ball4.y+10,fill='yellow',outline='yellow')
ball5=Ball(250,300,0,0)
_ball5=c.create_oval(ball5.x-10,ball5.y-10,ball5.x+10,ball5.y+10,fill='orange',outline='orange')
ball6=Ball(400,100,0,0)
_ball6=c.create_oval(ball6.x-10,ball6.y-10,ball6.x+10,ball6.y+10,fill='purple',outline='purple')
hole=c.create_oval(450-11,450-11,450+11,450+11,fill='black')
L=[ballw,ball1,ball2,ball3,ball4,ball5,ball6]
D={ballw:_ballw,ball1:_ball1,ball2:_ball2,ball3:_ball3,ball4:_ball4,ball5:_ball5,ball6:_ball6}
l=Label(root,text='Pole number:'+str(number))
quitButton=Button(root,text='Restart')
quitButton.bind('<1>',restart)
quitButton.pack()
c.bind("<B1-Motion>",extraball)
c.bind("<ButtonRelease-1>",loop)
root.mainloop()


