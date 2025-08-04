# catalogo-objetos-visor

Un visor web para navegar, buscar y filtrar el catálogo de objetos de IDERA.

## Convertidor de excel a json

Se creó un script en python ("convertidor-atributos-json.py") para convertir el excel del catalogo de objetos de IDERA (V2-1_Marzo_2023) en un archivo .json. Tiene las clases, sus subclases, sus objetos y sus atributos (solo códigos y nombres).
Se hicieron modificaciones al excel del Catalogo de Objetos:

- Se quitaron acentos en titulos de columnas (ej: Código -> Codigo)
- Se separaron celdas combinadas y se completaron las nuevas celdas vacías según correspondía
