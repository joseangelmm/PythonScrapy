'''
Created on 4 mar. 2019
@author: josea
'''
# -*- coding: utf-8 -*-

from tkinter import *
import sqlite3
from bs4 import BeautifulSoup
import urllib.request
import requests
from tkinter import messagebox
###############################################################################################################################################################
def InformacionGeneralDeLasPrimeras3Paginas(codigoHtml1,codigoHtml2,codigoHtml3):
    titulos1=[i['title'] for i in codigoHtml1.find_all('a',class_='title')]
    titulos2=[i['title'] for i in codigoHtml2.find_all('a',class_='title')]
    titulos3=[i['title'] for i in codigoHtml3.find_all('a',class_='title')]
    titulos=titulos1,titulos2,titulos3
    
    enlaces1=[i['href'] for i in codigoHtml1.find_all('a',class_='title')]
    enlaces2=[i['href'] for i in codigoHtml2.find_all('a',class_='title')]
    enlaces3=[i['href'] for i in codigoHtml3.find_all('a',class_='title')]
    enlaces=enlaces1,enlaces2,enlaces3
    
    autores1=[i.text for i in codigoHtml1.find_all('a',class_='username')]
    autores2=[i.text for i in codigoHtml2.find_all('a',class_='username')]
    autores3=[i.text for i in codigoHtml3.find_all('a',class_='username')]
    autores=autores1,autores2,autores3
    
    fecha1 =[i.previous_element for i in codigoHtml1.find_all('span',class_='time')]
    fecha2 =[i.previous_element for i in codigoHtml2.find_all('span',class_='time')]
    fecha3 =[i.previous_element for i in codigoHtml3.find_all('span',class_='time')]
    fechas=fecha1,fecha2,fecha3
    
    horasDeCreacion1= [i.text for i in codigoHtml1.find_all('span',class_='time')]
    horasDeCreacion2= [i.text for i in codigoHtml2.find_all('span',class_='time')]
    horasDeCreacion3= [i.text for i in codigoHtml3.find_all('span',class_='time')]
    horasDeCreacion=horasDeCreacion1,horasDeCreacion2,horasDeCreacion3
    
    respuestas1=[i.li.get_text()[-1] for i in codigoHtml1.find_all('ul',class_='threadstats td alt')]
    respuestas2=[i.li.get_text()[-1] for i in codigoHtml2.find_all('ul',class_='threadstats td alt')]
    respuestas3=[i.li.get_text()[-1] for i in codigoHtml3.find_all('ul',class_='threadstats td alt')]   
    respuestas=respuestas1,respuestas2,respuestas3
    
    visitas1=[i.text for i in codigoHtml1.find_all('ul',class_='threadstats td alt')]
    for i in range(len(visitas1)):
        c=re.match('.*(\n).*(\d).*(\n).*(\d)',visitas1[i])
        visitas1.append(c.groups()[3])
    visitas2=[i.text for i in codigoHtml2.find_all('ul',class_='threadstats td alt')]
    for i in range(len(visitas2)):
        c=re.match('.*(\n).*(\d).*(\n).*(\d)',visitas2[i])
        visitas2.append(c.groups()[3])
    visitas3=[i.text for i in codigoHtml3.find_all('ul',class_='threadstats td alt')]
    for i in range(len(visitas3)):
        c=re.match('.*(\n).*(\d).*(\n).*(\d)',visitas1[i])
        visitas3.append(c.groups()[3])
        
    visitass=[]
    visitas=[]
    for item in reversed(visitas1):
        visitass.append(item)
    visitas.append(visitass[0:20])
    for item in reversed(visitas2):
        visitass.append(item)
    visitas.append(visitass[0:20])
    for item in reversed(visitas3):
        visitass.append(item)
    visitas.append(visitass[0:20])
    
    
    Titulos                 = ponerEnUnaSolaLista(titulos)
    Enlaces                 = ponerEnUnaSolaLista(enlaces)
    EnlacesCorrectos        = ponerEnlacesCorrectos(Enlaces)
    Autores                 = ponerEnUnaSolaLista(autores)
    Fechas                  = ponerEnUnaSolaLista(fechas)
    Fechas                  = ponerFechasCorrectas(Fechas)
    HorasDeCreacion         = ponerEnUnaSolaLista(horasDeCreacion)
    Respuestas              = ponerEnUnaSolaLista(respuestas)
    Respuestas              = pasarAInteger(Respuestas)
    Visitas                 = ponerEnUnaSolaLista(visitas)
    Visitas                 = pasarAInteger(Visitas)
    return cargar(Titulos,EnlacesCorrectos,Autores,Fechas,HorasDeCreacion,Respuestas,Visitas)
    
###############################################################################################################################################################
def ponerFechasCorrectas(datos):
    listaDefinitiva = []
    for item in datos:
        temp = len(item)
        listaDefinitiva.append(item[:temp - 2])
    return listaDefinitiva
###############################################################################################################################################################
def pasarAInteger(datos):
    listaDefinitiva=[]
    for item in datos:
        listaDefinitiva.append(int(item))
    return listaDefinitiva
###############################################################################################################################################################
def ponerEnlacesCorrectos(datos):    
    listaDefinitiva = []
    for item in datos:
        listaDefinitiva.append("https://foros.derecho.com/"+item)
    return listaDefinitiva
###############################################################################################################################################################
def ponerEnUnaSolaLista(datos):
    listaDefinitiva = []
    for i in range(len(datos[0])):
        listaDefinitiva.append(datos[0][i])
    for i in range(len(datos[1])):
        listaDefinitiva.append(datos[1][i])
    for i in range(len(datos[2])):
        listaDefinitiva.append(datos[2][i])        
    return listaDefinitiva
###############################################################################################################################################################
def cargar(Titulos,EnlacesCorrectos,Autores,Fechas,HorasDeCreacion,Respuestas,Visitas):
    conn = sqlite3.connect('foro.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS FORODERECHO")   
    conn.execute('''CREATE TABLE FORODERECHO
                (  ID INTEGER       PRIMARY KEY  AUTOINCREMENT,
                   TITULO           TEXT         NOT NULL,
                   ENLACE           TEXT         NOT NULL,
                   AUTOR            TEXT         NOT NULL,
                   FECHA            TEXT         NOT NULL,
                   HORA             TEXT         NOT NULL,
                   RESPUESTAS       INTEGER      NOT NULL,
                   VISITAS          INTEGER      NOT NULL);''')
    for i in range(len(Titulos)):
        conn.execute("""INSERT INTO FORODERECHO (TITULO,ENLACE,AUTOR,FECHA,HORA,RESPUESTAS,VISITAS) VALUES (?,?,?,?,?,?,?)""",
                     (Titulos[i],EnlacesCorrectos[i],Autores[i],Fechas[i],HorasDeCreacion[i],Respuestas[i],Visitas[i]))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM FORODERECHO")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()   
###############################################################################################################################################################
def mostrarResgistrosEnBaseDeDatos():
    conn = sqlite3.connect('foro.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA FROM FORODERECHO")
    mostrarPorPantalla(cursor)
    conn.close()
###############################################################################################################################################################
def salir(ventanaDatos):
    return ventanaDatos.destroy()
###############################################################################################################################################################
def mostrarPorPantalla(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)
###############################################################################################################################################################
def temasMasPopulares():
    conn = sqlite3.connect('foro.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA,VISITAS FROM FORODERECHO ORDER BY VISITAS DESC LIMIT 5")
    mostrarPorPantallaVisitasOComentarios(cursor)
    conn.close()
###############################################################################################################################################################
def temasMasActivos():    
    conn = sqlite3.connect('foro.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA,RESPUESTAS FROM FORODERECHO ORDER BY RESPUESTAS DESC LIMIT 5")
    mostrarPorPantallaVisitasOComentarios(cursor)
    conn.close()
###############################################################################################################################################################
def mostrarPorPantallaVisitasOComentarios(cursor):
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
###############################################################################################################################################################
def buscarPorTema():       
    def listar_busqueda(event):
        conn = sqlite3.connect('foro.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,AUTOR,FECHA FROM FORODERECHO WHERE TITULO LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        mostrarPorPantalla(cursor)
        conn.close()    
    v = Toplevel()
    lb = Label(v, text="Introduzca el nombre del título: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
###############################################################################################################################################################
def buscarPorAutor():
    def listar_busqueda(event):
        conn = sqlite3.connect('foro.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,AUTOR,FECHA FROM FORODERECHO WHERE AUTOR LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        mostrarPorPantalla(cursor)
        conn.close()    
    v = Toplevel()
    lb = Label(v, text="Introduzca el nombre del autor: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
###############################################################################################################################################################
def ventana_principal():

    ventanaPrincipal = Tk()
    botonDatos = Button(ventanaPrincipal, text = "Datos", command = ventanaDatos())
    botonBuscar = Button(ventanaPrincipal, text = "Buscar", command = ventanaBusquedas())
    botonEstadisticas = Button(ventanaPrincipal, text = "Estadísticas", command = ventanaEstadisticas())
    """
    botonDatos.grid(row = 0, column = 0)
    botonBuscar.grid(row = 0, column = 1)
    botonEstadisticas.grid(row = 0, column = 2)
    """
    botonDatos.pack(side = TOP)
    botonBuscar.pack(side = TOP)
    botonEstadisticas.pack(side = TOP)
    
    ventanaPrincipal.mainloop()

###############################################################################################################################################################
def ventanaDatos():
    ventanaDatos = Tk()
    botonCarga   = Button(ventanaDatos, text = "Carga", command = cargarPaginaYVolcarEnBaseDeDatos())
    botonMostrar = Button(ventanaDatos, text = "Mostrar", command = mostrarResgistrosEnBaseDeDatos())
    #botonSalir   = Button(ventanaDatos, text = "Salir", command = salir(ventanaDatos))
    
    botonCarga.grid(row = 0, column = 0)
    botonMostrar.grid(row = 0, column = 1)
    #botonSalir.grid(row = 0, column = 2)
###############################################################################################################################################################
def ventanaBusquedas():
    ventanaBusquedas= Tk()
    botonTema    = Button(ventanaBusquedas, text = "Búsqueda por tema", command = buscarPorTema())
    botonAutor   = Button(ventanaBusquedas, text = "Búsqueda por autor", command = buscarPorAutor())
    
    botonTema.grid(row = 0, column = 0)
    botonAutor.grid(row = 0, column = 1)
###############################################################################################################################################################
def ventanaEstadisticas():
    ventanaEstadisticas = Tk()
    botonMasPopulares   = Button(ventanaEstadisticas, text = "Más populares", command = temasMasPopulares())
    botonMasActivos     = Button(ventanaEstadisticas, text = "Más activos", command = temasMasActivos())
    
    botonMasPopulares.grid(row = 0, column = 0)
    botonMasActivos.grid(row = 0, column = 1)
###############################################################################################################################################################
def abrir(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    return soup
###############################################################################################################################################################
def cargarPaginaYVolcarEnBaseDeDatos():
    archivoHtmlI=abrir('https://foros.derecho.com/foro/20-Derecho-Civil-General')
    archivoHtmlII=abrir('https://foros.derecho.com/foro/20-Derecho-Civil-General/page2')
    archivoHtmlIII=abrir('https://foros.derecho.com/foro/20-Derecho-Civil-General/page3')
    InformacionGeneralDeLasPrimeras3Paginas(archivoHtmlI,archivoHtmlII,archivoHtmlIII)
###############################################################################################################################################################
if __name__ == "__main__":
    ventana_principal()
