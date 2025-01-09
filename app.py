import pandas as pd
import streamlit as st

# Título de la aplicación
st.title("Filtro de Cursos y Nombres")

# Subida del archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel:", type=["xlsx"])

# Apartados para búsqueda
st.subheader("Buscar por Nombre de Persona o Curso")
opcion = st.radio(
    "Selecciona una opción para buscar:",
    ("Buscar por Nombre de Persona", "Buscar por Nombre del Curso")
)

# Entrada según la opción seleccionada
criterio = st.text_input("Escribe el valor a buscar:")

# Botón para procesar
if st.button("Procesar"):
    if uploaded_file and criterio:
        try:
            # Leer el archivo Excel
            datos = pd.ExcelFile(uploaded_file).parse(0)

            # Convertir las columnas relevantes a minúsculas para la búsqueda insensible a mayúsculas/minúsculas
            datos['Unnamed: 1'] = datos['Unnamed: 1'].str.lower()
            datos['Unnamed: 2'] = datos['Unnamed: 2'].str.lower()

            # Filtrar según la opción seleccionada
            if opcion == "Buscar por Nombre de Persona":
                filtrado = datos[datos['Unnamed: 1'] == criterio.lower()][['Unnamed: 2', 'Unnamed: 3']].copy()
                columna = "Nombre de Persona"
            elif opcion == "Buscar por Nombre del Curso":
                filtrado = datos[datos['Unnamed: 2'].str.contains(criterio.lower(), na=False)][['Unnamed: 1', 'Unnamed: 3']].copy()
                columna = "Nombre del Curso"

            # Renombrar columnas para mayor claridad
            if opcion == "Buscar por Nombre de Persona":
                filtrado.columns = ['Cursos', 'Link']
            else:
                filtrado.columns = ['Personas', 'Link']

            if filtrado.empty:
                st.warning(f"No se encontraron resultados para '{criterio}' en {columna}.")
            else:
                st.success(f"Se encontraron {len(filtrado)} resultados para '{criterio}' en {columna}.")

                # Mostrar los datos filtrados en la aplicación
                st.dataframe(filtrado)

                # Crear el nombre del archivo dinámicamente
                nombre_archivo = f"{criterio.replace(' ', '_')}-Resultados.xlsx"

                # Guardar los datos en un archivo Excel
                filtrado.to_excel(nombre_archivo, index=False)

                # Botón para descargar el archivo Excel
                with open(nombre_archivo, "rb") as file:
                    st.download_button(
                        label="Descargar Resultados",
                        data=file,
                        file_name=nombre_archivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        except Exception as e:
            st.error(f"Hubo un error procesando los datos: {e}")
    else:
        st.warning("Por favor, sube un archivo y escribe un criterio de búsqueda.")

# Mensaje adicional
st.info("Asegúrate de subir un archivo Excel válido y escribir correctamente el valor a buscar.")
