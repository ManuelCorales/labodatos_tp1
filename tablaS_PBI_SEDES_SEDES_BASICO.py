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
carpeta = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_originales/"

pais_PBI = pd.read_csv(carpeta + "PBI.csv")
paises_regiones= pd.read_csv(carpeta+ "paises_regiones.csv")
sedes= pd.read_csv(carpeta+ "lista-sedes.csv")
datos_sedes= pd.read_csv(carpeta+ "lista-sedes-datos.csv") ##no puedo cargar esta tabla
secciones = pd.read_csv(carpeta+"lista-secciones.csv")


                         #////////////////////////////#
                         #                 PAIS - PBI #
                         #////////////////////////////#

#Nos quedamos con los datos de 2022
#Para poder hacer la consultaSQL tuve que cambiar los nombres de las columnas
consultaSQL= """
                SELECT pp.Country_Code AS 'id',
                    pp.Country_Name AS 'nombre',
                       veinte_22 AS 'PBI',
                       pr.Region
                FROM pais_PBI AS pp
                INNER JOIN paises_regiones AS pr
                ON pp.Country_Code = pr.Country_Code
                WHERE "veinte_22" IS NOT NULL
           """
pbi_2022= sql^consultaSQL


#le agregue la region como atributo
#////////////PARA GQM /////////////////////////////////////////////////////
consultaSQL = """
            SELECT COUNT(*)
            FROM pbi_2022 as o
            WHERE o.PBI<=0 OR o.PBI > 0
            
            """
CAntidad_datos_conPBI= sql^consultaSQL 
consultaSQL = """
            SELECT COUNT(*)
            FROM pbi_2022 as o
   
            """
cantidad_total_datos = sql^consultaSQL

datos_sin_info= 266-244

porcentaje_de_datos_sin_info= datos_sin_info/266 *100

Cantidad_datos_conPBI= sql^consultaSQL 
consultaSQL = """
             SELECT id
             FROM pbi_2022 as o
             WHERE id NOT IN (
            SELECT id
            FROM pbi_2022 AS P
            WHERE P.PBI<=0 OR P.PBI > 0
               )
    
             """
paises_sin_datos = sql^consultaSQL
             
consultaSQL = """
             SELECT pais_iso_3 AS 'id'
             FROM sedes 
             WHERE id  IN (
            SELECT id
            FROM paises_sin_datos
               )
    
             """

sedes_en_paises_sin_Pbi = sql^consultaSQL
#////////////PARA GQM /////////////////////////////////////////////////////

  #////////////////////////#
  #           TABLA SEDES  #
  #////////////////////////#



consultaSQL= """
                SELECT sede_id AS 'id',
                      pais_iso_3 AS pais_id, 
                      estado
                       
                FROM sedes
           """
sedes_2= sql^consultaSQL


#//////////////////////////////////////////////////////////////////////////
