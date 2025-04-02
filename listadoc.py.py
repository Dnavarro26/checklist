import streamlit as st
import pandas as pd
import os

def main():
    st.title("Formulario de Documentación")

    # Definir el nombre y la ruta del archivo Excel
    archivo_excel = "checklist5.xlsx"  # Ruta completa del archivo


    # Asegurarse de que el archivo se encuentra en la ruta especificada
    if not os.path.exists(archivo_excel):
        st.error(f"El archivo {archivo_excel} no se encuentra en la ruta especificada.")
        return

    # Cargar datos desde el archivo Excel
    df_ident = pd.read_excel(archivo_excel, sheet_name="Documentación de indentificació")
    df_garantia = pd.read_excel(archivo_excel, sheet_name="Documentacion de garantía")
    df_otros = pd.read_excel(archivo_excel, sheet_name="Otros ")
    df_tipos = pd.read_excel(archivo_excel, sheet_name="tipos de ingreso")

    # Limpiar los espacios y caracteres extraños en las columnas relevantes
    df_tipos["Tipo de ingreso"] = df_tipos["Tipo de ingreso"].str.strip().str.lower()
    df_tipos["Actividad ecónomica"] = df_tipos["Actividad ecónomica"].str.strip()
    df_tipos["Modalidad"] = df_tipos["Modalidad"].str.strip()

    # Mostrar los documentos obligatorios
    st.markdown("## ✏️ Documentos de Identificación")
    if len(df_ident) > 0:
        for doc in df_ident["Documentación"]:
            st.write(f"- {doc}")

    st.markdown("## ✅ Documentos de Garantía")
    if len(df_garantia) > 0:
        for doc in df_garantia["Documentación"]:
            st.write(f"- {doc}")

    st.markdown("## ⭐ Otros Documentos para la Evaluación (Complementarios según la operación)")
    if len(df_otros) > 0:
        for doc in df_otros["Documentación"]:
            st.write(f"- {doc}")

    # Opciones de tipo de ingreso
    tipos_ingreso_opciones = df_tipos["Tipo de ingreso"].drop_duplicates().str.capitalize().tolist()

    st.markdown("## 🌎 Selección de Tipo de Ingreso")
    tipo_seleccionado = st.selectbox("Elige el tipo de ingreso", tipos_ingreso_opciones)

    # Convertir la selección a minúsculas para coincidir con el DataFrame
    tipo_seleccionado = tipo_seleccionado.lower()

    # Filtrar actividades económicas basadas en el tipo de ingreso seleccionado
    actividades_economicas = df_tipos[df_tipos["Tipo de ingreso"] == tipo_seleccionado]["Actividad ecónomica"].drop_duplicates().unique()

    # Mostrar selección de actividad económica
    st.markdown("## 💼 Selección de Actividad Económica")
    actividad_seleccionada = st.selectbox("Elige la actividad económica", actividades_economicas)

    # Filtrar modalidades basadas en el tipo de ingreso y actividad económica seleccionados
    modalidades_disponibles = df_tipos[
        (df_tipos["Tipo de ingreso"] == tipo_seleccionado) &
        (df_tipos["Actividad ecónomica"] == actividad_seleccionada)
    ]["Modalidad"].drop_duplicates().unique()

    # Mostrar selección de modalidad
    st.markdown("## ⚙️ Selección de Modalidad")
    modalidad_seleccionada = st.selectbox("Elige la modalidad", modalidades_disponibles)

    # Filtrar los documentos basados en el tipo de ingreso, actividad económica y modalidad seleccionados
    documentos_filtrados = df_tipos[
        (df_tipos["Tipo de ingreso"] == tipo_seleccionado) &
        (df_tipos["Actividad ecónomica"] == actividad_seleccionada) &
        (df_tipos["Modalidad"] == modalidad_seleccionada)
    ]

    # Mostrar los documentos requeridos
    st.markdown("## 📄 Documentos Requeridos (según selección)")
    if documentos_filtrados.empty:
        st.write("No hay documentos específicos para esta combinación.")
    else:
        for doc in documentos_filtrados["Documentación"]:
            st.write(f"- {doc}")

if __name__ == "__main__":
    main()
