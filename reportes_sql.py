# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:47:57 2024

@author: @soler
"""

#%%
# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val

def main():

    print()
    print("# =============================================================================")
    print("# Creamos/Importamos los datasets que vamos a utilizar en este programa")
    print("# =============================================================================")

    carpeta = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_limpios/"


    pais = pd.read_csv(carpeta+"Pais.csv")    
    redes_sociales = pd.read_csv(carpeta+"redes_sociales.csv")    
    secciones = pd.read_csv(carpeta+"secciones.csv")    
    sedes = pd.read_csv(carpeta+"sedes.csv") 

#%%
# =============================================================================
# PUNTO H.i (no lo pude terminar)
# =============================================================================
# primero unimos pais con sedes por medio del id_pais, y guardamos el resultado
   
    pais_sedes = sql^"""
                  SELECT p.nombre, COUNT(*) AS 'sedes', p.PBI AS 'PBI per Cápita 2022 (U$S)', p.id
                  FROM pais AS p
                  JOIN sedes AS s
                  ON p.id = s.pais_id
                  GROUP BY p.nombre, p.PBI, p.id
                  """   
# ahora,  traigo la tabla pais_sedes y le sumo cantidad de secciones en promedio 
# que pose en sus sedes

     sedes_secciones = sql^"""
                   SELECT sec.id_sede, sed.pais_id
                   FROM secciones AS sec
                   JOIN sedes AS sed
                   ON sec.id_sede = sed.id
                   """      
#%%
# =============================================================================
# PUNTO H.ii (terminado)
# =============================================================================

    consultasql = sql^"""
                  SELECT p.Region, COUNT() AS 'Paises Con Sedes Argentinas', AVG(p.PBI) AS 'Promedio PBI per Cápita 2022 (U$S)'
                  FROM pais AS p
                  INNER JOIN sedes AS s
                  ON p.id = s.pais_id
                  GROUP BY p.Region
                  ORDER BY AVG(p.PBI) DESC
                  """   
#%%
# =============================================================================
# PUNTO H.iii (terminado, creo)
# =============================================================================
    consultasql = sql^"""
                  SELECT rs.tipo, s.pais_id, COUNT()
                  FROM sedes AS s
                  JOIN redes_sociales AS rs
                  ON rs.id_sede = s.id
                  GROUP BY rs.tipo, s.pais_id
                  """  
# ya que tenemos agrupado por pais, tipo de red (y contamos para que no aparezca)
# por ejemplo, facebook chile dos veces
# vamos a contar cuantas veces aparece el pais_id

      rs_paises = sql^"""
                    SELECT c.pais_id, COUNT()
                    FROM consultasql AS c
                    GROUP BY c.pais_id
                    """             
