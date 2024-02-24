# -*- coding: utf-8 -*-
"""
Materia     : Laboratorio de datos - FCEyN - UBA
Grupo       : Grupo 2
Detalle     : 
    En este documento se realiza el proceso de limpieza de las tablas
    El mismo fue agrupado en funciones con nombres representativos     
Autores     : Corales, Biasoni y Soler
"""

#%% Importacion de librerias
import pandas as pd
from inline_sql import sql, sql_val
from pandas import DataFrame


"""
    Tabla pais:
    id(PK) → (nombre, PBI, región)

    Tabla sedes:
    id(PK) →(pais_id(FK))

    Tabla secciones:
    id(PK) → (id_sede(FK))
    
    Tabla red social:
    {id_sede(FK), url} → tipo
"""

#%% carpetaOriginal contiene los csv sin limpiar
## Luego de ser limpiados, se almacenan en carpetaDump
# carpetaOriginal = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_originales/" 
# carpetaDump = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_limpios/"
carpetaOriginal = "./csv_originales/" 
carpetaDump = "./csv_limpios/"


def main():
    armarTablaSecciones()
    armarTablaRedes()
    armarTablaSedes()
    armarTablaPaises()



def armarTablaSedes():
    sedesCsv = pd.read_csv(carpetaOriginal + "lista-sedes.csv")
    query= """
                SELECT
                    sede_id AS 'id',
                    pais_iso_3 AS pais_id
                FROM sedesCsv
                WHERE estado = 'Activo'
    """

    sedes: DataFrame = ejecutarQuery(query)
    crearTabla(sedes, "sedes.csv", agregarCampoId = False)


def armarTablaPaises():
    paisesCsv = pd.read_csv(carpetaOriginal + "PBI.csv")
    paisesRegionesCsv = pd.read_csv(carpetaOriginal + "paises_regiones.csv")

    query= """
                SELECT 
                    pp.Country_Code AS 'id',
                    pp.Country_Name AS 'nombre',
                    pp."2022" AS 'PBI',
                    pr.Region AS 'region'
                FROM paisesCsv AS pp
                INNER JOIN paisesRegionesCsv AS pr
                ON pp.Country_Code = pr.Country_Code
                WHERE pp."2022" IS NOT NULL AND region IS NOT NULL
    """

    paises: DataFrame = ejecutarQuery(query)
    crearTabla(paises, "paises.csv")


def armarTablaSecciones():
    seccionesCsv = pd.read_csv(carpetaOriginal + "lista-secciones.csv")
    query= """
                SELECT
                    s.sede_id AS id_sede
                FROM seccionesCsv as s
    """

    secciones: DataFrame = ejecutarQuery(query)
    crearTabla(secciones, "secciones.csv", agregarCampoId = True)


def armarTablaRedes():

    # Redes que se tendrán en cuenta para clasificarlas según tipo
    tiposRedes = [
        "facebook",
        "twitter",
        "instagram",
        "linkedin",
        "youtube",
        "flickr"
    ]
    sedesCsv = pd.read_csv(carpetaOriginal + "lista-sedes-datos.csv")
    query= """
                SELECT
                    s.sede_id AS id_sede,
                    s.redes_sociales
                FROM sedesCsv as s
    """

    sedes: DataFrame = ejecutarQuery(query)

    # Creo un array donde ire agregando un array con las redes parseadas para cada sede
    redesPorSede = []
    for i, sede in sedes.iterrows():
        redesTrim = []
        
        redes = sede["redes_sociales"]
        if(redes == None):
            redesPorSede.append(redesTrim)
            continue

        redes = redes.split("// ")

        for red in redes:
            trimmedRed = red.strip()

            if(trimmedRed != ""):
                redesTrim.append(trimmedRed)

        redesPorSede.append(redesTrim)




    # Creo un nuevo df donde le asigno a cada sede su serie de redes parseadas
    redesSociales = DataFrame(columns=['id_sede', 'url', 'tipo'])
    for i, redes in enumerate(redesPorSede):
        for url in redes:
            redEncontrada = False
            for tipoRed in tiposRedes:
                if tipoRed in url:
                    sedeId = sedes.iloc[i]["id_sede"]

                    df = DataFrame({'id_sede': sedeId, 'url': url, 'tipo': tipoRed}, index=[0])
                    redesSociales = pd.concat([redesSociales, df])
                    redEncontrada = True
                    break
            if(redEncontrada == False):
                sedeId = sedes.iloc[i]["id_sede"]
                df = DataFrame({'id_sede': sedeId, 'url': url, 'tipo': 'desconocido'}, index=[0])
                redesSociales = pd.concat([redesSociales, df])

    crearTabla(redesSociales, "redes_sociales.csv")


def crearTabla(df: DataFrame, nombreArchivo: str, agregarCampoId = False):
    if(agregarCampoId):
        df.index += 1

    df.to_csv(carpetaDump + nombreArchivo, index = agregarCampoId, index_label="id")


def ejecutarQuery(query: str) -> DataFrame:
    return sql^query


if(__name__ == "__main__"):
    main()