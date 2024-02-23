# -*- coding: utf-8 -*-
"""
Materia     : Laboratorio de datos - FCEyN - UBA
Grupo       : Grupo 2
Detalle     : 
    En este documento se realizan los reportes del punto h)
    El mismo fue agrupado en funciones con nombres representativos
Autores     : Corales, Biasoni y Soler
"""

#%%
# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val

def main():
    # carpeta = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_limpios/"
    # carpeta = "/home/oem/Desktop/uni/TP1/labodatos_tp1/csv_limpios/"
    carpeta = "./csv_limpios/"

    paises = pd.read_csv(carpeta+"paises.csv")
    redes_sociales = pd.read_csv(carpeta+"redes_sociales.csv")
    secciones = pd.read_csv(carpeta+"secciones.csv")
    sedes = pd.read_csv(carpeta+"Sedes.csv")

    reporte1()
    reporte2()
    reporte3()
    reporte4()

#%%
def reporte1():
    # primero unimos pais con sedes por medio del id_pais, y guardamos el resultado
    pais_sedes = sql^"""
        SELECT p.nombre, COUNT(*) AS 'cantidad_de_sedes', p.PBI AS 'PBI', p.id
        FROM paises AS p
        JOIN sedes AS s
        ON p.id = s.pais_id
        GROUP BY p.nombre, p.PBI, p.id
    """
    # ahora,  hago una tabla con la cantidad de secciones por paises
    secciones_por_pais = sql^"""
        SELECT pais_id,
        COUNT(sc.id) AS "cantidad_de_secciones"
        FROM secciones sc
        JOIN sedes AS sd
        ON sd.id = sc.id_sede
        GROUP BY pais_id
    """

    # hago otra tabla que tome la columna de 'cantidad_de_sedes' de pais_sedes y la columna 
    #'cantidad_de_secciones' de secciones_por _pais y las divido secciones/sede
    secciones_promedios = sql^"""
        SELECT pais_id,
        sp.cantidad_de_secciones/ps.cantidad_de_sedes AS 'secciones_promedio'
        FROM secciones_por_pais sp
        JOIN pais_sedes ps
        ON ps.id= sp.pais_id
    """

    reporte_1 = sql^"""
        SELECT nombre, cantidad_de_sedes AS 'sedes',
        secciones_promedio, PBI AS 'PBI per Cápita 2022 (U$S)'
        FROM pais_sedes AS ps
        JOIN secciones_promedios AS sc
        ON sc.pais_id = ps.id
    """


#%%
def reporte2():
    consultasql = sql^"""
        SELECT p.Region, COUNT() AS 'Paises Con Sedes Argentinas', AVG(p.PBI) AS 'Promedio PBI per Cápita 2022 (U$S)'
        FROM paises AS p
        INNER JOIN sedes AS s
        ON p.id = s.pais_id
        GROUP BY p.Region
        ORDER BY AVG(p.PBI) DESC
    """


#%%
def reporte3():
    consultasql = sql^"""
        SELECT DISTINCT rs.tipo, s.pais_id 
        FROM sedes AS s
        JOIN redes_sociales AS rs
        ON rs.id_sede = s.id
        GROUP BY s.pais_id, rs.tipo
    """
    # ya que tenemos agrupado por pais, tipo de red (y contamos para que no aparezca)
    # por ejemplo, facebook chile dos veces
    # vamos a contar cuantas veces aparece el pais_id

    rs_paises = sql^"""
        SELECT c.pais_id, COUNT(tipo) AS 'tipos de redes'
        FROM consultasql AS c
        GROUP BY c.pais_id
    """


#%%
def reporte4():
    sedes_pais = sql^"""
        SELECT s.id AS 'sede_id', p.nombre  
        FROM sedes AS s
        JOIN paises AS p
        ON s.pais_id= p.id
    """

    reporte_4= sql^"""
        SELECT sp.nombre AS 'Pais', r.id_sede, r.tipo AS 'red social',
        r.url
        FROM redes_sociales AS r
        JOIN sedes_pais AS sp
        ON r.id_sede = sp.sede_id
    """


if(__name__ == "__main__"):
  main()