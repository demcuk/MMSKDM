#encoding: utf-8
# кінематика механізму верстата-гойдалки (компонентно-орієнтований підхід)
# визначення полодження, швидкості і прискорення ланок за кутом повороту a кривошипа

from __future__ import division
import matplotlib.pyplot as plt
from scipy.optimize import root # функція для розв'язування системи рівнянь
from math import pi,sin,cos,tan,degrees,atan

class Frame:
    "Компонент описує ланку механізму"
    def __init__(self,x1,y1,x2,y2,L):
        "x1,y1,x2,y2,L - координати точок і довжина ланки"
        self.x1,self.y1,self.x2,self.y2,self.L=x1,y1,x2,y2,L
    def eqs(self): # система рівнянь компонента
        eqs=[]
        eqs+= [(self.x2-self.x1)**2 + (self.y2-self.y1)**2 - self.L**2] # незмінна відстань між точками
        return eqs
    def plot(self): # рисує компонент
        plt.plot([self.x1,self.x2],[self.y1,self.y2],'ko-')

class Connector:
    "Компонент описує шарнірне з'єднання двох ланок"
    def __init__(self,e1,e2):
        "e1,e2 - дві ланки, які з'єднуються точками 2 і 1 відповідно"
        self.e1,self.e2=e1,e2
    def eqs(self): # система рівнянь компонента
        eqs=[]
        eqs+= [self.e1.x2-self.e2.x1] # e1.x2=e2.x1
        eqs+= [self.e1.y2-self.e2.y1] # e1.y2=e2.y1
        return eqs
    def plot(self): # рисує компонент
        plt.plot([self.e1.x2],[self.e1.y2],'ro') 

class Connector2:
    "Компонент описує нерухоме з'єднання двох ланок"
    def __init__(self,e1,e2):
        "e1,e2 - дві ланки, які з'єднуються точками 2 і 1 відповідно"
        self.e1,self.e2=e1,e2
    def eqs(self): # система рівнянь компонента
        eqs=[]
        eqs+= [self.e1.x2-self.e2.x1] # e1.x2=e2.x1
        eqs+= [self.e1.y2-self.e2.y1] # e1.y2=e2.y1
        # однаковий кут повороту ланок: tan(a1)=tan(a2)
        eqs+= [(self.e1.y1-self.e1.y2)/(self.e1.x1-self.e1.x2)-(self.e2.y2-self.e2.y1)/(self.e2.x2-self.e2.x1)]
        return eqs
    def plot(self): # рисує компонент
        plt.plot([self.e1.x2],[self.e1.y2],'yo') 
            
class System:
    "Система компонентів"
    def __init__(self,e):
        "e - список компонентів"
        self.e=e
    def eqs(self): # система усіх рівнянь, які описують поведінку системи
        eqs=[]
        for ei in self.e: # для кожного компоненту
            eqs+= ei.eqs() # додати в список рівнянь усі рівняння компонента
        return eqs
    def plot(self): # рисує усі компоненти системи
        for ei in self.e:
            ei.plot()
        
def f(X, s): # векторна функція повертає значення лівих частин рівнянь
    exec rootstr+"=X" # невідомі (X - вектор початкових наближень)
    eqs=s.eqs()
    return eqs # якщо усі елементи eqs близькі до 0, то X - шукані корені

t,a=0,0 # початкові значення часу і кута повороту кривошипа
T,X=[],[] # списки значень часу і невідомих
d = type('', (), dict(xa=0, ya=0, xb=-1.345, yb=3.01195, L0=0.81371, L1=3.0, L2=2.0, L3=2.29))() # відомі постійні параметри механізму
fr0=Frame(x1=0.0,y1=0.0, x2=0.81371,y2=0, L=d.L0) # кривошип
fr1=Frame(x1=0.81371,y1=0, x2=0.65,y2=3, L=3.0) # шатун
fr2=Frame(x1=0.65,y1=3, x2=-1.345,y2=3.01195, L=2.0) # заднє плече балансира
fr3=Frame(x1=-1.345,y1=3.01195, x2=-3.6,y2=3, L=2.29) # переднє плече балансира
con0=Connector(fr0,fr1) # шарнір між кривошипом і шатуном
con1=Connector(fr1,fr2) # шарнір між шатуном і балансиром
con2=Connector2(fr2,fr3) # нерухоме зєднання плечей балансира
s=System([fr0, fr1, fr2, fr3, con0, con1, con2]) # механізм верстата-гойдалки
rootstr="s.e[1].x1, s.e[1].y1, s.e[1].x2, s.e[1].y2, s.e[2].x1, s.e[2].y1,  s.e[3].x2, s.e[3].y2"
# рядок rootstr потрібен щоб назви коренів записувались в програмі тільки один раз

while a<2*pi: # поки кут < 360 градусів
    s.e[0].x2=s.e[0].L*cos(a)+s.e[0].x1 # координата точки кривошипа dx/L=cos(a)
    s.e[0].y2=s.e[0].L*sin(a)+s.e[0].y1 # координата точки кривошипа dy/L=sin(a)
    # увага! потрібно запобігати тому щоб початкові наближення коренів =0
    roots=[x+0.001 for x in eval(rootstr)] # наприклад шляхом додавання 0.001
    sol = root(f, roots, args=(s,), method='lm') # розв'язати систему рівнянь
    exec rootstr+"=sol.x" # корені
    #print eval(rootstr)
    b=atan((s.e[3].y2-s.e[3].y1)/(s.e[3].x2-s.e[3].x1)) # кут повороту балансира atan(dy/dx)
    x,y=s.e[0].x1+s.e[3].x1-s.e[3].L, -s.e[3].L*b # координати точки підвісу
    plt.plot([x],[y],'bo')
    plt.text(x+0.1, y, t)
    plt.text(s.e[0].x2, s.e[0].y2, t)
    s.plot() # нарисувати положення ланок механізму
    T.append(t)
    X.append(y)
    t+=1 # збільшити час на крок
    a+=pi/16 #15.5 # збільшити кут на крок
plt.show()

import scipy
dt=T[1]-T[0]
V=scipy.gradient(X, dt) # швидкість (central differences)
A=scipy.gradient(V, dt) # прискорення (central differences)
plt.plot(T, X, 'k-', lw=2)
plt.plot(T, V, 'k--', lw=2)
plt.plot(T, A, 'r', lw=2)
plt.show()
