import pandas as pd
import streamlit as st

# Título de la aplicación
st.title("Filtro de Cursos por Nombre")

# Subida del archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel:", type=["xlsx"])

# Entrada del nombre
nombre = st.text_input("Escribe el nombre que deseas buscar:")

# Botón para procesar
if st.button("Procesar"):
    if uploaded_file and nombre:
        try:
            # Leer el archivo Excel
            datos = pd.ExcelFile(uploaded_file).parse(0)

            # Filtrar por el nombre
            filtrado = datos[datos['Unnamed: 1'] == nombre][['Unnamed: 2', 'Unnamed: 3']].copy()
            filtrado.columns = ['Cursos', 'Link']

            if filtrado.empty:
                st.warning(f"No se encontraron datos para '{nombre}'.")
            else:
                st.success(f"Se encontraron {len(filtrado)} cursos para '{nombre}'.")

                # Mostrar los datos filtrados en la aplicación
                st.dataframe(filtrado)

                # Crear el nombre del archivo dinámicamente
                nombre_archivo = f"{nombre.replace(' ', '_')}-Resultados.xlsx"

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
        st.warning("Por favor, sube un archivo y escribe un nombre.")

# Mensaje adicional
st.info("Asegúrate de subir un archivo Excel válido y escribir el nombre correctamente.")
