import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import re

# Cargar el conjunto de datos de Netflix
df = pd.read_csv('netflixData.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Recomendación de Netflix")
root.geometry("600x400")

# Inicializar recomendaciones y entrada
recomendaciones = df
entrada_usuario = tk.StringVar()

# Función para obtener recomendaciones
def obtener_recomendaciones():
    entrada_text = entrada_usuario.get().lower()
    
    # Limpiar resultados anteriores
    resultados.delete("1.0", "end")
    
    # Inicializar recomendaciones con todas las películas
    recomendaciones = df
    
    # Inicialmente, no hay coincidencias
    coincidencias = False

    # Buscar la película proporcionada por el usuario
    pelicula_usuario = df[df['Title'].str.lower() == entrada_text]
    
    # Primera condición: coincidencia de director, actores y género
    if not pelicula_usuario.empty:
        # Obtener director, actores y género de la película proporcionada por el usuario
        director_pelicula = pelicula_usuario['Director'].values[0]
        actores_pelicula = pelicula_usuario['Cast'].values[0]
        genero_pelicula = pelicula_usuario['Genres'].values[0]

        if not pd.isna(director_pelicula) and not pd.isna(actores_pelicula) and not pd.isna(genero_pelicula):
            # Primera condición: coincidencia de director, actores y género
            recomendaciones_primera_condicion = recomendaciones[
                (recomendaciones['Genres'].str.contains(genero_pelicula, case=False)) &
                (recomendaciones['Director'].str.contains(director_pelicula, case=False)) &
                (recomendaciones['Cast'].str.contains(actores_pelicula, case=False))
            ]

            if not recomendaciones_primera_condicion.empty:
                resultado_texto = "Recomendaciones basadas en tu elección:\n"
                resultado_texto += "\n".join(recomendaciones_primera_condicion['Title'])
                resultados.insert("insert", resultado_texto)
                coincidencias = True
    
    # Otras condiciones de búsqueda aquí (segunda, tercera, cuarta)

    # Segunda condición: coincidencia de director y género
    if not coincidencias:
        if not pd.isna(director_pelicula) and not pd.isna(genero_pelicula):
            recomendaciones_segunda_condicion = recomendaciones[
                (recomendaciones['Genres'].str.contains(genero_pelicula, case=False)) &
                (recomendaciones['Director'].str.contains(director_pelicula, case=False))
            ]

            if not recomendaciones_segunda_condicion.empty:
                resultado_texto = "Recomendaciones basadas en tu elección:\n"
                resultado_texto += "\n".join(recomendaciones_segunda_condicion['Title'])
                resultados.insert("insert", resultado_texto)
                coincidencias = True

    # Tercera condición: coincidencia de actores y género
    if not coincidencias:
        actores_pelicula_str = ", ".join(actores_pelicula) if not pd.isna(actores_pelicula) else ""
        if actores_pelicula_str and not pd.isna(genero_pelicula):
            actores_pelicula_str = re.escape(actores_pelicula_str)  # Escapar caracteres especiales
            recomendaciones_tercera_condicion = recomendaciones[
                (recomendaciones['Genres'].str.contains(genero_pelicula, case=False)) &
                (recomendaciones['Cast'].str.contains(actores_pelicula_str, case=False))
            ]

            if not recomendaciones_tercera_condicion.empty:
                resultado_texto = "Recomendaciones basadas en tu elección:\n"
                resultado_texto += "\n".join(recomendaciones_tercera_condicion['Title'])
                resultados.insert("insert", resultado_texto)
                coincidencias = True

    # Cuarta condición: coincidencia de género
    if not coincidencias:
        if not pd.isna(genero_pelicula):
            recomendaciones_cuarta_condicion = recomendaciones[
                (recomendaciones['Genres'].str.contains(genero_pelicula, case=False))
            ]

            if not recomendaciones_cuarta_condicion.empty:
                resultado_texto = "Recomendaciones basadas en tu elección:\n"
                resultado_texto += "\n".join(recomendaciones_cuarta_condicion['Title'])
                resultados.insert("insert", resultado_texto)
                coincidencias = True
    if not coincidencias:
        resultado_texto = "La película que has ingresado no se encuentra en la base de datos. Por favor, verifica el nombre e inténtalo de nuevo."
        resultados.insert("insert", resultado_texto)

# Función para limpiar la búsqueda actual
def limpiar_busqueda():
    entrada_usuario.set("")  # Limpiar el campo de entrada
    resultados.delete("1.0", "end")  # Limpiar los resultados

# Arriba: Etiqueta para ingresar el nombre y título
etiqueta = tk.Label(root, text="Ingresa una película o serie que has disfrutado en Netflix:")
etiqueta.grid(row=0, column=0, columnspan=4)

# Medio: Campo de entrada de usuario y botones "Recomendaciones" y "Limpiar"
entrada_usuario = tk.StringVar()
entrada = tk.Entry(root, textvariable=entrada_usuario)
entrada.grid(row=1, column=0, columnspan=4)

boton_buscar = tk.Button(root, text="Obtener Recomendaciones", command=obtener_recomendaciones)
boton_buscar.grid(row=2, column=0)

boton_limpiar = tk.Button(root, text="Limpiar", command=limpiar_busqueda)
boton_limpiar.grid(row=2, column=1)

# Abajo: Ventana de resultados con desplazamiento
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.grid(row=3, column=4, sticky='ns')

resultados = scrolledtext.ScrolledText(root, wrap=tk.WORD, yscrollcommand=scrollbar.set)
resultados.grid(row=3, column=0, columnspan=4, sticky='nsew')
scrollbar.config(command=resultados.yview)

root.mainloop()




