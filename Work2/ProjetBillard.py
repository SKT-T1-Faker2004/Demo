from tkinter import *
import tkinter.filedialog as tkFileDialog
import math, csv

class Table:
    def __init__(self, x, y):
        #创建一个窗口
        self.fenetre = Tk()
        self.fenetre.title("Projet Billard")

        #创建菜单
        self.menubar = Menu(self.fenetre)
        self.menubar.add_command(label="Aide ?", command=self.tutoriel)
        self.fenetre.config(menu=self.menubar)

        #创建一个画面
        self.canvas = Canvas(self.fenetre, width=x, height=y, bg="DarkGreen")
        self.canvas.pack()

    def tutoriel(self):
        popup = Toplevel()
        popup.title("关于这个台球项目")
        tuto = Label(popup, text="左键：改变红球位置\n\
中间点击：改变黄球位置.\n\
右键：改变白球的位置\n\
Enter：发射\n\
Espace: 向右射出 (0°).\n\
Ctrl (droit): 换一个球.\n\
Ctrl+S: 将此次数据保存在一个 *.csv 文件中\n\
左下标注的是米 meter.")
        tuto.pack()

    def afficher(self):
        #启动窗口（程序的主循环）
        self.fenetre.mainloop()



class Ball:
    def __init__(self, fenetre, canvas, x, y, limx, limy, metre, temps, couleur):
        #窗口和canvas设定
        self.fenetre = fenetre
        self.canvas = canvas
        #坐标的设定
        self.coordx = x
        self.coordy = y
        #球桌的大小
        self.limx = limx
        self.limy = limy
        #每一个球的速度和分量
        self.vitesse = 0
        self.vitx = 0
        self.vity = 0
        #方向 (angle = 球的; theta = 射击的角度)
        self.angle = 0
        self.theta = 0
        self.focus = False
        self.dir_x = self.coordx + 20 + 32*math.cos(self.angle)
        self.dir_y = self.coordy + 20 - 32*math.sin(self.angle)
        self.dir = self.canvas.create_line(self.coordx, self.coordy,
                            self.coordx, self.coordy, width=2)
        self.flag = True
        #米的数值 px
        self.metre = metre
        #刷新时间
        self.temps = temps
        #显示球的路径
        self.couleur = couleur
        self.save = []
        #数据的保存
        self.savex = []
        self.savey = []
        self.savit = []
        self.sava = []
        #创建和显示对象
        self.objet = self.canvas.create_oval(self.coordx, self.coordy,
                            self.coordx+30, self.coordy+30, fill=couleur)
        self.centre = self.canvas.create_oval(self.coordx+14, self.coordy+14,
                            self.coordx+16, self.coordy+16, fill='black')

    def test_collision(self):
        #台球击中球桌边缘会反弹
        #... sauf si elle s'est trop enfoncée (and)
        #Et on ralentit (*0.5 (trouvé expérimentalement))
        """球的碰撞."""
##        if (self.coordx <= 0) and (self.vitx < 0):
##            self.vitx = - 0.5*self.vitx
##
##        elif (self.coordy <= 0) and (self.vity < 0):
##            self.vity = - 0.5*self.vity
##
##        elif (self.coordx +30 >= self.limx) and (self.vitx > 0):
##            self.vitx = - 0.5*self.vitx
##
##        elif (self.coordy +30 >= self.limy) and (self.vity >0):
##            self.vity = - 0.5*self.vity

        #这里是对边缘反弹反馈的管理
        #因为低速的效果更好
        pi = math.pi
        if (self.coordx <= 0) and (self.vitx < 0):
            self.vitesse = self.vitesse/2
            self.angle = pi - self.angle

        elif (self.coordy <= 0) and (self.vity < 0):
            self.vitesse = self.vitesse/2
            self.angle = 2*pi - self.angle

        elif (self.coordx +30 >= self.limx) and (self.vitx > 0):
            self.vitesse = self.vitesse/2
            self.angle = pi - self.angle

        elif (self.coordy +30 >= self.limy) and (self.vity > 0):
            self.vitesse = self.vitesse/2
            self.angle = 2*pi - self.angle

        """正在测试球和球之间的碰撞!!!"""
        for k in range(len(main.Boules)):
            #球之间的距离
            dist = math.sqrt((self.coordx - main.Boules[k].coordx)**2 +
                        (self.coordy - main.Boules[k].coordy)**2)
            #会发生碰撞 <=> 球间的距离 <= 半径的两倍
            #   会有碰撞发生
            if (dist <= 30) and (dist != 0):
                self.collision(main.Boules[k])
            if (self.flag == False) and (main.Boules[k].flag == False):
                self.collision(main.Boules[k])

    def viser(self, event):
        """方向的检测.==="""
        #勾股定理进行计算
        adj = event.x - self.coordx
        hypo = math.sqrt((event.x - self.coordx)**2 + (event.y - self.coordy)**2)
        if hypo == 0:
            hypo = 0.01
        angle = math.acos(adj/hypo)
        #确定是钝角还是锐角
        if event.y > self.coordy:
            angle = - angle
        #计算碰撞后向量的位置
        self.theta = angle
        self.dir_x = self.coordx + 15 + 32*math.cos(self.theta)
        self.dir_y = self.coordy + 15 - 32*math.sin(self.theta)
        #显示
        self.canvas.coords(self.dir, self.coordx+15, self.coordy+15, self.dir_x, self.dir_y)

    def tirer(self, vitesse):
        #删除旧的路径以及数据
        def supprsave(boule):
            count = 0
            for k in range(len(boule.save)):
                count += 1
                self.canvas.delete(self.canvas, boule.save[k])
            boule.save = []
            boule.savex = []
            boule.savey = []
            boule.savit = []
            boule.sava = []
        for k in range(len(main.Boules)):
            supprsave(main.Boules[k])
        #
        for k in range(len(main.Boules)):
            main.Boules[k].flag = True
        #速度的单位转化为dm/s 和 px/cs
        #速度 = 整体(dm/s=>m/s=>px/s)
        self.vitesse = int(vitesse/10*self.metre)
        self.angle = self.theta

    def move(self):
        #减速
        if main.loi.get() == "库伦法":
            self.ralentissement()
        else:
            self.ralentissement2()
        #位置的改变
        self.coordx += self.vitx*self.temps/1000
        self.coordy += self.vity*self.temps/1000
        self.test_collision()
        #移动
        self.canvas.coords(self.objet, self.coordx, self.coordy,
                            self.coordx+30, self.coordy+30)
        self.canvas.coords(self.centre, self.coordx+14, self.coordy+14,
                            self.coordx+16, self.coordy+16)
        #显示射击的方向
        if self.focus == True:
            #定向线段位置的计算
            self.dir_x = self.coordx + 15 + 32*math.cos(self.theta)
            self.dir_y = self.coordy + 15 - 32*math.sin(self.theta)
            #显示
            self.canvas.coords(self.dir, self.coordx+15, self.coordy+15,
                                self.dir_x, self.dir_y)
        else:
            self.canvas.coords(self.dir, self.coordx+15, self.coordy+15,
                                self.coordx+15, self.coordy+15)


    def ralentissement(self):
        #减速 (库伦计算法)
        #v(t) = -f*g*t + v0
        #在程序中循环几次∆t的测量,
        #一个确定的序列：
        #v(t + [delta t]ms) = 转换(-f*g*[delta t], m/s en px/s) + v(t)

        #f为这里的摩擦系数
        #对于∆t相关数量的计算
        f = float(main.frottement.get())
        t = self.temps/1000
        #关键，计算新的速度和分量
        self.vitesse = (-f*9.81*t)/10*self.metre + self.vitesse
        if self.vitesse < 0:
            self.vitesse = 0
        self.vitx = self.vitesse*math.cos(-self.angle)
        self.vity = self.vitesse*math.sin(-self.angle)

    def ralentissement2(self):
        #减速，加速度与速度成正比(-f*v)
        #v(t + t0) = -f*v(t)/m *t0 + v0,

        #获得摩擦系数
        #关于∆t的一系列计算
        f = float(main.frottement.get())
        t = self.temps/1000
        #计算出新的速度和分量
        self.vitesse = -f*self.vitesse/0.169*t + self.vitesse
        if self.vitesse < 0:
            self.vitesse = 0
        self.vitx = self.vitesse*math.cos(-self.angle)
        self.vity = self.vitesse*math.sin(-self.angle)

    def collision(self, boule2):
        #球和球之间
        if (self.flag) and (boule2.flag):
            pi = math.pi
            #防止碰撞一直被执行下去
            self.flag, boule2.flag = False, False

            if boule2.coordx != self.coordx:
                angle = math.atan(abs(boule2.coordy-self.coordy)/abs(boule2.coordx-self.coordx))
            else:
                angle = pi/2
            #在常规的标记上确定角度
            if boule2.coordx < self.coordx:
                angle = angle + pi/2
            if self.coordy < boule2.coordy:
                angle = -angle
            #如果两个球都在运动的情况下
            vitesse = math.sqrt(self.vitx**2+self.vity**2)
            #2号球
            boule2.vitesse = math.cos( abs( abs(angle)-abs(self.angle) ) )*vitesse
            boule2.angle = angle
            #1号球
            self.vitesse = math.sqrt( abs(self.vitesse**2-boule2.vitesse**2) )
            #碰撞过后的方向
            if (math.cos(self.angle) < 0):
                if(math.cos(boule2.angle + pi/2) < 0):
                        self.angle = boule2.angle + pi/2
                else:
                        self.angle = boule2.angle - pi/2
            else:
                if(math.cos(boule2.angle + pi/2) > 0):
                        self.angle = boule2.angle + pi/2
                else:
                        self.angle = boule2.angle - pi/2
        #管理flags
        if  math.sqrt((self.coordx - boule2.coordx)**2 + (self.coordy - boule2.coordy)**2) >= 30:
            self.flag, boule2.flag = True, True


    def deplacement(self, event):
        #把球的位置移到点击的坐标上
        #...除非和另一个球重合
        voixlibre = True
        for k in range(len(main.Boules)):
            if (main.Boules[k].couleur != self.couleur) and\
            ( math.sqrt((event.x-15 - main.Boules[k].coordx)**2 + (event.y-15 - main.Boules[k].coordy)**2) <= 30 ):
                voixlibre = False
        if voixlibre:
            self.coordx = event.x - 15
            self.coordy = event.y - 15






class Simu:
    def __init__(self, dim, temps):
        #台球的桌子
        self.terrain = Table(dim[0], dim[1])
        #在这里500px等于1m
        self.metre = 500
        #两个图像之间的帧率
        self.temps = temps

        #球
        self.Alpha = Ball(self.terrain.fenetre, self.terrain.canvas,
                     250, 250, dim[0], dim[1], self.metre, self.temps, 'red')
        self.Beta = Ball(self.terrain.fenetre, self.terrain.canvas,
                     750, 30, dim[0], dim[1], self.metre, self.temps, 'yellow')
        self.Gamma = Ball(self.terrain.fenetre, self.terrain.canvas,
                     750, 440, dim[0], dim[1], self.metre, self.temps, 'white')
        self.Boules = [self.Alpha, self.Beta, self.Gamma]

        #输入速度值
        self.label = Label(self.terrain.fenetre, text="速度(in dm/s):")
        self.label.pack(side=LEFT)
        self.vitesse = Scale(self.terrain.fenetre, from_=0, to=50,  orient=HORIZONTAL)
        self.vitesse.set(25)
        self.vitesse.pack(side=LEFT)

        #摩擦的类型
        self.label = Label(self.terrain.fenetre, text="\t 摩擦定律:")
        self.label.pack(side=LEFT)

        self.loi = StringVar(self.terrain.fenetre)
        self.loi.set("库伦法")
        self.choix = OptionMenu(self.terrain.fenetre, self.loi, "与压力成正比", "-k*v")
        self.choix.pack(side=LEFT)

        #Input frottement
        self.label = Label(self.terrain.fenetre, text="\t 摩擦系数:")
        self.label.pack(side=LEFT)
        self.frottement = Spinbox(self.terrain.fenetre, width=8, value=0.1875)
        self.frottement.pack(side=LEFT)

        #Positions souris
        self.posx = Label(self.terrain.fenetre, text="\t X(m):")
        self.posx.pack(side=LEFT)
        self.posy = Label(self.terrain.fenetre, text="; Y(m):")
        self.posy.pack(side=LEFT)

    def switch(self, event):
        #改变球
        for k in range(0, len(self.Boules)):
            if self.Boules[k].focus:
                self.Boules[k].focus = False
                self.Boules[k-1].focus = True
                break

    def quivise(self, event):
        #确定这是哪一个球
        for k in range(len(self.Boules)):
            if self.Boules[k].focus:
                self.Boules[k].viser(event)
        #显示指针位置
        self.posx.config(text='\t X: '+str(event.x/self.metre) )
        self.posy.config(text='; Y: '+str(event.y/self.metre) )

    def tirdroit(self, event):
        #0 角度
        for k in range(len(self.Boules)):
            self.Boules[k].theta = 0
        self.tir(event)

    def tir(self, event):
        #按照显示速度射击
        for k in range(len(self.Boules)):
            if self.Boules[k].focus:
                self.Boules[k].tirer(float(self.vitesse.get()))

    def savedata(self, event):
        #将速度和位置文件保存为一个*.csv .
        filename = tkFileDialog.asksaveasfilename(defaultextension='*.csv', filetypes=[('supported', ('*.csv'))])
        with open(filename, 'w', newline='') as fichier:
            file = csv.writer(fichier)
            file.writerow(["Temps [s]", "Xred [m]", "Yred [m]", "Xjaune [m]", "Yjaune [m]", "Xblanc [m]", "Yblanc [m]",
            "Vred [dm/s]", "Vjaune [dm/s]", "Vblanc [dm/s]",
            "Dir(red) [rad]", "Dir(jaune) [rad]", "Dir(blanc) [rad]"])
            t = self.temps/1000
            for k in range(len(self.Alpha.savit)):
                file.writerow([ str(round(k*t, 3)), str(round(self.Alpha.savex[k]/self.metre, 3)), str(round(self.Alpha.savey[k]/self.metre, 3)),
                str(round(self.Beta.savex[k]/self.metre, 3)), str(round(self.Beta.savey[k]/self.metre, 3)),
                str(round(self.Gamma.savex[k]/self.metre, 3)), str(round(self.Gamma.savey[k]/self.metre, 3)),
                str(round(self.Alpha.savit[k], 3)), str(round(self.Beta.savit[k], 3)), str(round(self.Gamma.savit[k], 3)),
                str(round(self.Alpha.sava[k], 3)), str(round(self.Beta.sava[k], 1)), str(round(self.Gamma.sava[k], 1)) ])

    def lancer(self):
        #默认控制红球
        self.Alpha.focus = True

        """Evènements"""
        #左键改变红球位置
        self.terrain.canvas.bind('<Button-1>', self.Alpha.deplacement)
        #中间键改变白球位置
        self.terrain.canvas.bind('<Button-2>', self.Beta.deplacement)
        #右键改变黄球位置
        self.terrain.canvas.bind('<Button-3>', self.Gamma.deplacement)
        #鼠标的运动等于方向
        self.terrain.canvas.bind('<Motion>', self.quivise)
        #用ctrl键切换球
        self.terrain.fenetre.bind('<Control_R>', self.switch)
        #Enter键射击
        self.terrain.fenetre.bind('<Return>', self.tir)
        #space
        self.terrain.fenetre.bind('<space>', self.tirdroit)
        #大写键save
        self.terrain.fenetre.bind('<Control-s>', self.savedata)
        self.terrain.fenetre.bind('<Control-S>', self.savedata)

        #循环
        self.boucle()
        #显示
        self.terrain.afficher()

    def boucle(self):
        #球的运动
        for k in range(len(self.Boules)):
            self.Boules[k].move()
        #球是否处于禁止状态
        sigma = 0
        for k in range(len(self.Boules)):
            sigma += self.Boules[k].vitesse
        #...如果没有就记录数据
        for k in range(len(self.Boules)):
            if sigma:
                #位置
                self.Boules[k].savex.append(self.Boules[k].coordx)
                self.Boules[k].savey.append(self.Boules[k].coordy)
                #速度
                self.Boules[k].savit.append(self.Boules[k].vitesse/self.metre*10)
                #角度
                self.Boules[k].sava.append(self.Boules[k].angle)
            if sigma and self.Boules[k].vitesse:
                #轨道的标记
                self.Boules[k].save.append(self.Boules[k].canvas.create_oval(self.Boules[k].coordx+13,
                self.Boules[k].coordy+13, self.Boules[k].coordx+17, self.Boules[k].coordy+17, width=0, fill=self.Boules[k].couleur))
        #自我循环
        self.terrain.fenetre.after(self.temps, self.boucle)


if __name__ == '__main__':
    #模拟循环
    #可以改变场地的大小(长*宽, in px) 以及图像的更新率 因此改变准确度 (in ms).
    #台球桌的大小是2*1.6
    main = Simu([1000, 500], 10)
    main.lancer()























