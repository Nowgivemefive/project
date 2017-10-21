import turtle
import numpy as np
import random
import tkinter as tk

#随机
def randomstat():
    if random.random() > 0.5:
        return True
    else:
        return False
# 是否撞墙
def iswall(ob):
    x,y = ob.position()
    if x>320 or x<-310 or y>230 or y<-400:
        return True
    else:
        return False
    
#1
def getRandomPos():
    '''
    # x 320 -310
    # y 230 -400
    get random position
    rtype:tupe (x,y)
    '''
    x = random.randint(-310,320)
    y = random.randint(-400,230)
    return (x,y)
#2
def towardPoint(x,y,*obs):
    '''
    type:int x
    type:int y
    type:RawTurtle obs
    rtype:None
    '''
    for ob in obs:
        ob.left(ob.towards(x,y))
    return
#3
def m__forward(distance,*obs):
    '''
    type:int distance
    type:RawTurtle bs
    rtype:None
    '''
    for ob in obs:
        ob.forward(distance)
        if iswall(ob):
                ob.undo()
    return
def m__backward(distance,*obs):
    '''
    type:int distance
    type:RawTurtle bs
    rtype:None
    '''
    for ob in obs:
        ob.backward(distance)
        if iswall(ob):
                ob.undo()
    return

#4
def target_behaviour_for(ob_tar,obs):
    '''
    type:RawTurtle ob_tar
    type:RawTurtle ob_tars
    rtype:None
    '''
    #如果只有一个实例
    if obs == None:
        ob.left(ob.towards((x,y)) - ob.heading())
        ob.forward(50)
        if iswall(ob):
            ob.undo()
    for ob_t in ob_tar:
        x,y = ob_t.position()
        for ob in obs:
            ob.left(ob.towards((x,y)) - ob.heading())
            ob.forward(50)
            if iswall(ob):
                ob.undo()
    return

def target_behaviour_back(ob_tar,obs):
    '''
    type:RawTurtle ob_tar
    type:RawTurtle ob_tars
    rtype:None
    '''
    #如果只有一个实例
    if obs == None: 
        ob.left(ob.towards((x,y)) - ob.heading())
        ob.backward(50)
        if iswall(ob):
            ob.undo()
    for ob_t in ob_tar:
        x,y = ob_t.position()
        for ob in obs:
            ob.left(ob.towards((x,y)) - ob.heading())
            ob.backward(50)
            if iswall(ob):
                ob.undo()
    return 
#4
def worker_behaviour_for(ob_work,ob_tar):
    '''
    type:RawTurtle ob_work
    type:RawTurtle ob_tar
    rtype:None
    '''
    x_t,y_t = ob_tar.position()
    ob_work.left(ob_work.towards((x_t,y_t)) - ob_work.heading())
    ob_work.forward(100)
    return
def worker_behaviour_back(ob_work,ob_tar):
    '''
    type:RawTurtle ob_work
    type:RawTurtle ob_tar
    rtype:None
    '''
    x_t,y_t = ob_tar.position()
    ob_work.left(ob_work.towards((x_t,y_t)) - ob_work.heading())
    ob_work.backward(100)
    return

#编写一个函数，在每个龟和它最近的邻居之间画一条直线
def mkline(ob,*obs):
    '''
    type:RawTurtle ob_work
    type:RawTurtle ob_tar
    rtype:None
    '''
    dis_list = []
    for item in range(len(obs)):
        dis_list.append((item,ob.distance(obs[item].position())))
    dis_list = sorted(dis_list, key = lambda temp:temp[1])
    if dis_list[0][1] == dis_list[1][1]:
        ob.write('具有相同距离的点')
    x,y = ob.position()
    ob.down()
    ob.goto(obs[dis_list[0][0]].position())
    ob.goto(x,y)
    ob.up()
    ob.clear()
    return


root =tk.Tk()
root.title("Turtle")
root.geometry('800x640')
cv = tk.Canvas(root,bg='white',height=800,width=640)
cv.pack()

a = turtle.RawPen(cv)
b = turtle.RawPen(cv)
c = turtle.RawPen(cv)
d = turtle.RawPen(cv)

i = [a,b,c,d]
for ob in i:
    ob.up()
    ob.setpos(getRandomPos())# 随机放置多个海龟在画布上

'''
向中心随机移动 
'''
while True:
    towardPoint(0,0,a,b,c,d) #朝向共同点
    #随机前进和后退
    if randomstat: 
        m__forward(random.randint(0,50),a,b,c,d) 
    else:
        m__backward(random.randint(0,50),a,b,c,d)
    #随机吸引或驱赶
    if randomstat:
        target_behaviour_for(ob_tar=[a,b],obs=[c,d])
    else:
        target_behaviour_back(ob_tar=[a,b],obs=[c,d])
    mkline(a,b,c,d)
    mkline(b,a,c,d)
    mkline(c,a,b,d)
    mkline(d,a,b,c)
#worker_behaviour_for(a,b)
#worker_behaviour_back(a,b)
root.mainloop()
'''
介绍随机移动海龟之间的碰撞检测
两点坐标相等
if ob.position() == ob.position():
    pass
'''
