import pandas as pd
from inline_sql import sql, sql_val
from pandas import DataFrame
import matplotlib.pyplot as plt


carpetaCvs = "./csv_limpios/"

def main():
    plotearSedesPorRegion()

def plotearSedesPorRegion():
    sedes = pd.read_csv(carpetaCvs + "sedes.csv")
    paises = pd.read_csv(carpetaCvs + "paises.csv")

    query = """
        SELECT
            p.region AS region,
            count(p.region) AS cantidad_sedes
        FROM sedes s
        INNER JOIN paises p ON p.id = s.pais_id
        GROUP BY p.region 
        ORDER BY cantidad_sedes asc;
    """

    resultado = ejecutarQuery(query)
    fig, ax = plt.subplots()    # fig.savefig('yourfilename.png')
    plt.rcParams['font.family'] = 'sans-serif'
    ax.barh(data=resultado, 
           y='region',
           width='cantidad_sedes',
          )
    ax.set_title('Cantidad de sedes argentinas por región')
    ax.set_xlabel('Región (en inglés)', fontsize='medium')
    ax.set_ylabel('Cantidad de sedes', fontsize='medium')

    plt.show()

def ejecutarQuery(query: str) -> DataFrame:
    return sql^query


if(__name__ == "__main__"):
  main()