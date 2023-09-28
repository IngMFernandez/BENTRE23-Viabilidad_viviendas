#! /usr/bin/python3

#Globalmente, el programa lo que debiera hacer es abrir un conjunto de archivos demandado por el input y armar un diccionario de tarifas con todos los tipos.
#Las funciones que debería tener esto descompuesto son: 
#1. Función que muestre en pantalla posibles archivos a abrir y con el numpad permita su selección, se retorne el nombre de archivo.
#?. Evaluar alguna función que transforme la macro lista en int si fuera posible, googlear soluciones ya hechas.
    
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
import os
import csv
import pprint

def generador_de_lista(nombre_archivo): #Con el el string del archivo seleccionado, abrirlo, y pasar sus datos a  una lista matricial de dos dimensiones, retornar esa lista.
    logging.debug('Voy a abrir: '+nombre_archivo)
    lector_csv=csv.reader(open(nombre_archivo),delimiter=';')
    lista=list(lector_csv)
    logging.debug('Armé la siguiente lista: '+str(lista))
    return lista

def segmentador_de_nivel(primer_fila_en_formato_lista): #función que lea la primer fila del csv original/primer lista de la matriz y arme un diccionario de niveles, que se retorna.
    db_tarifas_solo_niveles={}
    for celda in primer_fila_en_formato_lista:
        if celda != '':
            db_tarifas_solo_niveles.setdefault(int(celda),{})
    return db_tarifas_solo_niveles

def contador_whitespaces_per_nivel(primer_fila_en_formato_lista): #Aunque es ineficiente,lee la primer fila del csv original/primer lista de la matriz y arma otro diccionario de niveles, indicando para cada nivel la cantidad de celdas vacías.
    db_qt_wspaces_per_nivel={}
    for celda in primer_fila_en_formato_lista:
        if celda == '':
                db_qt_wspaces_per_nivel[list(db_qt_wspaces_per_nivel.keys())[-1]] = db_qt_wspaces_per_nivel[list(db_qt_wspaces_per_nivel.keys())[-1]] + 1
        else:
            db_qt_wspaces_per_nivel.setdefault(int(celda),0)
        logging.debug('cantidad de blancos: '+str(db_qt_wspaces_per_nivel))
    return db_qt_wspaces_per_nivel

def localizador_de_posiciones(diccionario_con_niveles_definidos,primer_fila_en_formato_lista): #obtiene un diccionario de las posiciones en columna de cada uno de los niveles
    locacion_en_columna_de_cada_nivel={}
    for nivel in diccionario_con_niveles_definidos.keys():
        locacion_en_columna_de_cada_nivel.setdefault(nivel,primer_fila_en_formato_lista.index(str(nivel)))
        logging.debug(locacion_en_columna_de_cada_nivel)
    return locacion_en_columna_de_cada_nivel

def calculador_cantidad_de_sub_niveles_por_nivel(db_qt_wspaces_por_nivel):
    diccionario_de_cantidad_de_sub_niveles_por_nivel={}
    for nivel in db_qt_wspaces_por_nivel:
        diccionario_de_cantidad_de_sub_niveles_por_nivel.setdefault(nivel,int((dicc_qt_wspace[nivel]+1)/2))
    return diccionario_de_cantidad_de_sub_niveles_por_nivel
    
def calculador_posiciones_a_recorrer_por_nivel(diccionario_de_cantidad_de_sub_niveles,diccionario_con_niveles_definidos): #Aunque sea ineficiente, una función que lea la primer fila del csv original/primer lista de la matriz y armé otro diccionario de niveles, contando para cada nivel la cantidad de celdas a recorrer.
    diccionario_de_posiciones_a_recorrer_por_nivel={}
    for nivel in diccionario_con_niveles_definidos:
        diccionario_de_posiciones_a_recorrer_por_nivel.setdefault(nivel,diccionario_de_cantidad_de_sub_niveles[nivel]*2)
    return diccionario_de_posiciones_a_recorrer_por_nivel

#La gran función principal que tome la matriz del archivo csv (lista de python), el diccionario vacío de niveles , el diccionario de cantidad a recorrer y diccionario de posiciones de niveles y arme el diccionario con subniveles y tarifas.
def macro_armadora_de_subtablas(lista_de_datos_extraidos,diccionario_de_posiciones_a_recorrer_por_nivel,locacion_en_columna_de_cada_nivel,diccionario_con_niveles_definidos):
    diccionario_a_retornar=diccionario_con_niveles_definidos
    for nivel in diccionario_con_niveles_definidos.keys():
        logging.debug('posicion de nivel: '+str(locacion_en_columna_de_cada_nivel[nivel]))
        logging.debug('cantidad a recorrer: '+str(diccionario_de_posiciones_a_recorrer_por_nivel[nivel]))

        for indice in range(diccionario_de_posiciones_a_recorrer_por_nivel[nivel]):
            posicion_columna=locacion_en_columna_de_cada_nivel[nivel]+indice
            logging.debug('posicion columna: '+str(posicion_columna))
            try:
                if int(lista_de_datos_extraidos[1][posicion_columna]) in diccionario_con_niveles_definidos[nivel].keys(): # Acá es donde empieza el problema de por que se hizo una función con dos for loop, la solucion encontrada necesita en la parte más micro citar al diccionario general 
                    nro_de_fila=2
                    columna_sub_nivel=posicion_columna
                    sub_nivel=int(lista_de_datos_extraidos[1][columna_sub_nivel])
                    logging.debug('valor en celda: '+str(lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel]))
                    try:
                        while lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel] != '':
                                try:
                                    diccionario_a_retornar[nivel][sub_nivel].setdefault(int(lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel]),float(lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel+1]))
                                    nro_de_fila=nro_de_fila+1
                                except ValueError:
                                    diccionario_a_retornar[nivel][sub_nivel].setdefault(lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel],float(lista_de_datos_extraidos[nro_de_fila][columna_sub_nivel+1]))
                                    nro_de_fila=nro_de_fila+1
                    except IndexError:
                        continue
            except ValueError: #solucion horrible!!! Hay que encontrar una alternativa mas inteligente a tener que depender de error.
                continue
            logging.debug(diccionario_a_retornar)
    return  diccionario_a_retornar

os.chdir(os.path.join('.','pruebas_tarifas'))
logging.debug('Estoy en la carpeta '+os.getcwd())
 
diccionario_a_guardar={}
for fil in list(os.walk(os.path.abspath('.')))[0][2]:
    logging.debug(fil)
lista_de_archivos=list(os.walk(os.path.abspath('.')))[0][2]
logging.debug(lista_de_archivos)

for gran_index in range(len(lista_de_archivos)):
    logging.debug(lista_de_archivos[gran_index])
    datos_del_tipo= generador_de_lista(lista_de_archivos[gran_index])
    logging.debug(datos_del_tipo)
    logging.debug(datos_del_tipo[0])
    db_tarifas=segmentador_de_nivel(datos_del_tipo[0])
    dicc_qt_wspace=contador_whitespaces_per_nivel(datos_del_tipo[0])
    logging.debug('cantidad de blancos: '+str(dicc_qt_wspace))
    diccionario_de_posiciones_de_nivel=localizador_de_posiciones(db_tarifas,datos_del_tipo[0])                                               
    dicc_qt_sub_niveles=calculador_cantidad_de_sub_niveles_por_nivel(dicc_qt_wspace)
    logging.debug('cantidad de sub niveles: '+str(dicc_qt_sub_niveles)) 
    logging.debug(datos_del_tipo[1])
    for level in db_tarifas.keys():
        for index in range(dicc_qt_wspace[level]):
            if datos_del_tipo[1][diccionario_de_posiciones_de_nivel[level]+index] != '':
                db_tarifas[level].setdefault(int(datos_del_tipo[1][diccionario_de_posiciones_de_nivel[level]+index]),{})

    logging.debug(db_tarifas)
    diccionario_de_posiciones_a_recorrer_por_nivel=calculador_posiciones_a_recorrer_por_nivel(dicc_qt_sub_niveles,db_tarifas)
    nombre_del_tipo=lista_de_archivos[gran_index].split('.')[0]
    diccionario_a_guardar.setdefault(nombre_del_tipo,macro_armadora_de_subtablas(datos_del_tipo,diccionario_de_posiciones_a_recorrer_por_nivel,diccionario_de_posiciones_de_nivel,db_tarifas))

logging.debug(diccionario_a_guardar)
os.chdir('..')
print('Transcribiendo resultado a diccionarios python')
archivo_python_de_tarifas=open('Tarifas_Electricidad_Santa_Fe_diccionarios.py','w')
archivo_python_de_tarifas.write('Datos = '+pprint.pformat(diccionario_a_guardar))
archivo_python_de_tarifas.close()



