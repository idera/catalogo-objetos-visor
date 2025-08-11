import pandas as pd

# Cargar todas las hojas del Excel
xls = pd.read_excel("convertidor-excel-json/Catalogo_Objetos_IDERA.xls", sheet_name=None, header=2)

# Hoja: Lista de atributos
df_lista_atrib = xls["LISTA DE ATRIBUTOS"]

# Cargar todas las hojas del Excel
xls_atrib = pd.read_excel("convertidor-excel-json/Catalogo_Objetos_IDERA.xls", sheet_name=None, header=3)

# Todas las hojas con nombres que coincidan con códigos de atributos
atributo_sheets = []
for sheet_name in xls_atrib.keys():
    # filtrar not in ["CLASES", "SUBCLASES", "OBJETOS", "ATRIBUTOS", "LISTA DE ATRIBUTOS"]
    if sheet_name not in ["PORTADA", "ESQUEMA", "CLASES", "SUBCLASES", "OBJETOS", "ATRIBUTOS", "LISTA DE ATRIBUTOS"]:
        atributo_sheets.append((sheet_name, xls_atrib[sheet_name]))

# lista de atributos final
lista = []

# primero recorremos la lista de atributos df_lista_atrib
for index, row in df_lista_atrib.iterrows():
    attr_codigo = row["CODIGO_A"]
    attr_nombre = row["NOMBRE"]
    attr_definicion = row["DEFINICION"]
    attr_tipo = row["TIPO DE ATRIBUTO"]
    attr_dominio = row["DOMINIO"]
    attr_obs = row["OBSERVACIONES"]

    if pd.isna(attr_obs):
        attr_obs = ""

    # si dominio es SI, busca el CODIGO_A en las hojas de atributos
    if attr_dominio == "SI":
        attr_dominio = []
        for sheet_name, sheet_data in atributo_sheets:
            if attr_codigo == sheet_name:
                # primero recorre todo el sheet_data, que tiene filas con codigos del dominio y definiciones de esos codigos
                for idx, sd_row in sheet_data.iterrows():
                    # siempre se salta el primero
                    if idx == 0:
                        continue
                    dominio_codigo = sd_row["Codigo"]
                    dominio_etiqueta = sd_row["Etiqueta"]
                    dominio_definicion = sd_row["Definición"]
                    dominio_obs = sd_row.get("Observaciones", "")

                    if pd.isna(dominio_obs):
                        dominio_obs = ""
                    if pd.isna(dominio_definicion):
                        dominio_definicion = ""

                    # crea un objeto dominio
                    obj_dominio = {
                        "codigo": dominio_codigo,
                        "etiqueta": dominio_etiqueta,
                        "definicion": dominio_definicion,
                        "observaciones": dominio_obs
                    }
                    # agrega el dominio al atributo
                    attr_dominio.append(obj_dominio)
    
    elif attr_dominio == "NO":
        attr_dominio = None

    atributo_data = {
        "codigo": attr_codigo,
        "nombre": attr_nombre,
        "definicion": attr_definicion,
        "dominio": attr_dominio,
        "tipo": attr_tipo,
        "observaciones": attr_obs
    }
    lista.append(atributo_data)

# crea un archivo json con los atributos, sus códigos y sus dominios (valores posibles, junto con sus definiciones)
import json
with open("convertidor-excel-json/atributos.json", "w", encoding="utf-8") as g:
    json.dump(lista, g, ensure_ascii=False, indent=2)