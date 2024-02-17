#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:05:45 2024

@author: Natali Biasoni

"""
                             #///////////#
                             # LIBRERIAS #
                             #///////////#

import numpy as np
import os
import pandas as pd 
from inline_sql import sql, sql_val

###Cargar tablas###
carpeta = "/home/oem/Desktop/uni/TP1/"


pais_PBI= pd.read_csv(carpeta+"PBI.csv")
paises_regiones= pd.read_csv(carpeta+ "paises_regiones.csv")
sedes= pd.read_csv(carpeta+ "lista_sedes.csv")
datos_sedes= pd.read_csv(carpeta+ "lista_sedes_datos.csv")
secciones = pd.read_csv(carpeta+"lista_secciones.csv")

                         #////////////////////////////#
                         # LIMPIAMOS TABLA PAIS - PBI #
                         #////////////////////////////#

#Nos quedamos con los datos de 2022
#Para poder hacer la consultaSQL tuve que cambiar los nombres de las columnas
consultaSQL= """
                SELECT Country_Name AS 'Pais',
                       Country_Code AS 'id',
                       Indicator_Name,
                       Indicator_Code,
                       vente_22 AS 'PBI'
                FROM pais_PBI
           """
pbi_2022= sql^consultaSQL


#REDONDEA LOS PBI NOSE SI ESTARA BIEN??

   #///////////////////////////////#
   # LIMPIAMOS TABLA PAIS - regions#
   #///////////////////////////////#
#no hay un codigo para identificar las regiones de los paises
   
consultaSQL= """
                SELECT Country_Code AS 'id_pais',
                       Region
                       
                FROM paises_regiones
           """
regiones_pais= sql^consultaSQL

