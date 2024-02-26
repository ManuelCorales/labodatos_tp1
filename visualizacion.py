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

# carpetaCvs = r"C:/Users/soler/Documents/Nari/faca/labodatos/tp1/labodatos_tp1/csv_limpios/"
carpetaCvs = "./TablasLimpias/"

def main():
    visualizacion1()
    visualizacion2()
    visualizacion3()

def visualizacion1():
    sedes = pd.read_csv(carpetaCvs + "sedes.csv")
    paises = pd.read_csv(carpetaCvs + "paises.csv")
    
    query = """
        SELECT
            p.region AS region,
            COUNT(p.region) AS cantidad_sedes
        FROM sedes s
        INNER JOIN paises p ON p.id = s.pais_id
        GROUP BY p.region 
        ORDER BY cantidad_sedes desc;
    """
    
    # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)
    
    # Creamos el gráfico utilizando seaborn
    plt.figure(figsize=(10, 8))
    sns.barplot(data=resultado, x='cantidad_sedes', y='region', palette="plasma")
    
    # Personalizar el gráfico
    plt.title('Cantidad de sedes argentinas por región', fontsize=16)
    plt.xlabel('Cantidad de sedes', fontsize=14)
    plt.ylabel('Región (en inglés)', fontsize=14)
    
    # Agregar etiquetas con la cantidad de sedes al final de cada barra
    for i, total in enumerate(resultado['cantidad_sedes']):
        plt.text(total + 0.5, i, f'{total}', va='center', ha='left', fontsize=12, weight='bold', color='black')
    
    plt.show()

#%% 
#Boxplot, por cada región geográfica, del PBI per cápita 2022 de los países
#donde Argentina tiene una delegación. Mostrar todos los boxplots en una
#misma figura, ordenados por la mediana de cada región.

def visualizacion2():
    sedes = pd.read_csv(carpetaCvs + "sedes.csv")
    paises = pd.read_csv(carpetaCvs + "paises.csv")

    query = """
        SELECT DISTINCT
            p.region AS region,
            PBI,
        FROM sedes s
        INNER JOIN paises p ON p.id = s.pais_id
        ORDER BY p.region ASC
    """
     # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)
        
    # Calcular las medianas por región y ordenarlas de manera descendente
    medianas_por_region = resultado.groupby('region')['PBI'].median().sort_values(ascending=False)
    
    # Establecer el orden de las categorías de la columna 'region'
    resultado['region'] = pd.Categorical(resultado['region'], categories=medianas_por_region.index, ordered=True)
    
    # Crear el gráfico de caja con un tamaño de figura ajustado
    fig, ax = plt.subplots()  # Ajusta el tamaño de la figura según tus preferencias
    
    resultado.boxplot(by=['region'], column=['PBI'], showmeans=True, ax=ax, layout=(1, 1))
    
    # Personalizar el título del gráfico
    ax.set_title('PBI per capita 2022 por región geográfica')
    
    # Personalizar el eje y
    ax.set_ylabel('PBI per capita 2022 (USD)')
    ax.set_xlabel('Región geográfica')
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"))  # Agrega separador de decimales
    
    # Ajustar las etiquetas del eje x para que aparezcan diagonalmente y no se superpongan
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Eliminar el título generado automáticamente
    plt.suptitle('')
    
    # Mostrar el gráfico
    plt.show()

    # realizo un grafico para ver mas grande las ultimas dos regiones
         
    # Obtener las últimas dos regiones según las medianas más bajas
    medianas_ultimas_dos_region = medianas_por_region.nsmallest(2).sort_values(ascending=False)
    
    # Filtrar el DataFrame resultado para que solo contenga las últimas dos regiones
    resultado_ultimas_dos = resultado[resultado['region'].isin(medianas_ultimas_dos_region.index)]
    
    # Establecer el orden de las categorías de la columna 'region'
    resultado_ultimas_dos['region'] = pd.Categorical(resultado_ultimas_dos['region'], categories=medianas_ultimas_dos_region.index, ordered=True)
    
    # Crear el gráfico de caja con un tamaño de figura ajustado
    fig, ax = plt.subplots(figsize=(10, 8))
    
    resultado_ultimas_dos.boxplot(by='region', column='PBI', showmeans=True, ax=ax)
    
    # Personalizar el título del gráfico
    ax.set_title('PBI per capita 2022 por las dos últimas regiones geográficas con menores medianas')
    
    # Personalizar el eje y
    ax.set_ylabel('PBI per capita 2022 (USD)')
    
    # Personalizar el eje x
    ax.set_xlabel('Región geográfica')
    
    # Formatear el eje y con separador de decimales
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"))
    
    # Ajustar las etiquetas del eje x para que aparezcan diagonalmente y no se superpongan
    ax.set_xticklabels(ax.get_xticklabels())
    
    # Eliminar el título generado automáticamente
    plt.suptitle('')
    
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
        SELECT DISTINCT
            p.nombre, p.region, p.PBI, COUNT(p.nombre) AS 'cant_sedes_por_pais'
        FROM paises AS p
        INNER JOIN sedes AS s
        ON p.id = s.pais_id
        GROUP BY p.nombre, p.id, p.PBI, p.region
        ORDER BY cant_sedes_por_pais
    """
    
    # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
    resultado = ejecutarQuery(query)
    
    # Calcular el número de colores necesarios para la paleta personalizada
    num_categorias = resultado['cant_sedes_por_pais'].nunique()
    
    # Generar una paleta de colores personalizada con más colores
    custom_palette = sns.color_palette("plasma", n_colors=num_categorias)
    
    ## Grafico con todos los paises 
    
    plt.figure(figsize=(12, 25))  # Ancho x Alto
    sns.scatterplot(data=resultado, x="PBI", y="nombre", s=300, hue='cant_sedes_por_pais', palette=custom_palette)
    
    # Add legend
    plt.legend(title='Cantidad de Sedes', fontsize=18)
    
    plt.title("Países en función de su PBI per cápita. Gradiente de color de acuerdo a la cantidad de delegaciones argentinas.", fontsize=16)
    plt.xlabel('PBI per cápita (USD)')
    plt.grid()

    plt.ylabel('Nombre de País')
    plt.xticks(fontsize=14)  # Agrandar la letra del eje x
    plt.yticks(fontsize=14)  # Agrandar la letra del eje y

    plt.show()

def ejecutarQuery(query: str) -> DataFrame:
    return sql^query
    
if(__name__ == "__main__"):
  main()