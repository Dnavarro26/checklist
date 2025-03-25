import streamlit as st
import pandas as pd
import os

def main():
    st.title("Formulario de Documentación")

    # Definir el nombre del archivo Excel
    archivo_excel = "checklist4.xlsx"  # Solo el nombre del archivo

    # Asegurarse de que el archivo se encuentra en la misma carpeta que el script
    if not os.path.exists(archivo_excel):
        st.error(f"El archivo {archivo_excel} no se encuentra en el mismo directorio que el script.")
        return

    # Cargar datos desde el archivo Excel
    df_ident = pd.read_excel(archivo_excel, sheet_name="Hoja 1")
    df_garantia = pd.read_excel(archivo_excel, sheet_name="Hoja 2")
    df_otros = pd.read_excel(archivo_excel, sheet_name="Hoja 3")
    df_tipos = pd.read_excel(archivo_excel, sheet_name="tipos de ingreso")

    # Limpiar los espacios y caracteres extraños en las columnas relevantes
    df_tipos["Tipo de Ingreso"] = df_tipos["Tipo de Ingreso"].str.strip().str.lower()
    df_tipos["Modalidad"] = df_tipos["Modalidad"].str.strip()

    # Mostrar los documentos obligatorios
    st.markdown("## ✏️ Documentos de Identificación (Obligatorios)")
    if len(df_ident) > 0:
        for doc in df_ident["Documentación"]:
            st.write(f"- {doc}")

    st.markdown("## ✅ Documentos de Garantía (Obligatorios)")
    if len(df_garantia) > 0:
        for doc in df_garantia["Documentación"]:
            st.write(f"- {doc}")

    st.markdown("## ⭐ Otros Documentos para la Evaluación (Complementarios según la operación)")
    if len(df_otros) > 0:
        for doc in df_otros["Documentación"]:
            st.write(f"- {doc}")

    # Opciones de tipo de ingreso
    tipos_ingreso_opciones = [
        "1ra categoría formal",
        "1ra categoría informal",
        "3ra categoría formal",
        "3ra categoría informal",
        "4ta categoría formal",
        "profesional independiente (no formal)",
        "5ta categoría formal"
    ]

    st.markdown("## 🌎 Selección de Tipo de Ingreso")
    tipo_seleccionado = st.selectbox("Elige el tipo de ingreso", tipos_ingreso_opciones)

    # Convertir la selección a minúsculas para coincidir con el DataFrame
    tipo_seleccionado = tipo_seleccionado.lower()

    # Filtrar modalidades basadas en el tipo de ingreso seleccionado
    modalidades_disponibles = df_tipos[df_tipos["Tipo de Ingreso"] == tipo_seleccionado]["Modalidad"].drop_duplicates().dropna().unique()

    # Si no hay modalidades disponibles, mostrar un mensaje adecuado
    if len(modalidades_disponibles) == 0:
        st.write("No hay modalidades disponibles para este tipo de ingreso.")
    else:
        st.markdown("## ⚙️ Selección de Modalidad")
        modalidad_seleccionada = st.selectbox("Elige la modalidad", modalidades_disponibles)

        # Filtrar los documentos basados en el tipo de ingreso y modalidad seleccionados
        documentos_filtrados = df_tipos[
            (df_tipos["Tipo de Ingreso"] == tipo_seleccionado) &
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

