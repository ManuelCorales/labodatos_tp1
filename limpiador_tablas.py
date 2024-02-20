
import pandas as pd
from inline_sql import sql, sql_val
from pandas import DataFrame


"""
    Tabla pais:
    id(PK) → (nombre, PBI, región)

    Tabla sedes:
    id(PK) →(pais_id(FK), estado)

    Tabla secciones:
    id(PK) → (id_sede(FK))
    
    Tabla red social:
    {id_sede(FK), tipo} → URL
"""

def main():
    carpetaOriginal = "./csv_originales/" 
    carpetaDump = "./csv_limpios/"

    limpiarTablaSecciones(carpetaOriginal, carpetaDump)
    


def limpiarTablaSecciones(carpetaOriginal, carpetaDump):
    seccionesCsv = pd.read_csv(carpetaOriginal + "lista-secciones.csv")
    query= """
                SELECT
                    s.sede_id AS id_sede
                FROM seccionesCsv as s
    """

    secciones: DataFrame = ejecutarQuery(query)
    crearTabla(secciones, carpetaDump, "secciones.csv", agregarCampoId = True)


def crearTabla(df: DataFrame, carpetaDump: str, nombreArchivo: str, agregarCampoId = False):
    df.to_csv(carpetaDump + nombreArchivo, index = agregarCampoId, index_label="id")


def ejecutarQuery(query: str) -> DataFrame:
    return sql^query

if(__name__ == "__main__"):
    main()