"""
Materia     : Laboratorio de datos - FCEyN - UBA
Grupo       : Grupo 2
Detalle     : 
    En este documento se realizan las visualizaciones pedidas
    
Autores     : Corales, Biasoni y Soler

"""
#%% Importacion de librerias
import pandas as pd
from inline_sql import sql, sql_val
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker 

carpetaCvs = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_limpios/"

def main():
    plotearSedesPorRegion()
    visualizacion2()
    visualizacion3()

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
    # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)
    #Creamos el grafico
    fig, ax = plt.subplots()    # fig.savefig('yourfilename.png')
    plt.rcParams['font.family'] = 'sans-serif'
    ax.barh(data=resultado, 
           y='region',
           width='cantidad_sedes',
          )
    ax.set_title('Cantidad de sedes argentinas por región')
    ax.set_ylabel('Región (en inglés)', fontsize='medium')
    ax.set_xlabel('Cantidad de sedes', fontsize='medium')

    plt.show()

def ejecutarQuery(query: str) -> DataFrame:
    return sql^query

#%% 
#Boxplot, por cada región geográfica, del PBI per cápita 2022 de los países
#donde Argentina tiene una delegación. Mostrar todos los boxplots en una
#misma figura, ordenados por la mediana de cada región.


def visualizacion2():
    sedes = pd.read_csv(carpetaCvs + "sedes.csv")
    paises = pd.read_csv(carpetaCvs + "paises.csv")

    query = """
        SELECT
            p.region AS region,
            PBI AS 'PBI per capita 2022',
        FROM sedes s
        INNER JOIN paises p ON p.id = s.pais_id
        ORDER BY p.region ASC
    """
    
    # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)
    
    # Crear el gráfico de caja con un tamaño de figura ajustado
    fig, ax = plt.subplots()  # Ajusta el tamaño de la figura según tus preferencias
    
    # Utilizar el método boxplot() en el DataFrame resultado
    resultado.boxplot(by=['region'], column=['PBI per capita 2022'], showmeans=True, ax=ax, layout=(1, 1))
    
    # Personalizar el gráfico
    ax.set_title('')
    ax.set_ylabel('PBI per capita 2022')
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"))  # Agrega separador de decimales
    
    # Ajustar las etiquetas del eje x para que aparezcan diagonalmente y no se superpongan
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Mostrar el gráfico
    plt.show()

#%%    
#Relación entre el PBI per cápita de cada país (año 2022 y para todos los
#países que se tiene información) y la cantidad de sedes en el exterior que
#tiene Argentina en esos países.
def visualizacion3():
    sedes = pd.read_csv(carpetaCvs + "sedes.csv")
    paises = pd.read_csv(carpetaCvs + "paises.csv")
    
    query = """
        SELECT
            p.nombre, p.region, p.PBI, COUNT(p.nombre) AS 'cant_sedes_por_pais'
        FROM paises AS p
        INNER JOIN sedes AS s
        ON p.id = s.pais_id
        GROUP BY p.nombre, p.id, p.PBI, p.region
        ORDER BY p.region
    """
    
    # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)    
    
    ## Grafico con todos los paises 

    plt.figure(figsize=(12, 20))  # Ancho x Alto
    sns.scatterplot(data=resultado, x="PBI", y="nombre", size='cant_sedes_por_pais', hue='cant_sedes_por_pais', legend=False, sizes=(200, 1000), palette= "plasma")


    # Lista de países para los cuales quieres agregar líneas horizontales
    paises_a_linea = ["China", "Italy", "Mexico", "Qatar", "United States", "Pakistan"]
    
    # Iterar sobre la lista de países y agregar líneas horizontales después de cada uno
    for pais in paises_a_linea:
        indice_pais = resultado[resultado['nombre'] == pais].index[0]  # Obtener el índice del país
        posicion_y_pais = indice_pais + 0.5  # Calcular la posición y del país y agregar un desplazamiento
        plt.axhline(y=posicion_y_pais, color='gray', linestyle='--', linewidth=1)
     
      
    plt.title(f'Scatterplot de PBI vs. Nombre de País con Gradiente de Colores según Cantidad de Sedes - Región: {region}')
    plt.xlabel('PBI')
    plt.ylabel('Nombre de País')
    plt.show()
        
    #realizamos un grafico por region para poder "hacer zoom" y analizar mejor
    # Iterar sobre cada región y trazar un scatter plot para cada una

    for region in resultado['region'].unique():
        plt.figure(figsize=(12, 10))  # Ancho x Alto
        data_region = resultado[resultado['region'] == region]
        sns.scatterplot(data=data_region, x="PBI", y="nombre", size='cant_sedes_por_pais', hue='cant_sedes_por_pais', legend=False, sizes=(200, 1000), palette= "plasma")
        plt.title(f'Scatterplot de PBI vs. Nombre de País con Gradiente de Colores según Cantidad de Sedes - Región: {region}')
        plt.xlabel('PBI')
        plt.ylabel('Nombre de País')
        plt.show()


    
if(__name__ == "__main__"):
  main()