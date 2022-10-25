"""
Universidad del Valle de Guatemala 
Física III - Sección 30
Javier Mejía Alecio 20304
Juan Pablo Zelada 201004

Se simula la trayectoria de los electrones dentro de un tubo de rayos catódicos y la colisión de estas en una pantalla.

"""

#Se importan las librerías utilizadas para la matemática, gráficas animadas e interfaz gráfica
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from math import pi

#Se establecen los valores que se mantienen contante y las listas encargadas de almacenar las coordenadas de colisión de las partículas
DX = 0.09
Dy = 0.015/4
mole = []
X = [0]
Y = [0]
VX = []
VY = []
d = 0
opt = ['0', 'pi/4', 'pi/2', '3*pi/4', 'pi']


#Se crea la clave de color y la gráfica encargada de mostrar las colisiones de las partículas.
intensity = []
t = np.linspace(0, 2*pi, 125)
colors = [[0,0,1,0],[0,0,1,0.5],[0,0.2,0.4,1]]
cmap = LinearSegmentedColormap.from_list("", colors)
fig, ax = plt.subplots()
ax.axis([-155,155,-155,155])
scatter = ax.scatter(VX, VY, c =[], cmap = cmap, vmin = 0, vmax = 1, marker = ".")


#Se crea una clase encargada de crear los objetos que actúan como partículas. Estos objetos reciben valores que van a adeterminar su aceleración tanto en X como en Y.
class Moleculas:
    def __init__(self, canvas, x, y, w, h, Yo, tipo, mass = 9.11*10**-31, q = -1.60*10**-19, Xo = -275, color = 'blue'):
        
        #Se defienen las propiedades de los objetos 
        self.canvas = canvas


        self.x = x
        self.y = y
        self.vel = [0,0]
        self.acc = [0,0]    
        self.body = self.canvas.create_oval(x-w/2, y-h/2, x+w/2, x+h/2, fill = color)
        self.mass = mass
        self.q = q
        self.tipo = tipo
        self.Xo = Xo
        self.Yo = Yo
        self.colors = [0,0,0,0]

        #Se colocan en posición incial
        self.canvas.move(self.body, -275, Yo)

    #Se crean una función para definir la aceleración de la partícula en el eje X
    def Acex(self, Px):
        self.acc[0] = (self.q*Px)/(self.mass*DX)
        

    #Se crean una función para definir la aceleración de la partícula en el eje Y
    def Acey(self, Py):
        self.acc[1] = (self.q*Py)/(self.mass*Dy)


    #Se crea la función encargada de actualizar la velocidad y posición de las partículas durante el trayecto
    def update(self, t, P1, P2):
        self.x, self.y, *c = self.canvas.coords(self.body)

        if self.x <= 383:

            self.Acex(P1)

            #Se colocan sentencias lógicas para determinar si las partículas ya colisionaron con la pantalla y para determinar cuando se encuentran entre las placas de deflección
            if self.x >= 140 and self.x <= 145 and self.tipo == "S":
                self.Acey(P2)
                self.vel[1] = self.vel[1] + self.acc[1]*t

            elif self.x >= 150 and self.x <= 155 and self.tipo == "L":
                self.Acey(P2)
                self.vel[1] = self.vel[1] + self.acc[1]*t

            self.vel[0] = self.vel[0] + self.acc[0]*t
            
            
            self.canvas.move(self.body, -self.vel[0], self.vel[1])
        
            

        else:
            if self.tipo == "S":
                X.append(self.y-625)
            else:
                Y.append(self.y-196)

            self.canvas.delete(self.body)

    #Se crea una función para destruir las partículas
    def AD(self):
        self.canvas.delete(self.body)





        




#Se crea una clase encargada de tener los elementos gráficos de la simulación
class aplic():
    #Se crea la funición principal
    def __init__(self):
        #Se crea la ventana master. A esta ventana el usuario no tiene acceso por ser la que mantiene el loop del programa
        self.master = Tk()
        self.master.geometry("1x1")
        self.master.withdraw()
        self.root = tk.Toplevel()
        #Se definen las dimensiones de la ventana a la que tiene acceso el usuario
        w,h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.resizable(False,False)

        self.Can = Canvas(self.root, bg = 'white', height = h, width = w)
        self.Can.pack()

        self.graph = Canvas(self.Can, bg = 'black', height = 750, width = 635)
        self.graph.place(x = 650, y = 40)

        fontt = tkFont.Font(family = "Century Gothic", size = 10)


#Se crea la Vista Superior del tubo
        lS = Label(self.Can, text = "Vista superior del tubo", font = fontt, bg = 'white')
        lS.place(x = 50, y = 500)

        p1 = self.Can.create_rectangle(0, 0, 120, 1, fill ="black")
        self.Can.move(p1, 50, 650)

        p2 = self.Can.create_rectangle(0, 0, 120, 1, fill ="black")
        self.Can.move(p2, 50, 611)

        p3 = self.Can.create_rectangle(0, 0, 341, 1, fill ="black")
        self.Can.move(p3, 50, 630)

        p4 = self.Can.create_line(120, 0, 341, 129, width = 2)
        self.Can.move(p4, 50, 650)

        p5 = self.Can.create_line(120, 0, 341, -143, width = 2)
        self.Can.move(p5, 50, 611)

        p6 = self.Can.create_line(341, -156, 341, 156)
        self.Can.move(p6, 50, 624)

        p8 = self.Can.create_line(250, 31, 250, 70)
        self.Can.move(p8, -200, 580)


        


#Se crea la Vista lateral del tubo
        lL = Label(self.Can, text = "Vista lateral del tubo", font = fontt, bg = 'white')
        lL.place(x = 50, y = 75)

        p1 = self.Can.create_rectangle(0, 0, 120, 1, fill ="black")
        self.Can.move(p1, 50, 220)

        p2 = self.Can.create_rectangle(0, 0, 120, 1, fill ="black")
        self.Can.move(p2, 50, 181)

        p3 = self.Can.create_rectangle(0, 0, 341, 1, fill ="black")
        self.Can.move(p3, 50, 200)

        p4 = self.Can.create_line(120, 0, 341, 129, width = 2)
        self.Can.move(p4, 50, 220)

        p5 = self.Can.create_line(120, 0, 341, -143, width = 2)
        self.Can.move(p5, 50, 181)

        p6 = self.Can.create_line(341, -156, 341, 156)
        self.Can.move(p6, 50, 194)

        p8 = self.Can.create_line(250, 31, 250, 70)
        self.Can.move(p8, -200, 150)

        #Frame para los botones
        W = Frame(self.Can, height = 300, width = 1050, bg = "#F0B27A")
        W.place(x = 465 , y = 520)

        
        #Se crean los sliders, checkbox y combobox utilizados para obtener los valores que desee el usuario
        SV = Scale(W, from_=-500, to=500, tickinterval= 500, orient=HORIZONTAL, length=185, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Potencial placas verticales', font = fontt)
        SV.set(0)
        SV.place(x = 10, y = 35)


        SH = Scale(W, from_=-475, to=475, tickinterval= 225, orient=HORIZONTAL, length=200, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Potencial placas horizontales', font = fontt)
        SH.set(0)
        SH.place(x = 300, y = 35)

        SA = Scale(W, from_= 500, to=2500, tickinterval= 500, orient=HORIZONTAL, length=250, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Potencial Aceleración', font = fontt)
        SA.set(0)
        SA.place(x = 10, y = 130)

        SD = Scale(W, from_= 0, to=1, resolution= 0.1, orient=HORIZONTAL, length=200, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Tiempo del difuminado', font = fontt)
        SD.set(.5)
        SD.place(x = 300, y = 130)

        SAx = Scale(W, from_= -200, to=200, tickinterval = 20, orient=HORIZONTAL, length=150, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Apertura de X', font = fontt)
        SAx.set(100)
        SAx.place(x = 675, y = 35)

        SAy = Scale(W, from_= -200, to=200, tickinterval = 20, orient=HORIZONTAL, length=150, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Apertura de Y', font = fontt)
        SAy.set(100)
        SAy.place(x = 850, y = 35)

        Sfx = Scale(W, from_= 0, to=10, tickinterval = 5, orient=HORIZONTAL, length=150, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Frecuencia de X', font = fontt)
        Sfx.set(1)
        Sfx.place(x = 675, y = 130)

        Sfy = Scale(W, from_= 0, to=10, tickinterval = 5, orient=HORIZONTAL, length=150, bg = '#F0B27A', bd = 0, highlightbackground = '#F0B27A', label = 'Frecuencia de Y', font = fontt)
        Sfy.set(1)
        Sfy.place(x = 850, y = 130)

        des = StringVar()
        des.set(opt[0])

        drop = OptionMenu(W, des, *opt)
        drop.place(x = 820, y = 215)


        var = StringVar()

        c = Checkbutton(W, text = "Modo sinusoidal", variable = var, onvalue = "on", offvalue = "off", font = fontt, bg = "#F0B27A")
        c.deselect()
        c.place(x = 530, y = 15)


        #Ya que, el combobox devuelve un valor de texto se crea una función para obtener un valor numérico
        def desfase():
            v = des.get()

            if v == '0':
                return 0
            elif v == 'pi/4':
                return pi/4
            elif v == 'pi/2':
                return pi/2
            elif v == '3*pi/4':
                return (3*pi)/4
            elif v == 'pi':
                return pi


        #Función que calcula el voltaje con una función de coseno en las placas horizontales 
        def VoltX(m):

            return -SAx.get()*np.cos(Sfx.get()*m )

        #Función que calcula el voltaje con una función de coseno en las placas veticales 
        def VoltY(m):
            return -SAy.get()*np.cos(Sfy.get()*m + desfase())


        #Se obtiene las coordenadas de la última colisión y se envían a la función que actualiza la gráfica de matplotlib
        def get_new():
            new_X = [X[-1]]
            new_y = [Y[-1]]

            return new_X, new_y





#Gráfica

        #Función que actuliza la gráfica (pantalla)
        def animate(i):
            #Se obtiene el valor creado al inico dle programa
            global intensity
            #Se obtiene loa valores que se van a graficar
            Nx, Ny = get_new()
            #Se añade a la lista de puntos 
            VX.extend(Nx)
            VY.extend(Ny)
            #Se grafican
            scatter.set_offsets(np.c_[VX,VY])
            #Se actualiza el color de los puntos
            intensity = np.concatenate((np.array(intensity)*SD.get(), np.ones(len(Nx))))
            scatter.set_array(intensity)

            return ax 
        
        #Se crea el lienzo sobre el que se coloca la gráfica
        CA = FigureCanvasTkAgg(fig, master=self.graph)
        CA.get_tk_widget().place(x = 0, y = 0)

        
        #Se invoca a la animación
        ani = animation.FuncAnimation(fig, animate)
        

            
        self.root.update()


        #Función encargada de las partículas en modo sinusoidal
        def Lis():
            i = 0
            b = 0
            SD.set(.95)
            while i < len(t):
                try:
                    #Se crean las partículas
                    Ml = Moleculas(self.Can, 350, 350, 10, 10, -149, "L")
                    mole.append(Ml)
                    Ms = Moleculas(self.Can, 350, 350, 10, 10, 280, "S")
                    mole.append(Ms)

                    while True:
                        try:
                            self.root.update()
                            #Incia el movimiento sinusoidal de las partículas
                            for m in mole:
                                if m.tipo == "S":
                                    m.update(0.000000000000000001, SA.get(), VoltX(t[i]))
                                elif m.tipo == 'L':
                                    m.update(0.000000000000000001, SA.get(), VoltY(t[i]))
                        except:
                            break
                    #Se eliminan las partículas que ya terminaron el viaje
                    mole.clear()
                    i += 1
                except:
                    break

            c.deselect()
            SD.set(0.7)






        
            






#Bucle de las partículas
        #Función encargada de las partículas en modo lineal
        while True:
            try:
                #Se crean las partículas
                Ml = Moleculas(self.Can, 350, 350, 10, 10, -149, "L")
                mole.append(Ml)
                Ms = Moleculas(self.Can, 350, 350, 10, 10, 280, "S")
                mole.append(Ms)
                while True:
                    try:
                        self.root.update()
                        #Se verifica el modo en el que esta el programa
                        if var.get() == 'off':
                            #Incia el movimiento lineal de las partículas
                            for m in mole:
                                if m.tipo == "S":
                                    m.update(0.0000000000000001, SA.get(), SH.get())
                                elif m.tipo == "L":
                                    m.update(0.0000000000000001, SA.get(), SV.get())

                        elif var.get() == 'on':
                            SD.set(0)
                            for m in mole:
                                m.AD()
                            mole.clear()
                            Lis()
                            break
                                
                    except:
                        break
                mole.clear()

            except:
                break


        








        self.master.mainloop()











#Función que mantiene abierto el programa


def main():
    app = aplic()
    return(0)
        
if __name__ == '__main__':
    main()
        
