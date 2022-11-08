""" >>>> NO TOCAR ESTE CÓDIGO >>>> """

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def str2datetime(date, fmt="%Y-%m-%d"):
    """Convierte una cadena (o secuencia de cadenas) a tipo datetime (o secuencia de datetimes).

    ENTRADAS:
        date (str ó secuencia de str): fechas a convertir.
        fmt (str, opcional): formato de fecha (ver documentación de biblioteca datetime).
    SALIDAS:
        output (datetime ó secuencia de datetime): fechas convertidas a datetime.
    EJEMPLOS:
    >>>> date = str2datetime('2022-10-24')
    >>>> print(date.year, date.month, date.day)

    >>>> date = str2datetime(['2022-10-24', '2022-10-23', '2022-10-22'])
    >>>> print(len(date))"""
    if isinstance(date, str):
        return datetime.strptime(date, fmt)
    elif isinstance(date, (list, np.ndarray)):
        output = []
        for d in date:
            output.append(datetime.strptime(d, fmt))
        if isinstance(date, np.ndarray):
            output = np.array(output)
        return output


def datetime2str(date, fmt="%Y-%m-%d"):
    """Convierte un datetime (o secuencia de datetimes) a tipo str (o secuencia de str).

    ENTRADAS:
        date (datetime ó secuencia de datetime): fechas a convertir.
        fmt (str, opcional): formato de fecha (ver documentación de biblioteca datetime).
    SALIDAS:
        output (str ó secuencia de str): fechas convertidas a cadenas.
    EJEMPLOS:
    >>>> date_str = '2022-10-24'
    >>>> date = str2datetime(date_str)
    >>>> print(datetime2str(date) == date_str)"""
    if isinstance(date, datetime):
        return date.strftime(fmt)
    elif isinstance(date, (list, np.ndarray)):
        output = []
        for d in date:
            output.append(d.strftime(fmt))
        if isinstance(date, np.ndarray):
            output = np.array(output)
        return output


""" >>>> DEFINAN SUS FUNCIONES A PARTIR DE AQUÍ >>>> """

def read_file(archivo):
    """
    Toma un archivo csv y a partir de todas las columnas, crea un diccionario donde las claves son los nombres de las columnas y los valores son una lista de los datos de cada columna. 
    ENTRADA: archivo de tipo csv.
    SALIDA: ub diccionario con las claves y valores ya mencionados.
    """
    with open(archivo, 'r') as archivo: 
        diccio = {}
        for i, linea in enumerate(archivo): 
            if i==0: 
                lista = linea.strip().split(",")
                for valor in lista: 
                    diccio[valor] = []
            else: 
                lista2 = linea.strip().split(",")
                for llave, valores in zip(lista, lista2):
                    diccio[llave].append(valores)
    return diccio

def monthly_average(variable, diccionario):
    """
    Esta función toma una variable, que se supone que tiene que ser el nombre de las acciones de la bolsa, y el diccionario obtenido a partir de la función read_file(), y a partir de eso construye primero una lista con los primeros días de cada mes donde fueron registrados datos, que puede o no ser el día 1, y luego una lista con los promedios de la acción a lo largo de cada mes.
    ENTRADA: variable (el nombre de una acción), y el diccionario obtenido a partir de la función read_file().
    SALIDA: dos listas, una con la primera fecha de cada mes donde fueron registrados datos y la otra con el valor promedio de la acción, mes a mes. 
    """
    listadefechas = []
    listadevalores = []
    listafechas= []
    diccionariodefechas = {}
    diccionariodemeses = {}
    listapromedio = []
    for fechas in diccionario.get('Date'): 
        listadefechas.append(fechas)
        conversion = str2datetime(fechas)
        if conversion.month not in diccionariodefechas.keys():
            diccionariodefechas[conversion.month]= fechas
    for x in diccionariodefechas.values():
        listafechas.append(x)
    for valores in diccionario.get(variable):
        listadevalores.append(valores)
    for fechas1, valores in zip(listadefechas,listadevalores):
        conversion2 = str2datetime(fechas1)
        if conversion2.month not in diccionariodemeses.keys(): 
            diccionariodemeses[conversion2.month] = []
        else: 
            diccionariodemeses[conversion2.month].append(float(valores))
    for values in diccionariodemeses.values():
        calculo = sum(values)/len(values)
        listapromedio.append(calculo)
    return listafechas, listapromedio

""" >>>> ESCRIBAN SU CÓDIGO A PARTIR DE AQUÍ >>>> """

diccionario = read_file("/Users/sofialopezmoreno/Library/Mobile Documents/com~apple~CloudDocs/ipc/TP-AnalisisBursatil/bolsa.csv")

fechas, promedio_mes = monthly_average("SATL", diccionario)
with open("monthly_average_SATL.csv", "a") as archivo: 
    fechas, promedio_mes = monthly_average("SATL", diccionario)
    for x in zip(fechas,promedio_mes):
        archivo.write(str(x) + "\n")