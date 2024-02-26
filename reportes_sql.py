# -*- coding: utf-8 -*-
"""
Materia     : Laboratorio de datos - FCEyN - UBA
Grupo       : Grupo 2
Detalle     : 
    En este documento se realizan los reportes correspondientes al ejercicio h
    Las tablas resultantes se almacenan en la carpeta material_suplementario
    para despues poder hacer referencia en el informe escrito
Autores     : Corales, Biasoni y Soler
"""

#%%
# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val


# material_suplementario = "C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/material_suplementario"             
material_suplementario = "./material_suplementario"             
# carpeta= "/home/oem/Desktop/uni/TP1/labodatos_tp1/csv_limpios/"
carpeta = "./TablasLimpias/"

def main():
<<<<<<< HEAD
   carpeta = "./csv_limpios/"
   paises = pd.read_csv(carpeta+"paises.csv")
   redes_sociales = pd.read_csv(carpeta+"redes_sociales.csv")
   secciones = pd.read_csv(carpeta+"secciones.csv")
   sedes = pd.read_csv(carpeta+"sedes.csv")

   material_suplementario = "C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/material_suplementario"             
=======
    paises = pd.read_csv(carpeta+"paises.csv")
    redes_sociales = pd.read_csv(carpeta+"redes_sociales.csv")
    secciones = pd.read_csv(carpeta+"secciones.csv")
    sedes = pd.read_csv(carpeta+"sedes.csv")
    reporte1()
    reporte2()
    reporte3()
    reporte4()
>>>>>>> 685257725f23b7787e2c7c2cd5a9625f35cb9451

  
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

    # Almacenamos el reporte
    
    # Especifica la ruta del archivo CSV en la carpeta material_complementario
    ruta_archivo_csv = material_suplementario + "/tabla1.csv"

    # Almacenar el DataFrame en un archivo CSV en la carpeta material_complementario
    reporte_1.to_csv(ruta_archivo_csv, index=False)

#%%
def reporte2():
    reporte_2 = sql^"""
        SELECT p.Region, COUNT() AS 'Paises Con Sedes Argentinas', AVG(p.PBI) AS 'Promedio PBI per Cápita 2022 (U$S)'
        FROM paises AS p
        INNER JOIN sedes AS s
        ON p.id = s.pais_id
        GROUP BY p.Region
        ORDER BY AVG(p.PBI) DESC
    """

    # Almacenamos el reporte
    
    # Especifica la ruta del archivo CSV en la carpeta material_complementario
    ruta_archivo_csv = material_suplementario + "/tabla2.csv"

    # Almacenar el DataFrame en un archivo CSV en la carpeta material_complementario
    reporte_2.to_csv(ruta_archivo_csv, index=False)

#%%

def reporte3():
    consultasql = sql^"""
        SELECT DISTINCT rs.tipo, s.pais_id
        FROM sedes AS s
        INNER JOIN redes_sociales AS rs
        ON rs.id_sede = s.id
        GROUP BY s.pais_id, rs.tipo
    """

    # ya que tenemos agrupado por pais, tipo de red (y contamos para que no aparezca)
    # por ejemplo, facebook chile dos veces
    # vamos a contar cuantas veces aparece el pais_id


    reporte_3 = sql^"""
                SELECT c.pais_id, COUNT(tipo) AS 'cantidad_de_tipos_de_redes'
                FROM consultasql AS c
                GROUP BY c.pais_id
                """             
    # Almacenamos el reporte
    
    # Especifica la ruta del archivo CSV en la carpeta material_complementario
    ruta_archivo_csv = material_suplementario + "/tabla3.csv"

    # Almacenar el DataFrame en un archivo CSV en la carpeta material_complementario
    reporte_3.to_csv(ruta_archivo_csv, index=False)
           
  


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

    # Almacenamos el reporte
    
    # Especifica la ruta del archivo CSV en la carpeta material_complementario
    ruta_archivo_csv = material_suplementario + "/tabla4.csv"

    # Almacenar el DataFrame en un archivo CSV en la carpeta material_complementario
    reporte_4.to_csv(ruta_archivo_csv, index=False)

  
if(__name__ == "__main__"):
  main()