#! /usr/bin/python3


import os
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
import Tarifas_Electricidad_Santa_Fe_diccionarios #la  proxima selecciona un nombe más corto!!!
import pyperclip

def seleccion_de_tipo(diccionario):
    print('Hola, elegí el tipo de usuario:')
    for indice in range(len(diccionario.keys())):
        print(str(indice)+'- '+(list(diccionario.keys())[indice]))
    indice_tipo=int(input('Elija con un valor numérico '))
    tipo_electo=list(Tarifas_Electricidad_Santa_Fe_diccionarios.Datos.keys())[indice_tipo]
    logging.debug('Se selecciono el tipo '+tipo_electo)
    dicc_electo=diccionario[tipo_electo]
    return dicc_electo

def seleccion_de_nivel(diccionario_electo):
    print('Este tipe de usuario puede ser de los siguientes niveles: ')
    for nivel in diccionario_electo:
        print(str(nivel))
    nivel_seleccionado=int(input('Seleccione un nivel: '))
    diccionario_operativo=diccionario_electo[nivel_seleccionado]
    logging.debug(diccionario_operativo)
    logging.debug(list(diccionario_operativo))
    logging.debug(list(diccionario_operativo.keys()))
    return diccionario_operativo

def definicion_de_sub_nivel(lista_de_sub_niveles,diccionario_de_un_nivel, energia_consumida):
    for sub_nivel in lista_de_sub_niveles:
        logging.debug(sub_nivel)
        if energia_consumida> float(sub_nivel):
            dicc_operativo=diccionario_de_un_nivel[sub_nivel]
            break
        else:
            continue
    return dicc_operativo
def calculador_monto (diccionario_computo,energia_consumida):
    monto_fijo=diccionario_computo[0]
    logging.debug(monto_fijo)
    lista_de_keys=list(diccionario_computo.keys())
    logging.debug(lista_de_keys)
    indice_final=1
    while lista_de_keys[indice_final] != 'else':
        logging.debug(lista_de_keys[indice_final])
        if lista_de_keys[indice_final]<energia_consumida:
            logging.debug(dicc_operativo[lista_de_keys[indice_final]])
            logging.debug(lista_de_keys[indice_final])
            logging.debug(lista_de_keys[indice_final-1])
            monto_fijo= monto_fijo+(dicc_operativo[lista_de_keys[indice_final]]*(lista_de_keys[indice_final]-lista_de_keys[indice_final-1]))        
            logging.debug(monto_fijo)
            indice_final=indice_final+1
        else:
            break
    logging.debug(lista_de_keys[indice_final])
    monto_variable= diccionario_computo[lista_de_keys[indice_final]]*(energia_consumida-lista_de_keys[indice_final-1])
    logging.debug(monto_variable)
    monto=monto_variable+monto_fijo
    logging.debug(monto)
    return monto
        
dicc_main=seleccion_de_tipo(Tarifas_Electricidad_Santa_Fe_diccionarios.Datos)
logging.debug(dicc_main)
dicc_nivel=seleccion_de_nivel(dicc_main)
sub_niveles=(list(dicc_nivel.keys()))
sub_niveles.reverse()
logging.debug(sub_niveles)
energia_consumida=float(input('Cuanta energía se consumió en el mes?[kWh] '))
dicc_operativo=definicion_de_sub_nivel(sub_niveles,dicc_nivel,energia_consumida)
logging.debug(dicc_operativo)
pyperclip.copy(calculador_monto(dicc_operativo,energia_consumida))
