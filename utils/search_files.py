# utils/search_files.py
import os

def buscar_archivos(ruta_base, extension):
    encontrados = []
    extension = extension.strip().lower()
    if not extension.startswith("."):
        extension = "." + extension

    for carpeta, _, archivos in os.walk(ruta_base):
        for archivo in archivos:
            if archivo.lower().endswith(extension):
                encontrados.append(os.path.join(carpeta, archivo))
    return encontrados
