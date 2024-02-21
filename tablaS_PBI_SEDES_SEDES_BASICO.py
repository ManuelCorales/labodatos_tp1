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
from pandas import DataFrame

###Cargar tablas###
carpeta =  "/home/oem/Desktop/uni/TP1/"
pais_PBI = pd.read_csv(carpeta + "PBI.csv")
paises_regiones= pd.read_csv(carpeta+ "paises_regiones.csv")
sedes= pd.read_csv(carpeta+ "lista_sedes.csv")
datos_sedes= pd.read_csv(carpeta+ "lista_sedes_datos.csv") ##no puedo cargar esta tabla
secciones = pd.read_csv(carpeta+"lista_secciones.csv")


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
                WHERE "veinte_22" IS NOT NULL AND Region IS NOT NULL
           """
Pais = sql^consultaSQL

Pais.to_csv('/home/oem/Desktop/uni/TP1/labodatos_tp1/csv_limpios/' +'Pais.csv' )

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
                      pais_iso_3 AS pais_id
            
                FROM sedes
                WHERE sedes.estado = 'Activo'
           """
Sedes= sql^consultaSQL
#las sede con estado inactivo no las cuento 
Sedes.to_csv('/home/oem/Desktop/uni/TP1/labodatos_tp1/csv_limpios/' +'Sedes.csv' )



    
#//////////////////////////////////////////////////////////////////////////
prueba = sql^"""
      SELECT id 
      FROM Pais
      WHERE Pais.Region IS NULL
         """
prueba2= sql^"""
        SELECT prueba.id
        FROM  prueba
        INNER JOIN Sedes
        ON prueba.id= pais_id
        """
#como habia muchos datos en la tabla pais que tenian la region incompleta (ademas de que el pais no era un pais sino una region)
#nos fijamos si alguno de estos tenian sedes argentinas y como no lo hacian, 
#decidimos descartar los mismos 