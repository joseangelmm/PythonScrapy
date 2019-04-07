#encoding:utf-8
import os
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD
from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh import qparser
from whoosh import scoring
from datetime import datetime
from tkinter import *
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.qparser import dateparse, default, plugins, syntax
from whoosh.util.times import adatetime
from tkinter import messagebox

def creaIndexYEsquemaYScrapy():
    f = urllib.request.urlopen("https://www.meneame.net/")
    fPage2 = urllib.request.urlopen("https://www.meneame.net/?page=2")
    fPage3 = urllib.request.urlopen("https://www.meneame.net/?page=3")
    
    s = BeautifulSoup(f,"lxml")
    sPage2 = BeautifulSoup(fPage2,"lxml")
    sPage3 = BeautifulSoup(fPage3,"lxml")
    
    #############
    ###PÁGINA1###
    #############
    titulares1=[i.text for i in s.find_all('div',class_='center-content')]
    titularesDefinitivos1=metodosTitulares(titulares1)
    enlace1=metodoEnlaces(s)
    autores1=metodoAutores(s)
    fuenteNoticia1=metodoFuenteNoticia(titulares1)
    timesTamp1=[i['data-ts'] for i in s.findAll('span', class_="ts visible")]
    FechaYHora1=metodoFechaYHora(timesTamp1)
    cuerpoDeLaNoticia1=[i.text for i in s.find_all('div',class_='news-content')]
   
    #############
    ###PÁGINA2###
    #############
    
    titulares2=[i.text for i in sPage2.find_all('div',class_='center-content')]
    titularesDefinitivos2=metodosTitulares(titulares2)
    enlace2=metodoEnlaces(sPage2)
    autores2=metodoAutores(sPage2)
    fuenteNoticia2=metodoFuenteNoticia(titulares2)
    timesTamp2=[i['data-ts'] for i in sPage2.findAll('span', class_="ts visible")]
    FechaYHora2=metodoFechaYHora(timesTamp2)
    cuerpoDeLaNoticia2=[i.text for i in sPage2.find_all('div',class_='news-content')]
    
    #############
    ###PÁGINA3###
    #############
    titulares3=[i.text for i in sPage3.find_all('div',class_='center-content')]
    titularesDefinitivos3=metodosTitulares(titulares3)
    enlace3=metodoEnlaces(sPage3)
    autores3=metodoAutores(sPage3)
    fuenteNoticia3=metodoFuenteNoticia(titulares3)
    timesTamp3=[i['data-ts'] for i in sPage3.findAll('span', class_="ts visible")]
    FechaYHora3=metodoFechaYHora(timesTamp3)
    cuerpoDeLaNoticia3=[i.text for i in sPage3.find_all('div',class_='news-content')]
    
    titulares=titularesDefinitivos1+titularesDefinitivos2+titularesDefinitivos3
    autores=autores1+autores2+autores3
    enlaces=enlace1+enlace2+enlace3
    fuenteNoticias=fuenteNoticia1+fuenteNoticia2+fuenteNoticia3
    FechaYHoras=FechaYHora1+FechaYHora2+FechaYHora3
    FechaYHoras=metodoAuxiliarFechas(FechaYHoras)
    cuerpoDeLaNoticias=cuerpoDeLaNoticia1+cuerpoDeLaNoticia2+cuerpoDeLaNoticia3
    
    
    schema = Schema(titular=TEXT(stored=True),autor=TEXT(stored=True),enlace=TEXT(stored=True),fuenteNoticia=TEXT(stored=True),FechaYHora=DATETIME(stored=True),cuerpoNoticia=TEXT(stored=True))
    if not os.path.exists("Practica2Whoosh"):
        os.mkdir("Practica2Whoosh")
    ix = create_in("Practica2Whoosh", schema)
    writer = ix.writer()
    for i in range(len(titulares)):
        writer.add_document(titular=u(titulares[i]), autor=u(autores[i]),enlace=u(enlaces[i]), fuenteNoticia=u(fuenteNoticias[i]),FechaYHora=u(FechaYHoras[i]),cuerpoNoticia=u(cuerpoDeLaNoticias[i]))
    writer.commit()
    messagebox.showinfo( "Base Datos", "Se han creado \n " + str(len(cuerpoDeLaNoticias)) + " registros")
    
def metodoAuxiliarFechas(Fecha):
    list=[]
    for item in Fecha:
        date_object = datetime.strptime(item, '%H:%M %m-%d-%Y')
        list.append(date_object )
    return list 

def metodoFechaYHora(timesTamps):
    list=[]
    for i in range(len(timesTamps)):
        if i%2 == 0:
          list.append(datetime.utcfromtimestamp(int(timesTamps[i])).strftime('%H:%M %m-%d-%Y'))
        
    return list

def metodoFuenteNoticia(titulares):
    lista=[]
    for item in titulares:
        item=(item.split("   por")[1])
        if item.split()[2] == "publicado:" :
            lista.append("meneame.net")
        else:
            lista.append(item.split()[2])
    return lista

def metodoEnlaces(l):
    enlaces=[]
    todo= [i for i in l.findAll('div', class_="center-content")]
    for item in todo:
        enlaces.append(item.find('a')['href'])
    return enlaces

def metodoAutores(titulares):
    todo= [i.text for i in titulares.findAll('div', class_="news-submitted")]
    lista=[autor.split()[1] for autor in todo]
    return lista

def metodosTitulares(titulares):
    lista=[]
    for item in titulares:
        item=(item.split('      ')[0])
        lista.append(item.split('     ')[0])
    return lista

def ventanaPrincipal():    
    top = Tk()
    
    menubar = Menu(top)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Cargar", command=creaIndexYEsquemaYScrapy)
    filemenu.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Datos", menu=filemenu)
    
    searchmenu = Menu(menubar, tearoff=0)
    searchmenu.add_command(label="Noticia", command=buscarPorTitularoCuerpoNoticia)
    searchmenu.add_command(label="Fuente", command=buscarPorFuente)
    searchmenu.add_command(label="Fechas", command=buscarPorFechas)
    menubar.add_cascade(label="Búsquedas", menu=searchmenu)
    
    top.config(menu=menubar)
    top.mainloop()
    
def buscarPorFuente():
    def listarBusqueda(event):
        ix=open_dir("Practica2Whoosh")
        a=en.get()
        with ix.searcher() as searcher:
            query = QueryParser("fuenteNoticia", ix.schema).parse(u(a))
            resultsPorTitularoCuerpoNoticia = searcher.search(query)
            print(resultsPorTitularoCuerpoNoticia)
            listaNoticias=[]
            for res in resultsPorTitularoCuerpoNoticia:
                listaAuxiliar=[]
                listaAuxiliar.append(res['titular'])
                listaAuxiliar.append(res['autor'])
                listaAuxiliar.append(res['fuenteNoticia'])
                print(res['FechaYHora'])
                listaNoticias.append(listaAuxiliar)
            mostrarPorPantalla1(listaNoticias)
            
    v = Toplevel()
    lb = Label(v, text="Introduzca la palabra a buscar en la fuente: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listarBusqueda)
    en.pack(side = LEFT)   
    
def buscarPorFechas():
    def listarBusqueda(event):
        ############
        en1=en.get()
        t=en1.split()
        horasYMinutos=t[0].split(":")
        Hora=horasYMinutos[0]
        Minutos=horasYMinutos[1]
        Mes=t[1]
        Dia=t[2]
        Año=t[3]
        ############
        ix=open_dir("Practica2Whoosh")
        with ix.searcher() as searcher:
            fecha=str(Año)+str(Mes)+str(Dia)+str(Hora)+str(Minutos)
            Horaa=str(datetime.now()).split()[0].split("-")
            minutoss=str(datetime.now()).split()[1].split(":")
            FechaCompletaActual=Horaa[0]+Horaa[1]+Horaa[2]+minutoss[0]+minutoss[1]

            query = QueryParser("titular", schema=ix.schema).parse(u"FechaYHora:["+ fecha +"to"+ FechaCompletaActual+"]")
            resultsPorTitularoCuerpoNoticia = searcher.search(query)
            listaNoticias=[]
            for res in resultsPorTitularoCuerpoNoticia:
                #if (datee.time()<res['FechaYHora'].time()):
                    listaAuxiliar=[]
                    listaAuxiliar.append(res['titular'])
                    listaAuxiliar.append(res['autor'])
                    listaAuxiliar.append(res['FechaYHora'])
                    listaNoticias.append(listaAuxiliar)
            mostrarPorPantalla1(listaNoticias)
            
    v = Toplevel()
    lb = Label(v, text="Introduzca la fecha (HH:MM MM DD AAAA): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listarBusqueda)    
    en.pack(side = LEFT)    
    
def buscarPorTitularoCuerpoNoticia():
    def listarBusquedaa(event):
        ix=open_dir("Practica2Whoosh")
        a=en.get()
        with ix.searcher() as searcher:
            query=Or([Term("titular", u(a)), Term("cuerpoNoticia", u(a))])
            resultsPorTitularoCuerpoNoticia = searcher.search(query)
            listaNoticias=[]
            for res in resultsPorTitularoCuerpoNoticia:
                listaAuxiliar=[]
                print(str(res['FechaYHora']).split())
                listaAuxiliar.append(res['titular'])
                listaAuxiliar.append(res['cuerpoNoticia'])
                listaAuxiliar.append(res['enlace'])
                listaNoticias.append(listaAuxiliar)
            mostrarPorPantalla1(listaNoticias)
    v = Toplevel()
    lb = Label(v, text="Introduzca la palabra a buscar en el título o en la noticia: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listarBusquedaa)
    en.pack(side = LEFT)    

def mostrarPorPantalla1(lista):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in lista:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

    

if __name__ == "__main__":
    ventanaPrincipal()
    #buscarPorFechas()
