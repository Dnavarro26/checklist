import streamlit as st
import pandas as pd
import os

def main():
    st.title("Formulario de Documentación")
    st.markdown("**📋 Nota importante**")
    st.write("Los documentos opcionales no son obligatorios pero son altamente sugeridos para aumentar las probabilidades de aprobación y tener un flujo rápido de la operación.")

    # Definir el nombre y la ruta del archivo Excel
    archivo_excel = "checklist4.xlsx"  # Ruta completa del archivo


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
    st.write("**Estos documentos son obligatorios para el ingreso a riesgos:**")
    if len(df_ident) > 0:
        for doc in df_ident["Documentación"]:
            st.write(f"- {doc}")

    st.markdown("## ✅ Documentos de Garantía")
    st.write("**Estos documentos no son requeridos por el área de riesgos para determinar su aprobación. Sí son requeridos para realizar estudio de títulos de la propiedad y tasar el inmueble:**")
    if len(df_garantia) > 0:
        for doc in df_garantia["Documentación"]:
            st.write(f"- {doc}")
    st.write("Si crees que la garantía puede ser débil, de baja comercialidad o está en las periferias, te recomendamos que envíes una foto y la ubicación de la garantía.")

    st.markdown("## ⭐ Otros Documentos para la Evaluación (Complementarios según la operación)")
    st.markdown("**Documentos obligatorios según sea el caso:**")
    if len(df_otros) > 0:
        for doc in df_otros["Documentación"]:
            st.write(f"- {doc}")
    st.markdown("**Documentos que pueden ayudar a esclarecer una observación de riesgos**")
    st.markdown("• (Opcional) Cartas de no Adeudo: para acreditar si alguna deuda reportada actualmente ya ha sido cancelada")
    st.markdown("• (Opcional) Documentos que fortalezcan el destino como por ejemplo:")
    st.markdown("    -Si el cliente va a comprar una maquinaria o activo fijo con el préstamo, nos serviría la proforma de qué va a comprar.")
    st.markdown("    -Si el cliente hiciera una remodelación con el préstamo, nos serviría el presupuesto de obra del proyecto de remodelación.")
    st.markdown("**Si el cliente paga un préstamo con garantía inmobiliaria a un acreedor que no es un Banco, Caja o cooperativa:**")
    st.markdown("• (Obligatorio) Cronograma de pagos del préstamo.")
    st.markdown("• (Obligatorio) Últimos 6 vouchers de pago de la cuota.")
    st.markdown("• (Obligatorio) Liquidación para cancelar el préstamo a 25 días desde la fecha actual.")
    st.markdown("• (Opcional) Minuta o testimonio del préstamo con garantía hipotecaria.")
    st.markdown("• Nota: no puede haber atrasos en este tipo de préstamos, lo máximo tolerable es hasta 8 días.")

    # Opciones de tipo de ingreso
    tipos_ingreso_opciones = df_tipos["Tipo de ingreso"].drop_duplicates().str.capitalize().tolist()

    st.markdown("## 💵Documentos de Ingresos")
    st.write("Estos son los documentos que son requisitos para que sea evaluado por el equipo de riesgos.")
    st.markdown("## 🌎 Selección de Tipo de Ingreso")
    st.write("Aquí puede ser un ingreso declarado por SUNAT o un ingreso no declarado a SUNAT (Informal)")
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
    st.write("Para ciertos tipos de ingresos, tenemos hasta 2 opciones de sustentación:")
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
