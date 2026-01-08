import os
import pandas as pd
from datetime import datetime, timedelta
from config import EXCEL_BASE_FOLDER, EXCEL_EXTENSION

df_cache = None
archivo_cargado = None


def generar_excel_limpio(fecha_excel):
    """
    Crea un Excel limpio usando POSICIÓN DE COLUMNAS
    """
    global df_cache, archivo_cargado

    archivo_origen = None
    for root, _, files in os.walk(EXCEL_BASE_FOLDER):
        for file in files:
            if file.endswith(EXCEL_EXTENSION) and fecha_excel in file:
                archivo_origen = os.path.join(root, file)
                break

    if not archivo_origen:
        return False, f"No se encontró Excel para la fecha {fecha_excel}"

    df = pd.read_excel(archivo_origen, dtype=str, engine="openpyxl")

    if df.shape[1] < 8:
        return False, "El Excel no tiene la cantidad mínima de columnas esperadas"

    df_limpio = pd.DataFrame({
        "area": df.iloc[:, 6].fillna(""),
        "ubicacion": df.iloc[:, 1].fillna(""),
        "sku": (
            df.iloc[:, 2]
            .astype(str)
            .str.replace('="', '', regex=False)
            .str.replace('"', '', regex=False)
            .str.replace("=", "", regex=False)
            .str.strip()
        ),
        "descripcion": df.iloc[:, 3].fillna(""),
        "stock": df.iloc[:, 4].fillna("0"),
        "asignado": df.iloc[:, 5].fillna("0"),
        "bloqueado": df.iloc[:, 7].fillna("")
    })

    base_clean = "data_limpia"
    carpeta_fecha = datetime.strptime(fecha_excel, "%d-%m-%Y").strftime("%Y-%m-%d")
    ruta_carpeta = os.path.join(base_clean, carpeta_fecha)
    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_excel = os.path.join(ruta_carpeta, "inventario_limpio.xlsx")
    df_limpio.to_excel(ruta_excel, index=False)

    df_cache = df_limpio
    archivo_cargado = ruta_excel

    print("✅ Excel limpio generado:", ruta_excel)
    print("📋 Columnas:", df_limpio.columns.tolist())

    return True, ruta_excel


def actualizar_excel_limpio():
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)

    fecha_hoy = hoy.strftime("%d-%m-%Y")
    fecha_ayer = ayer.strftime("%d-%m-%Y")

    ok, _ = generar_excel_limpio(fecha_hoy)
    if ok:
        return {
            "status": "ok",
            "mensaje": "Excel actualizado con información del día de hoy"
        }

    ok, _ = generar_excel_limpio(fecha_ayer)
    if ok:
        return {
            "status": "warning",
            "mensaje": "Excel creado con información de ayer. Intente más tarde para actualizar con la fecha de hoy."
        }

    return {
        "status": "error",
        "mensaje": "No se encontró Excel ni de hoy ni de ayer"
    }


def search_by_sku(sku):
    global df_cache

    if df_cache is None:
        return []

    sku = str(sku).strip()
    df_filtrado = df_cache[df_cache["sku"] == sku]

    if df_filtrado.empty:
        return []

    return df_filtrado.to_dict(orient="records")


def get_excel_info():
    return archivo_cargado


def generar_excel_limpio_desde_archivo(ruta_excel):
    """
    Genera el Excel limpio a partir de un archivo subido manualmente
    """
    global df_cache, archivo_cargado

    df = pd.read_excel(ruta_excel, dtype=str, engine="openpyxl")

    if df.shape[1] < 8:
        return False, "El Excel no tiene la cantidad mínima de columnas esperadas"

    df_limpio = pd.DataFrame({
        "area": df.iloc[:, 6].fillna(""),
        "ubicacion": df.iloc[:, 1].fillna(""),
        "sku": (
            df.iloc[:, 2]
            .astype(str)
            .str.replace('="', '', regex=False)
            .str.replace('"', '', regex=False)
            .str.replace("=", "", regex=False)
            .str.strip()
        ),
        "descripcion": df.iloc[:, 3].fillna(""),
        "stock": df.iloc[:, 4].fillna("0"),
        "asignado": df.iloc[:, 5].fillna("0"),
        "bloqueado": df.iloc[:, 7].fillna("")
    })

    hoy = datetime.now().strftime("%Y-%m-%d")
    ruta_carpeta = os.path.join("data_limpia", hoy)
    os.makedirs(ruta_carpeta, exist_ok=True)

    ruta_excel_limpio = os.path.join(ruta_carpeta, "inventario_limpio.xlsx")
    df_limpio.to_excel(ruta_excel_limpio, index=False)

    df_cache = df_limpio
    archivo_cargado = ruta_excel_limpio

    return True, "Excel cargado manualmente y procesado correctamente"
