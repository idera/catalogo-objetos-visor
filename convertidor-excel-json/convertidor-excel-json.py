import pandas as pd

# Cargar todas las hojas del Excel
xls = pd.read_excel("Catalogo_Objetos_IDERA.xls", sheet_name=None, header=2)

# Hoja: Clases
df_clases = xls["CLASES"]

# Hoja: Subclases
df_subclases = xls["SUBCLASES"]

# Hoja: Objetos
df_objetos = xls["OBJETOS"]

# Hoja: Atributos asociados
df_atributos = xls["ATRIBUTOS"]

# Array final
catalogo = []

# Paso 1: Recorremos cada clase
for i, clase_row in df_clases.iterrows(): # el indice i es el índice de la clase actual
    clase_codigo = clase_row["CODIGO_C"]
    clase_nombre = clase_row["CLASE"]
    catalogo.append({"nombre": clase_nombre, "codigo": clase_codigo, "contenido": clase_row["CONTENIDO"], "subcategorias": []})

    # Subcategorías de esa clase
    subclases = df_subclases[df_subclases["CODIGO_C"] == clase_codigo] # Filtrar subclases por clase actual
    for j, sub_row in subclases.iterrows():
        sub_codigo = sub_row["CODIGO_S"]
        sub_nombre = sub_row["SUBCLASE"]
        key = sub_row["CODIGO_S"]
        catalogo[i]["subcategorias"].append({"nombre": sub_nombre, "codigo": sub_codigo, "contenido": sub_row["CONTENIDO"], "objetos": []})

        # Objetos dentro de esa subcategoría
        objetos = df_objetos[
            (df_objetos["CODIGO_C"] == clase_codigo) &
            (df_objetos["CODIGO_S"] == sub_codigo)
        ]
        for _, obj_row in objetos.iterrows():
            obj_codigo = obj_row["CODIGO_O"]
            obj_nombre = obj_row["OBJETO"]
            obj_def = obj_row["DEFINICION"]
            obj_geo = obj_row["GEOMETRIA"]

            objeto_data = {
                "nombre": obj_nombre,
                "geometria": obj_geo,
                "definicion": obj_def,
                "atributos": []
            }

            # Buscar atributos asociados
            atributos = df_atributos[
                (df_atributos["CODIGO_C"] == clase_codigo) &
                (df_atributos["CODIGO_S"] == sub_codigo) &
                (df_atributos["CODIGO_O"] == obj_codigo)
            ]
            for _, attr_row in atributos.iterrows():
                attr_codigo = attr_row["CODIGO_A"]
                attr_denominacion = attr_row["DENOMINACION"]
                #attr_info = df_lista_atrib[df_lista_atrib["CODIGO_A"] == attr_codigo].squeeze() # Obtener la fila como una Serie

                objeto_data["atributos"].append({
                    "codigo": attr_codigo,
                    "denominacion": attr_denominacion,
                })

            catalogo[i]["subcategorias"][-1]["objetos"].append(objeto_data)

# Guardar el resultado
import json
with open("catalogo.json", "w", encoding="utf-8") as f:
    json.dump(catalogo, f, ensure_ascii=False, indent=2)


