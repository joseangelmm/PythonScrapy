'''
Created on 8 mar. 2019

@author: josea
'''
#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

def extraer_jornadas():
    f = urllib.request.urlopen("http://resultados.as.com/resultados/futbol/primera/2017_2018/calendario/")
    s = BeautifulSoup(f,"lxml")
    
    l = s.find_all("div", class_= ["cont-modulo","resultados"])
    return l


def imprimir_lista(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    jornada=0
    for row in cursor:
        if row[0] != jornada:
            jornada=row[0]
            lb.insert(END,"\n")
            s = 'JORNADA '+ str(jornada)
            lb.insert(END,s)
            lb.insert(END,"-----------------------------------------------------")
        s = "     " + row[1] +' '+ str(row[3]) +'-'+ str(row[4]) +' '+  row[2]
        lb.insert(END,s)
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)
 
def almacenar_bd():
    conn = sqlite3.connect('as.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS JORNADAS") 
    conn.execute('''CREATE TABLE JORNADAS
       (JORNADA       INTEGER NOT NULL,
       LOCAL          TEXT    NOT NULL,
       VISITANTE      TEXT    NOT NULL,
       GOLES_L        INTEGER    NOT NULL,
       GOLES_V        INTEGER NOT NULL,
       LINK           TEXT);''')
    l = extraer_jornadas()
    for i in l:
        jornada = int(re.compile('\d+').search(i['id']).group(0))
        partidos = i.find_all("tr",id=True)
        for p in partidos:
            equipos= p.find_all("span",class_="nombre-equipo")
            local = equipos[0].string.strip()
            visitante = equipos[1].string.strip()
            resultado_enlace = p.find("a",class_="resultado")
            if resultado_enlace != None:
                goles=re.compile('(\d+).*(\d+)').search(resultado_enlace.string.strip())
                goles_l=goles.group(1)
                goles_v=goles.group(2)
                link = resultado_enlace['href']
                
                conn.execute("""INSERT INTO JORNADAS VALUES (?,?,?,?,?,?)""",(jornada,local,visitante,goles_l,goles_v,link))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM JORNADAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


def listar_bd():
    conn = sqlite3.connect('as.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM JORNADAS ORDER BY JORNADA")
    imprimir_lista(cursor)
    conn.close()


  
def ventana_principal():
    top = Tk()
 
    almacenar = Button(top, text="Almacenar Resultados", command = almacenar_bd)
    almacenar.pack(side = TOP)
    listar = Button(top, text="Listar Jornadas", command = listar_bd)
    listar.pack(side = TOP)
    
    buscarJornada = Button(top, text="Buscar por jornada", command=buscarPorJornada)
    buscarJornada.pack(side = TOP)
    
    buscarGoles = Button(top, text="Buscar por jornada y partido", command=buscarJornadaYDespuesGoles)
    buscarGoles.pack(side = TOP)
    
    top.mainloop()

def buscarPorJornada():
    def listar_busqueda(event):
        conn = sqlite3.connect('as.db')
        conn.text_factory = str
        s = en.get() 
        cursor = conn.execute("""SELECT LOCAL,VISITANTE,GOLES_L,GOLES_V FROM JORNADAS WHERE JORNADA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        mostrarPorPantalla(cursor)
        conn.close()    
    v = Toplevel()
    lb = Label(v, text="Introduzca la jornada: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
#####
def buscarJornadaYDespuesGoles():
    def obtenerPartidosDeEsaJornada(event):
        conn = sqlite3.connect('as.db')
        conn.text_factory = str
        s = en.get() 
        cursor = conn.execute("""SELECT LOCAL,VISITANTE,GOLES_L,GOLES_V,LINK FROM JORNADAS WHERE JORNADA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        mostrarListaDePartidosEnUnSpinbox(cursor,s)
        conn.close() 
    v = Toplevel()
    lb = Label(v, text="Introduzca la jornada: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", obtenerPartidosDeEsaJornada)
    en.pack(side = LEFT)
       
        
def mostrarListaDePartidosEnUnSpinbox(cursor,s):
    def click_me():
        partidoSeleccionado=spin1.get().split("-")
        local=partidoSeleccionado[0]
        visitante=partidoSeleccionado[1]
        golesLocales=int(partidoSeleccionado[2])
        golesVisitantes=int(partidoSeleccionado[3])
        ss=int(s)
        conn = sqlite3.connect('as.db')
        conn.text_factory = str  
        cursor1 = conn.execute('SELECT LINK FROM JORNADAS WHERE JORNADA == "%i" AND LOCAL == "%s" AND VISITANTE == "%s" ' % (ss,local,visitante))    
        mostrarPorPantalla11(cursor1)
        conn.close()
        
    root=Tk()
    lista=[]
    for item in cursor:
        lista.append(str(item[0])+"-"+str(item[1])+"-"+str(item[2])+"-"+str(item[3]))
        
    spin1=Spinbox(root, values=lista)
    spin1.pack()
    button =Button(root,text="Selecionar partido",command=click_me)
    button.pack()
    root.mainloop()
####    
    
    
def mostrarPorPantalla(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,row[3])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)
    
def mostrarPorPantalla11(cursor):
    listaa=[]
    for row in cursor:
        listaa.append("https://resultados.as.com"+row[0])
    return ultimoEjercicio(listaa[0])
    

    
def ultimoEjercicio(enlace):
    f = urllib.request.urlopen(enlace)
    s = BeautifulSoup(f,"lxml")
    
    listaEventos=[i.text for i in s.find_all('p',class_='txt-accion')]
    liii=[]
    for item in listaEventos:
        if 'Gol' in item:
            liii.append(item.splitlines())
    print(liii)
    return mostrarPorPantallaGoles(liii)


def mostrarPorPantallaGoles(listaEventos):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in listaEventos:
        lb.insert(END,"Gol en el minuto "+row[1]+" marcado por "+row[3])        
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

if __name__ == "__main__":
    ventana_principal()
    
