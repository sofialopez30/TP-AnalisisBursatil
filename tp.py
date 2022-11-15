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

def max_gain(accion,diccionario, fecha_venta):
    """
    Esta función encuentra el precio de la acción fue el menor (teniendo en cuanta la fecha de venta de la acción) y cual fue la ganancia entre el precio de venta y el precio de compra. 
    ENTRADAS: una de las acciones, el diccionario obtenido a partir de la función read_file(), y una fecha de venta para la acción. 
    SALIDAS: la fecha donde la acción tuvo el menor precio (teniendo en cuenta que tiene que ser antes de la fecha de venta de la acción), es decir la mejor fecha para comprar la acción, y la ganancia entre el precio de compra y el precio de venta.
    """
    fecha = []
    valores = []
    diccioconfechas = {}
    diccioconvalores = {}
    for fechas in diccionario.get("Date"):
        fecha.append(fechas)
    for valores_accion in diccionario.get(accion):
        valores.append(float(valores_accion))
    for dates, values in zip(fecha, valores):
        if dates not in diccioconfechas.keys():
            diccioconfechas[dates] = values
        if values not in diccioconvalores.keys():
            diccioconvalores[values] = dates
    valor_de_venta = diccioconfechas.get(fecha_venta)
    posicion_de_fecha = valores.index(valor_de_venta)
    valoresantesdelafecha = valores[0:posicion_de_fecha]
    mejor_valor_de_compra = min(valoresantesdelafecha)
    fecha_compra = diccioconvalores.get(mejor_valor_de_compra)
    ganancia = ((valor_de_venta-mejor_valor_de_compra)/mejor_valor_de_compra)
    return fecha_compra, ganancia

def report_max_gains(diccionario, fecha_venta):
    """
    Esta función escribe en un archivo de texto el resumen del rendimiento de la acción, a partir de la compra en una determinada fecha. 
    ENTRADA: el diccionario obtenido a partir de la función read_file() y una fecha de venta.
    SALIDA: esta función no retorna nada en sí, sino que escribe en un archivo de texto el resumen del rendimiento de la acción. En caso de que la acción tenga una ganancia negativa, informa tambien esto.
    """
    with open("resumen_mejor_compra.txt", "a", encoding="utf-8") as archivo: 
        fecha_compra, ganancia = max_gain(accion, diccionario,fecha_venta)
        escribir = f'{accion} genera una ganancia de {ganancia*100} % habiendo comprado en {fecha_compra} y vendiéndose en {fecha_venta}'
        if ganancia<0: 
            escribir = escribir + f'La acción {accion} solo genera perdidas'
        archivo.write(escribir)

def plot_price(accion, diccionario):
    '''
    Esta función tiene como objetivo obetener un gráfico de lineas acerca el precio de las acciones, fecha por fecha de dicha accion
    con el nombre price_MELI.png. 
    ENTRADA: una de las acciones, el diccionario obtenido a partir de la función read_file(), y una acción.
    SALIDA: un gráfico de lineas  acerca el precio de las acciones, fecha por fecha de dicha accion
    con el nombre price_MELI.png. 
    '''
    fecha = []
    valores = []
    diccioconfechas = {}
    for fechas in diccionario.get("Date"):
        fecha.append(fechas)
    for valores_accion in diccionario.get(accion):
        valores.append(float(valores_accion))
    for dates, values in zip(fecha, valores):
        if dates not in diccioconfechas.keys():
            diccioconfechas[dates] = values
    xpoint= list(diccioconfechas.keys())
    ypoints= list(diccioconfechas.values())
    plt.title = f"Precio de la acción {accion}"
    plt.plot(xpoint, ypoints)
    plt.show()

def monthly_average_bar_plot(acción, diccionario):
    """
    Esta función devuelve un gráfico de barras donde se muestra el promedio de la acción mes a mes. 
    ENTRADA: el nombre de una acción y el diccionario surgido a partir de read_file().
    SALIDA: un gráfico de barras con lo mencionado anteriormente. 
    """
    listademeses = []
    fechas, promedios = (monthly_average(accion, diccionario))
    for x in fechas:
        conversion = str2datetime(x)
        meses = f"{conversion.month}-{conversion.year}"
        listademeses.append(meses)
    plt.bar(listademeses, promedios, 0.5)
    plt.show()

def plot_max_gains(diccionario,fecha_venta):
    """
    Esta función genera un gráfico de barras con las ganancias que se tienen por cada acción si se venden en un día determinado. 
    ENTRADA: el diccionario obtenido a partir de la función read_file() y una fecha de venta.
    SALIDA: un gráfico de barras con las ganancias que cada acción genera si se venden en ese día determinado.
    """
    max = {}
    for clave in diccionario.keys():
        if clave !='Date':
            fecha_compra, ganancia = max_gain(clave, diccionario, fecha_venta)
            max[clave] = ganancia
    ypoints = max.values()
    xpoints = max.keys()
    plt.bar(xpoints, ypoints)
    plt.show()
    
""" >>>> ESCRIBAN SU CÓDIGO A PARTIR DE AQUÍ >>>> """

diccionario = read_file("/Users/chiarafacal/OneDrive/PENSAMIENTO COMPUTACIONAL/bolsa.csv")

fechas, promedios_mes = monthly_average("SATL", diccionario)

with open("monthly_average_SATL.csv", "a") as archivo: 
    fechas, promedio_mes = monthly_average("SATL", diccionario)
    for x in zip(fechas,promedio_mes):
        archivo.write(str(x) + "\n")

fecha_venta = "2022-06-06"
accion = "RTX"
fecha_compra, ganancia = max_gain("RTX", diccionario, fecha_venta)

report_max_gains(diccionario,fecha_venta)

plot_price("MELI", diccionario)

monthly_average_bar_plot('SATL', diccionario)




    

    

