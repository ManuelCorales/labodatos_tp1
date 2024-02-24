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
    visualizacion1()
    visualizacion2()
    visualizacion3()

def visualizacion1():
>>>>>>> 032a6b5748c01e460b29efd6a727563d0ac56477
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
    plt.show()

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
    
    # Calcular las medianas por región y ordenarlas
    medianas_por_region = resultado.groupby('region')['PBI per capita 2022'].median().sort_values()
        
    # Crear el gráfico de caja con un tamaño de figura ajustado
    fig, ax = plt.subplots()  # Ajusta el tamaño de la figura según tus preferencias
    
    resultado.boxplot(by=['region'], column=['PBI per capita 2022'], showmeans=True, ax=ax, layout=(1, 1))
    
    # Personalizar el título del gráfico
    ax.set_title('PBI per capita 2022 por región')
    
    # Personalizar el eje y
    ax.set_ylabel('PBI per capita 2022')
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.2f}"))  # Agrega separador de decimales
    
    # Ajustar las etiquetas del eje x para que aparezcan diagonalmente y no se superpongan
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
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
    
    # Calcular el número de colores necesarios para la paleta personalizada
    num_categorias = resultado['cant_sedes_por_pais'].nunique()
    
    # Generar una paleta de colores personalizada con más colores
    custom_palette = sns.color_palette("plasma", n_colors=num_categorias)
    
    ## Grafico con todos los paises 
    
    plt.figure(figsize=(12, 20))  # Ancho x Alto
    sns.scatterplot(data=resultado, x="PBI", y="nombre", s=300, hue='cant_sedes_por_pais', palette=custom_palette)
    
    # Add legend
    plt.legend(title='Cantidad de Sedes', fontsize=18)
    
    # Lista de países para los cuales quieres agregar líneas horizontales
    paises_a_linea = ["China", "Italy", "Mexico", "Qatar", "United States", "Pakistan"]
    
    # Iterar sobre la lista de países y agregar líneas horizontales después de cada uno
    for pais in paises_a_linea:
        indice_pais = resultado[resultado['nombre'] == pais].index[0]  # Obtener el índice del país
        posicion_y_pais = indice_pais + 0.5  # Calcular la posición y del país y agregar un desplazamiento
        plt.axhline(y=posicion_y_pais, color='gray', linestyle='--', linewidth=1)
    
    plt.title("titulo")
    plt.xlabel('PBI')
    plt.ylabel('Nombre de País')
    plt.show()

def ejecutarQuery(query: str) -> DataFrame:
    return sql^query
    
if(__name__ == "__main__"):
  main()