# -*- coding: cp936 -*-
import pygame,sys,math,random,os

# Define some colors 定义一些颜色
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue2    = (   0, 191, 255)
blue3    = ( 176, 224, 230,120)
blue4    = ( 175, 238, 238,120)
blue1    = (   0, 255, 255,120)
yellow   = ( 255, 255, 0  )
#初始化pygame
pygame.init()
#为了xp下的兼容性做以下设置
os.environ['SDL_VIDEODRIVER']='windib'

# Set the width and height of the screen [width,height]
lst_size=[800,600]
screen=pygame.display.set_mode(lst_size,pygame.HWSURFACE|pygame.DOUBLEBUF,0)


pygame.display.set_caption("Super Ship")

#Loop until the user clicks the close button.
b_done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()
fps=35
#__set music and sound______设置一些音乐和音效______________________________

pygame.mixer.music.load('background.mp3')

sound_daodan=pygame.mixer.Sound('daodan2.wav')
sound_mechinegun=pygame.mixer.Sound('mechinegun.wav')
sound_jiguang=pygame.mixer.Sound('jiguang.wav')
sound_thunder=pygame.mixer.Sound('thunder.wav')
#设置一些字体        
font2= pygame.font.Font(None, 72)
font = pygame.font.Font(None, 36)
text_wait=font.render('loading.....',True,blue1)
#screen.blit(text_wait,[lst_size[0]/2-50,lst_size[1]/2-20])

#Design back ground____设计背景____________________________________________
class Background(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    
#让背景动起来的函数
def animateBackground(p):
    for background in bg_list:
        if  -1950<background.x<lst_size[0]+30:
           screen.blit(background.img, (background.x, background.y)) #BG 1
        if background.x<=-1950:
            background.x+=20*1920
        background.x -= p

    
#_____________________________________________________________________





#Design your ship____设计玩家飞机_________________________________________________
class Player(object):
    def __init__(self,x,y,img,a,b,hp):
        self.x=x
        self.y=y
        self.img=img
        self.change_x=a
        self.change_y=b
        self.hp=hp
#设计一些要用到的变量        
livemax=4
live=3
level=0        
exp=0
lastlooplevel=0
sp=0
live_img= pygame.image.load('live.png').convert_alpha()
#设计剩余生命值个数的图像
def liveleft():
    global live
    for i in range(live-1):
        screen.blit(live_img, (i*55+300, 10)) 
        
#在玩家类中创造一个玩家
ship=pygame.image.load('player.png').convert_alpha()
player=Player(300,300,ship,0,0,500)



#______________________________________________________________________
#设置开始画面的几张图像
plane_img= pygame.image.load('plane.jpg').convert()
compiler_img = pygame.image.load('jia.jpg').convert()



#set bullet class___________________________________________________________
class Bullet(pygame.sprite.Sprite):
    def __init__(self,color,speed,filename,kill,direction):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 

        # Create an image of the Bullet,
       
        self.image = pygame.image.load(filename).convert_alpha()
        self.image.set_colorkey(black)

        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.speed=speed
        self.kill=kill
        self.direction=direction
#子弹列表       
bulletlist=pygame.sprite.RenderPlain()
#添加子弹的函数（一次两枚）
def addbullet():
        bull=Bullet(white,20,'bl.png',30+level_bullet*20,0)
        bull.rect.x=player.x+128
        bull.rect.y=player.y+12
        bulletlist.add(bull)
        bull=Bullet(white,20,'bl.png',30+level_bullet*20,0)
        bull.rect.x=player.x+128
        bull.rect.y=player.y+76
        bulletlist.add(bull)
        
    

    


#design enemy__定义敌人类________________________________________________________       
class Enemy(pygame.sprite.Sprite):
    
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, filename,hp):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        # Create an image of the Enemy,
        self.image = pygame.image.load(filename).convert_alpha()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.hp=hp
        self.clock=random.randrange(1,100)
        self.hpmax=hp
        self.explo=0

#创建精灵组
presentlist=pygame.sprite.RenderPlain()

#level 0 for 8 enemy 初始化敌人

#添加敌人的函数
def Enemylist(x):
    if x<30:
        for i in range(8*x,min(9*x+7,8*x+15)):
            enem=enemylist[i]
            if not (enem in presentlist) :
                enem.hp=enem.hpmax
                enem.rect.x=random.randint(lst_size[0],3000)
                enem.rect.y=random.randint(0,lst_size[1]-128)
            presentlist.add(enem)
    if x>=30:
        for i in range (300):
            enem=enemylist[i]
            if not (enem in presentlist) :
                enem.hp=enem.hpmax
                enem.rect.x=random.randint(lst_size[0],3000)
                enem.rect.y=random.randint(0,lst_size[1]-128)
            presentlist.add(enem)
        
    


#set enemy bullet创建子弹精灵组________________________________________________
enemybulletlist=pygame.sprite.RenderPlain()
#创建敌人发射子弹的过程
def addenemybullet1():
   bull=Bullet(white,-10,'bullet.png',5,0)
   bull.rect.x=enem.rect.x+5
   bull.rect.y=enem.rect.y+64
   enemybulletlist.add(bull)
   bull=Bullet(white,-10,'bullet.png',5,5)
   bull.rect.x=enem.rect.x+5
   bull.rect.y=enem.rect.y+64
   enemybulletlist.add(bull)
   bull=Bullet(white,-10,'bullet.png',5,-5)
   bull.rect.x=enem.rect.x+5
   bull.rect.y=enem.rect.y+64
   enemybulletlist.add(bull)


    
    
#set enemy hp line_画出敌人hp线____________________________________________________
def drawhpline():
    for enem in presentlist:
        #创造矩形，边框为红线
        pygame.draw.rect(screen,blue1,[enem.rect.x+3,enem.rect.y,128,5],1)
        #计算血量
        linelong=int(enem.hp/float(enem.hpmax)*128)
        #画出血条
        s=pygame.Surface((max(linelong,0),5))
        #设置透明度
        s.set_alpha(150)
        #填充颜色
        s.fill(red)
        screen.blit(s,(enem.rect.x+3,enem.rect.y))


#________________________________________________________________________       


#激光炮第一阶段效果与变量___
#定义并初始化一些要用到值  _________________________________________________________
jiguangbool=False
jiguangclock=0
jiguangfa=0
hurts=0
def jiguang():
    global jiguangclock
    global hurts
    #每次运行，激光clock+1，并画出半径减小的圆来展示蓄力效果
    if jiguangclock > 0 and jiguangclock < 26:

        r=130-5*jiguangclock
        pygame.draw.circle(screen,blue1,[player.x+64,player.y+64],r,(jiguangclock/8)+1)

        pygame.draw.circle(screen,blue4,[player.x+135,player.y+64],r+13,(jiguangclock/8)*3+3)

        jiguangclock+=1

    #激光clock+1，蓄力能量球不断扩大，没有上限 
    if jiguangclock > 25 :

        pygame.draw.line(screen,blue4,[player.x+64,player.y+64],[player.x+135,player.y+64],3)
        
        pygame.draw.circle(screen,blue4,[player.x+64,player.y+64],7)
        pygame.draw.circle(screen,blue4,[player.x+135,player.y+64],jiguangclock-3)

        jiguangclock+=1

re=0
f=0
#当蓄力完成后，展示发射效果    
def jiguangfashe():
    global jiguangfa
    global hurts
    global jiguangclock
    global re
    global f
    global jiguangbool
    if jiguangclock > 0:
        hurts=jiguangclock    #将clock值赋予成伤害值（蓄力时间越久，伤害越大）
        re=hurts            #将clock值赋予半径值（蓄力时间越久，激光半径越大）
            
    if jiguangfa == 1 :
        #J键被放开时，此段程序执行
        #若蓄力时间不够，（<27)，那么关掉激光发射器
        if hurts < 27:
            jiguangbool=False
            jiguangfa=0
        #当蓄力时间够时  画出能量球与激光 
        if hurts > 26 and re >= 1 :
            #画出能量球1
            
            pygame.draw.circle(screen,blue1,[player.x+64,player.y+64],7)

            #画出激光
            s=pygame.Surface((lst_size[0],2*re))
            s.set_alpha(130)
            s.fill(blue4)
            screen.blit(s,(player.x+128+re,player.y+64-re))
            sound_jiguang.play()
            #画出能量球2
            pygame.draw.circle(screen,blue4,[player.x+128+re,player.y+64],re)
            pygame.draw.line(screen,blue4,[player.x+64,player.y+64],[player.x+135,player.y+64],3)

            #每执行一次半径减少2
            re-=2
        #半径过小时关掉激光发射器    
        if re<1:
            jiguangfa=0
            jiguangbool=False
#________________________________________________________________________________________________







#set Machine gun___设置机关枪_________________________________________________________
Machinebool=False
Machineclock=0

def Machinegun():
    global Machineclock
    global Machinebool
    #当使用机关枪技能时，根据等级的不同会赋予Machineclock 不同的正值，来调节机关枪的发射过程时间。
    #每运行一次下列代码，Machineclock-1
    if Machineclock > 0:
        Machinebool == True
        if Machineclock == 1:
            #当Machineclock减到一时关掉机关枪
            Machinebool = False
        #每运行一次代码，Machineclock-1    
        Machineclock-=1
        #设置子弹，调用子弹类
        bull1=Bullet(white,20,'bl2.png',3+level_machine*2,0)
        bull2=Bullet(white,20,'bl2.png',3+level_machine*3,0)
        bull3=Bullet(white,20,'bl2.png',3+level_machine*3,0)
        bull4=Bullet(white,20,'bl2.png',3+level_machine*3,0)
        bull5=Bullet(white,20,'bl2.png',3+level_machine*2,0)
        #设置子弹位置与发射时间
        if Machineclock%4 == 1:
            bull1.rect.x=player.x+128
            bull1.rect.y=player.y+30

            bull2.rect.x=player.x+128
            bull2.rect.y=player.y+44

            bull3.rect.x=player.x+128
            bull3.rect.y=player.y+58

            bull4.rect.x=player.x+128
            bull4.rect.y=player.y+72

            bull5.rect.x=player.x+128
            bull5.rect.y=player.y+86
            bulletlist.add(bull1,bull2,bull3,bull4,bull5)
        if Machineclock % 4 == 3 :
            bull1.rect.x=player.x+128
            bull1.rect.y=player.y+37

            bull2.rect.x=player.x+128
            bull2.rect.y=player.y+51

            bull3.rect.x=player.x+128
            bull3.rect.y=player.y+65

            bull4.rect.x=player.x+128
            bull4.rect.y=player.y+79
            bulletlist.add(bull1,bull2,bull3,bull4)
        sound_mechinegun.play()   

#________set  clock for skill____________________________-_-__
#设置技能冷却的雷达扫描效果          
def redar(fulltime,xx,yy,cding):
    #xx,yy,为雷达中心位置，fulltime为总时间，cding时当前技能冷却时间
    angle=(float(cding)/fulltime)*2*math.pi
    #计算雷达指针断电的位置
    x=int(25*math.sin(angle)+xx)
    y=int(25*math.cos(angle)+yy)
    #画出效果
    pygame.draw.line(screen,black,[xx,yy],[x,y],2)
 
#___set icon of skill______________________________________
#设置技能图片在右下角画出            
def icon():
    global jiguangbool,jiguangcd,Machinebool,Machinecd
    #把技能图片画出来
    screen.blit(icon1, (800,lst_size[1]-65))
    screen.blit(icon2, (855,lst_size[1]-65))
    screen.blit(icon3, (910,lst_size[1]-65))
    screen.blit(icon4, (965,lst_size[1]-65))
    screen.blit(icon5, (1020,lst_size[1]-65))
    screen.blit(icon6, (1075,lst_size[1]-65))
    #设置透明矩形，显示技能正在冷却
    s1=pygame.Surface((50,50))
    s1.set_alpha(150)
    s1.fill(blue1)
    #将雷达位置放在每个技能图片上，调用redar（）
    if jiguangbool==True or Machinebool== True:
        screen.blit(s1,(855,lst_size[1]-65))
        screen.blit(s1,(910,lst_size[1]-65))
    if jiguangcd > 0 :
        screen.blit(s1,(855,lst_size[1]-65))
        redar(jiguangcdmax,855+25,lst_size[1]-65+25,jiguangcd)
    if Machinecd > 0:
        screen.blit(s1,(910,lst_size[1]-65))
        redar(Machinecdmax,910+25,lst_size[1]-65+25,Machinecd)
    if Snowcd>0:
        screen.blit(s1,(965,lst_size[1]-65))
        redar(Snowcdmax,965+25,lst_size[1]-65+25,Snowcd)
    if fixcd>0:
        screen.blit(s1,(1020,lst_size[1]-65))
        redar(fixcdmax,1020+25,lst_size[1]-65+25,fixcd)
    if thundercd>0:
        screen.blit(s1,(1075,lst_size[1]-65))
        redar(thundercdmax,1075+25,lst_size[1]-65+25,thundercd)    

#计数器injury,被击中后全屏红
jishu_injury=0            
#set effect of injury___________________________________
def injury():
    global jishu_injury
    injury_rect=pygame.Surface(lst_size)
    #当被击中后，将赋予jishu_injury为1
    if jishu_injury > 0:
        x=jishu_injury
        #透明度成计数器的二次函数
        injury_rect.set_alpha(int((16*x-x*x)*2))
        #每次技术器值+1
        jishu_injury+=1
        injury_rect.fill(red)
        screen.blit(injury_rect,(0,0))
    #当计数器达到16时，计数器重回到0
    if jishu_injury == 16:
        jishu_injury=0
    
    

#设置技能飘雪的效果
Snowclock=0
#当飘雪技能被触发时，根据等级赋予Snowclock大于0的值，以此调节技能时间
def snow():
    global fps
    global Snowclock
    global player_speed
    global skip
    Snow_rect=pygame.Surface(lst_size)
    #全屏发白
    if Snowclock > 0:
        x=Snowclock
        Snow_rect.set_alpha(min(50,Snowclock))
        Snow_rect.fill(white)
        screen.blit(Snow_rect,(0,0))
    #调节屏闪频率，我机速度变快
    if Snowclock > 1:
        Snowclock-=1
        fps=25-level_snow
        player_speed=18
        snoweffect()
    #snowclock为1时，让效果恢复正常    
    if Snowclock ==1:
        Snowclock-=1
        fps=35
        player_speed=11
#设置雪花列表，以此展示飘雪效果        
snowlist=[]
snow_img=pygame.image.load('Snow.png').convert_alpha()
#制作雪花列表
def makelist():
    for i in range(100):
        x=random.randrange(-5,lst_size[0])
        y=random.randrange(-5,lst_size[1])
        snowlist.append([x,y])
        
#让雪花飘        
def snoweffect():
    for i in range(len(snowlist)):
        screen.blit(snow_img, snowlist[i])
        snowlist[i][1]+=2
        #若雪花飘出屏幕，则重新设置位置
        if snowlist[i][1] > lst_size[1]:
            y=random.randrange(-725,-5)
            snowlist[i][1]=y
            x=random.randrange(-5,lst_size[0])
            snowlist[i][0]=x
#设置自我修复效果，工作原理和雪花，机关枪相同，

            
fixclock=0                        
def Fix():
    global fixclock
    if fixclock > 0 and live_==True:
        fixclock-=1
        #没1/3秒加一次血，血量由level_fix调节
        if fixclock%12==0:
            player.hp=min(player.hp+1.7+level_fix/4.0,hpmax)
        #画一个透明矩形来展示加血效果    
        screen.blit(lst_fix[(fixclock%22)/2],(player.x-110,player.y-110))






#设置雷电效果        
thunderclock=0        
def Thunder():
    global thunderclock
    if thunderclock > 0 :
        thunderclock-=1
        for enem in presentlist:
            if presentlist != []:
                screen.blit(lst_thunder[17-thunderclock/2],[enem.rect.x-186,enem.rect.y-550])
                if enem.rect.x<lst_size[0] and enem.rect.x>-128:
                    enem.hp-=4+level_thunder*4
                    if thunderclock == 0:
                        enem.hp-=level_thunder*500
                
    
#设置升级效果                
levelclock=0
#引入一系列图片，造成动画效果

def levelup():
    global levelclock
    if levelclock > 0:
        levelclock-=1
        screen.blit(lst_level[13-levelclock/2],[player.x-111,player.y-111])
        if levelclock==1 and live_==True:
            player.hp=min(hpmax,player.hp+200)

#设置gameover()效果
def gameover():
    global Bool_gameover
    text_gameover=font2.render("GAME OVER !",True,white)
    #打出一行字
    screen.blit(text_gameover,[450,350])
    text_gameover=font2.render("Try again ?",True,white)
    #打出一行字
    screen.blit(text_gameover,[450,420])
    Bool_gameover=True
#设置button类
class button :
    def __init__(self,p1,p2,color,alpha,string,s_color):
        self.p1=p1
        self.p2=p2
        self.color=color
        self.alpha=alpha
        self.rect=pygame.Surface([abs(p1[0]-p2[0]),abs(p1[1]-p2[1])])
        self.rect.set_alpha(alpha)
        self.rect.fill(color)
        self.string=font2.render(string,True,s_color)                        
    def draw(self):
        screen.blit(self.rect,self.p1)
        screen.blit(self.string,[self.p1[0]+10,self.p1[1]+20])
    
    def click(self):
        a= pygame.mouse.get_pos()
        if abs(a[0]-self.p1[0])+abs(a[0]-self.p2[0])== abs(self.p1[0]-self.p2[0]) and\
           abs(a[1]-self.p1[1])+abs(a[1]-self.p2[1])== abs(self.p1[1]-self.p2[1]):
            return True
        else :
            return False
#定义若干个button
button_start=button([500,500],[700,580],yellow,150,'  Start  ',red)        
button_quit=button([500,600],[700,680],yellow,150,'  quit  ',red)
button_Y=button([400,490],[450,560],yellow,120,'Y',red)
button_N=button([480,490],[530,560],yellow,120,'N',red)
button_x=button([lst_size[0]-20,0],[lst_size[0],20],blue1,120,' ',black)


def relive():
    global relive_clock
    a=relive_clock-35
    if 0<=a<25 :
        screen.blit(lst_relive[a/2],[player.x-110,player.y-110])
    


#定义一些变量
relive_clock=0            
wudi=False
#冷却变量
bulletcd=0
Machinecd=0
jiguangcd=0
Snowcd=0
player_speed=11
thundercd=0   
fixcd=0
#键开关变量                
Key_a=False
Key_s=False
Key_d=False
Key_w=False
#技能等级变量
level_bullet=1
level_machine=1
level_jiguang=1
level_snow=1
level_fix=1
level_thunder=1
#其他变量
stage=0
global_time=1
#游戏进行阶段变量
live_=True
Bool_gameover=True
Bool_gamestart=False
hpmax=level*200+500
loading=True
pygame.mixer.music.play(-1)
# -------- Main Program Loop -----------
while b_done==False:
  if loading==True:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            b_done=True
    screen.fill(white)
    lst_text_compiler=['Author: Dongyu Jia.','SJTU' , 'GRADE ONE','F1203022        5120309607' , '2012     Autumn','All rights reserved','Please wait.....']
    t_jishu=0
    for t in lst_text_compiler:
        text_compiler=font2.render(t,True,black)
        screen.blit(text_compiler,[160,150+t_jishu])
        t_jishu+=68
    pygame.display.update()
    #制作背景列表以及各种列表
    bg_list=[]
    for i in range(20):    
        bg=pygame.image.load('bgfile/'+str(i+1)+'.jpg').convert()
        background=Background(1920*i,-200,bg)
        bg_list.append(background)
    lst_thunder=[]
    for i in range(18):
        order=str(i+1)+'.png'
        thunder_img=pygame.image.load('thunder/'+order).convert_alpha()
        lst_thunder.append(thunder_img)
    lst_level=[]
    for i in range(14):
        order=str(i+1)+'.png'
        level_img=pygame.image.load('levelup/'+order).convert_alpha()
        lst_level.append(level_img)
    makelist()
    icon1 = pygame.image.load('1.jpg').convert()
    icon2 = pygame.image.load('icon2.jpg').convert()
    icon3 = pygame.image.load('icon3.jpg').convert()
    icon4 = pygame.image.load('icon4.jpg').convert()
    icon5 = pygame.image.load('fix.jpg').convert()
    icon6 = pygame.image.load('thunder.png').convert()
    bg2=pygame.image.load('bg2.gif').convert()
    bg2=pygame.transform.scale(bg2,(lst_size[0],195))
    lst_explo=[]
    for i in range(16):
        order=str(i+1)+'.png'
        explo_img=pygame.image.load('explosive/'+order).convert_alpha()
        lst_explo.append(explo_img)
    #创建敌人列表，并填充列表        
    enemylist=[]
    for i in range(100):
        e=Enemy(black,'en'+str(i%8+1)+'.png',100+i*20)
        enemylist.append(e)
    for i in range(100):
        e=Enemy(black,'en'+str(i%10+1)+'.png',2000+i*50)
        enemylist.append(e)
    for i in range(100):
        e=Enemy(black,'en'+str(i%6+7)+'.png',7000+i*100)
        enemylist.append(e)
        loading=False
    for i in range(8):
        # This represents a enemy
        enem=enemylist[i]
        # Set a random location for the enemy
        enem.rect.x=random.randint(lst_size[0],3000)
        enem.rect.y=random.randint(0,lst_size[1]-128)
        presentlist.add(enem)
    lst_fix=[]
    for i in range(11):
        order='fix/'+str(i+1)+'.png'  
        a=pygame.image.load(order).convert_alpha()
        lst_fix.append(a)
    lst_relive=[]    
    for i in range(13):
        order='relive/'+str(i+1)+'.png'
        a=pygame.image.load(order).convert_alpha()
        lst_relive.append(a)
#加载完毕后进入游戏入口        
  if  Bool_gamestart==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            b_done=True
        #点击开始即可运行
        if event.type == pygame.MOUSEBUTTONDOWN :
            if button_start.click():
                Bool_gamestart=True
                Bool_gameover =False
            #点击退出即退出    
            if button_quit.click():
                b_done=True
    #设置背景 text button        
    text_compiler=font.render('Author: Dongyu Jia',True,blue1)
    animateBackground(50)
    screen.blit(plane_img, (600, 100))
    screen.blit(compiler_img,[130,50])
    screen.blit(text_compiler,[160,450])
    text_tip =font.render('Click with mouse on start!',True,blue1)
    screen.blit(text_tip,[160,550])
    button_start.draw()
    button_quit.draw()
    #每秒刷新
    pygame.display.update()
    clock.tick(fps)
  #游戏结束效果  
  if Bool_gamestart==True and Bool_gameover==True :      
    for event in pygame.event.get():
        #交互
        if event.type == pygame.QUIT: # If user clicked close
            b_done=True
        if event.type == pygame.MOUSEBUTTONDOWN :
            if button_x.click():
                b_done=True
            if button_Y.click():
                #初始化游戏参数
                Bool_gamestart = False
                Bool_gameover = False
                relive_clock=0            
                wudi=False
                Key_a=False
                Key_s=False
                Key_d=False
                Key_w=False
                level_bullet=1
                level_machine=1
                level_jiguang=1
                level_snow=1
                level_fix=1
                level_thunder=1
                stage=0
                global_time=1
                live_=True
                jiguangbool=False
                jiguangclock=0
                jiguangfa=0
                hurts=0
                bulletcd=0
                Machinecd=0
                jiguangcd=0
                Snowcd=0
                player_speed=11
                thundercd=0  
                fixcd=0
                #初始化游戏列表
                for enem in enemylist:
                    enem.hp=enem.hpmax
                for enem in presentlist:
                    presentlist.remove(enem)
                    enem.hp=enem.hpmax
                for i in range(8):
                    enem=enemylist[i]
                    enem.rect.x=random.randint(lst_size[0],3000)
                    enem.rect.y=random.randint(0,lst_size[1]-128)
                    presentlist.add(enem)
                player=Player(300,300,ship,0,0,500)
                level=0        
                exp=0
                lastlooplevel=0
                sp=0
                live=3
                hpmax=level*200+500
                player.hp=hpmax
# -------- 
            if button_N.click():
                b_done=True
    #设置若干背景 button 。。。            
    animateBackground(3)  
    gameover()
    button_x.draw()
    button_Y.draw()
    button_N.draw()
    pygame.display.update()
    clock.tick(fps) 
  if  Bool_gamestart==True and Bool_gameover == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    #交互
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            b_done=True # Flag that we are b_done so we exit this loop
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
        if event.type == pygame.MOUSEBUTTONDOWN :
            if button_x.click():
                b_done=True
        #键盘交互及数据传输
        if event.type == pygame.KEYDOWN :
            #前后左右移动
            if event.key == pygame.K_a:
                Key_a=True
            if event.key == pygame.K_d:
                Key_d=True
            if event.key == pygame.K_w:
                Key_w=True
            if event.key == pygame.K_s:
                Key_s=True
            #设定技能冷却时间，技能开关    
            if event.key == pygame.K_j and Machinebool==False and jiguangcd<0:
                jiguangclock = 1
                jiguangfa=0
                jiguangbool=True
                jiguangcd=200
                jiguangcdmax=200
            #设定技能冷却时间，技能开关     
            if event.key == pygame.K_k and bulletcd<=0:
                sound_daodan.play()
                addbullet()
                bulletcd=30
             #设定技能冷却时间，技能开关    
            if event.key == pygame.K_l and jiguangbool==False and Machinecd < 0 :
                Machineclock=10+15*level_machine
                Machinecd=170+15*level_machine
                Machinecdmax=170+15*level_machine
                #设定技能冷却时间，技能开关 
            if event.key == pygame.K_u and Snowcd < 0:
                Snowclock=35*8+35*level_snow*2
                Snowcd=Snowclock*2
                Snowcdmax=Snowclock*2
                #设定技能冷却时间，技能开关 
            if event.key == pygame.K_i and fixcd < 0:
                fixclock=35*30+level_fix*35*10
                fixcd=35*30*2+level_fix*35*10
                fixcdmax=35*30*2+level_fix*35*9
                #设定技能冷却时间，技能开关 
            if event.key == pygame.K_o and thundercd<0:
                thunderclock=36
                thundercd=1800
                thundercdmax=1800
                sound_thunder.play()
                #设定技能升级 
            if event.key ==pygame.K_1 and sp>0:
                level_bullet+=1
                sp-=1
                #设定技能升级 
            if event.key ==pygame.K_2 and sp>0:
                level_jiguang+=1
                sp-=1
                #设定技能升级 
            if event.key ==pygame.K_3 and sp>0:
                level_machine+=1
                sp-=1
                #设定技能升级 
            if event.key ==pygame.K_4 and sp>0:
                level_snow+=1
                sp-=1
                #设定技能升级 
            if event.key ==pygame.K_5 and sp>0:
                level_fix+=1
                sp-=1
                #设定技能升级 
            if event.key ==pygame.K_6 and sp>0:
                level_thunder+=1
                sp-=1    
         #  if event.type == pygame.MOUSEBUTTONDOWN:   
                
                

        
        # 交互   
        # 设置前后左右开关
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_a :
                Key_a=False
            if event.key == pygame.K_d :
                Key_d=False
            if event.key == pygame.K_w :
                Key_w=False
            if event.key == pygame.K_s :
                Key_s=False
                #设置激光发射效果
            if event.key == pygame.K_j :
                
                jiguangclock = 0
                jiguangfa = 1
                
    #当键按下时，对应速度改变           
    if Key_a==True :
        player.x-=player_speed
    if Key_d==True :
        player.x+=player_speed
    if Key_s==True :
        player.y+=player_speed
    if Key_w==True :
        player.y-=player_speed        

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    #设置“墙”
    #_set_side______________________________________
    if player.x<0:
        player.x+=player_speed
    if player.x>lst_size[0]-128:
        player.x-=player_speed
    if player.y<0:
        player.y+=player_speed
    if player.y>lst_size[1]-128-80:
        player.y-=player_speed
    #_________________________________________________
    #定义最大血量    
    hpmax=level*200+500
    #设置敌人的运动方式（根据自身位置及相对玩家位置判断行进方式）
    #set enemy_how to go___________________________________________
    for enem in presentlist:
        if (enem.rect.x>player.x+150 or enem.rect.x<player.x-120 ) and enem.rect.x<1100:
            enem.rect.x-=7
            if enem.rect.y<1:
                enem.rect.y+=2
            elif enem.rect.y>lst_size[1]-128:
                enem.rect.y-=2
            else:
                if player.y-5>enem.rect.y:
                    enem.rect.y+=1
                elif player.y+5<enem.rect.y :
                    enem.rect.y-=1
                else :
                    enem.rect.y+=0
        elif enem.rect.x>player.x+84 and enem.rect.x<1100 :
            enem.rect.x-=4
            if player.y-5>enem.rect.y:
                enem.rect.y+=1
            elif player.y+5<enem.rect.y :
                enem.rect.y-=1
            else:
                enem.rect.y+=0
        elif enem.rect>=1100:
            enem.rect.x-=6
                
        else :
            if player.y>enem.rect.y :
                enem.rect.x-=5
                enem.rect.y+=2
            else:
                enem.rect.x-=5
                enem.rect.y-=2
        #敌人每次计数器加一（为发射子弹打前站）        
        enem.clock+=1        
    #_____________________________________________________________________

    #set position of enemy ,and make them hurt when hitted___________________________
    #设置敌人算法，相撞，发射子弹，被激光打到，出界的相关逻辑    
    jishu=0            
    for enem in presentlist:
        #设置敌人跑出屏幕的处理方案
        if enem.rect.x<-128:
            enem.rect.x=random.randint(lst_size[0],2300)
            enem.rect.y=576-(jishu %5)*130
            enem.hp=enem.hpmax
        #设置被激光照到的处理方法    
        if jiguangfa==1:
            if (enem.rect.y < player.y+re)and(enem.rect.y > player.y-re) and enem.rect.x<lst_size[0] and enem.rect.x>player.x:
                enem.hp-=2.3+3*level_jiguang
        #设置敌人死亡时效果        
        if enem.hp<=0:
            enem.explo=32
            presentlist.remove(enem)
            exp+=100+enem.hpmax/10
        #设置和玩家相撞的结果    
        if (abs(enem.rect.x-player.x)+abs(enem.rect.y-player.y)<100) and wudi==False:
            player.hp-=int(math.sqrt(abs(enem.hp))*10)
            enem.explo=32
            jishu_injury=1    
            presentlist.remove(enem)
        #设置发射子弹的效果    
        if enem.clock % 100 == 0 and enem.rect.x<1100 and enem.rect.x>player.x:
            addenemybullet1()
          
            
        #计数当前列表里有多少敌人        
        jishu=jishu+1
     #_________________________________________________________________________

    #判断玩家是否死亡，及死亡效果        
    #__whether alive_for player____________________________________________________________________
    if player.hp<=0 and live > 1:
        live_=False
        #复活效果（动画）
        if relive_clock==0:
            relive_clock+=1
            wudi=True
        elif relive_clock>=1 and relive_clock<35:
            relive_clock+=1
            player.hp=-1
            
        elif relive_clock >= 35 and relive_clock<70:
            player.hp=(-1)**(relive_clock/4)-1
            
            relive_clock+=1
        elif relive_clock==70:
            relive_clock=0
            player.hp=hpmax
            live-=1
            wudi=False
            live_=True
    #整体时间的设定与关卡的发展
    #_guanqiahua_______________________________________________
    if global_time % 1500 == 0 :
        #stage即为游戏关卡
        stage+=1
        Enemylist(stage)
        #当敌人被打光时自动进入下一阶段
    if not presentlist:#列表为空时执行
        stage+=1
        Enemylist(stage)
        global_time=((global_time/1800)+1)*1800


    
    #
    #启动机关枪（内置判断启动语句）
    Machinegun()
    #技能冻结时间减少1
    bulletcd-=1
    Machinecd-=1
    jiguangcd-=1
    Snowcd-=1
    fixcd-=1
    thundercd-=1
    #设置子弹的移动-与效果-
    for bul in bulletlist:
        #横向
        bul.rect.x+=bul.speed
        #纵向
        bul.rect.y+=bul.direction
        #子弹出屏的处理
        if bul.rect.x>lst_size[0]:
            bulletlist.remove(bul)
            #子弹撞到敌机的逻辑
        for enem in presentlist:
            if bul.rect.y<enem.rect.y+128 and enem.rect.y<bul.rect.y and bul.rect.x>enem.rect.x-16 and bul.rect.x<enem.rect.x+128-32:
                bulletlist.remove(bul)
                enem.hp-=bul.kill
                enem.rect.x+=10

    #设置敌人子弹的移动与效果
    for bul in enemybulletlist:
        bul.rect.x+=bul.speed#横向
        bul.rect.y+=bul.direction#纵向
        if bul.rect.x < -50:
            enemybulletlist.remove(bul)#子弹出屏的处理
            #子弹撞到我机的逻辑
        if bul.rect.y>player.y+5 and bul.rect.y < player.y+128-16-5 and bul.rect.x>player.x and bul.rect.x<player.x+115 and wudi==False:
            player.hp-=bul.kill
            enemybulletlist.remove(bul)
            #计数器启动，并引发全屏红的效果（在其他过程中有全屏红的过程，这里只做数据接口）
            jishu_injury=1


    #set level up logic__设置升级逻辑_____________________________
    expmax=level*150+100        
    if exp>expmax:
        exp-=expmax
        level+=1
        sp+=1
    #_set__hpline__设置血条_______________________________________________    
    
    hpline=int((player.hp/float(hpmax))*400)
        

    #升级的判定
    if lastlooplevel < level:
        #levelclock作为数据接口可导致升级动画
        levelclock=28
    #上一圈的等级记录（用于判断是否升级）    
    lastlooplevel=level
    

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT 画出应画的
    animateBackground(3)#背景
    
    
    #当玩家存活时应画出的效果
    if player.hp>-1:
        jiguang()
        snow()        
        jiguangfashe()
        injury()
        Fix()
        Thunder()
        screen.blit(player.img,(player.x,player.y))
    #无论玩家是否存活时应画出的效果
    liveleft()
    presentlist.draw(screen)
    bulletlist.draw(screen)    
    relive()    
    drawhpline()    
    #一些额外的背景
    screen.blit(bg2,[0,lst_size[1]-80])
    #画出图标
    icon()
    #set some parameters_设置一些_字符并画出来___________________________
    textlevel=font.render("Level:"+str(level),True,blue1)
    textsp=font.render('sp:'+str(sp),True,blue1)
    textexp=font.render("Exp:   "+str(exp)+'/'+str(expmax),True,white)
    texthp=font.render("HP:   "+str(int(max(0,player.hp)))+'/'+str(hpmax),True,white)
    textlevel_sp=font.render(str(level_bullet)+'      '+str(level_jiguang)+'      '+str(level_machine)+'      '+str(level_snow)+'      '+str(level_fix)+'      '+str(level_thunder),True,red)
    textx=font.render('x',True,white)
    #把关闭按钮画出来
    button_x.draw()
    screen.blit(textx,[lst_size[0]-20,-5])
    #move作为调整下面图形位置的统一调用数据，通过改变move使图形绝对位置改变，相对位置不变）
    move=150
    pygame.draw.rect(screen,red,[40+move,lst_size[1]-40,400,25],2)
    pygame.draw.rect(screen,red,[40+move,lst_size[1]-40,hpline,25])
    screen.blit(texthp,[160+move,lst_size[1]-36])
    screen.blit(textlevel,[620,lst_size[1]-73])
    expline=int((exp/float(expmax))*400)
    pygame.draw.rect(screen,blue1,[40+move,lst_size[1]-74,400,25],2)
    pygame.draw.rect(screen,blue1,[40+move,lst_size[1]-74,expline,25])
    screen.blit(textexp,[160+move,lst_size[1]-73])
    screen.blit(textsp,[620,lst_size[1]-38])
    screen.blit(textlevel_sp,[lst_size[0]-402-166,lst_size[1]-68])
    #画一个小黑条是画面过度更自然
    pygame.draw.rect(screen,black,[0,lst_size[1]-90,lst_size[0],10],1)
    stick=pygame.Surface((lst_size[0],10))
    stick.set_alpha(135)
    stick.fill(black)
    screen.blit(stick,(0,lst_size[1]-90))                     

    #画出敌人子弹 升级效果 
    enemybulletlist.draw(screen)
    levelup()
    global_time+=1
    
    #爆炸动画
    for enem in enemylist:
        if enem.explo>0:
            enem.explo-=1
            screen.blit(lst_explo[15-enem.explo/2],[enem.rect.x-110,enem.rect.y-110])
    #游戏结束的判定        
    if live==1 and player.hp < 0:
        gameover()
       

    # Go ahead and update the screen with what we've drawn.
    pygame.display.update([0,0,lst_size[0],lst_size[1]])

    # Limit to fps frames per second
    clock.tick(fps)
    

# Close the window and quit.

pygame.quit ()

