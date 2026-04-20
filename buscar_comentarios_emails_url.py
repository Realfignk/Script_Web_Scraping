import requests
from bs4 import BeautifulSoup, Comment
import re

def extraer_datos_web(url, archivo_salida):
    print(f"Estableciendo conexion hacia: {url}...")
    try:
        print("""
-------------------------------------------------------------
Proceso de extracción de comentarios y emails iniciado...
-------------------------------------------------------------
    """)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la página: {e}")
        return
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    comentarios = soup.find_all(string=lambda text: isinstance(text, Comment))
    patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    correos_encontrados = re.findall(patron_email, respuesta.text)
    correos_unicos = list(set(correos_encontrados))

    print(f"Archivo creado con los resultados: '{archivo_salida}'...")
    with open(archivo_salida, 'w', encoding='utf-8') as archivo:
        archivo.write(f">>> RESULTADO DE LA EXTRACCIÓN <<<\n")
        archivo.write(f"URL: {url}\n\n")
        archivo.write("- Correos electrónicos.\n")
        if correos_unicos:
            for correo in correos_unicos:
                archivo.write(f"- {correo}\n")
        else:
            archivo.write("No se encontraron correos electrónicos.\n")
        archivo.write("\n")
        archivo.write("- Comentarios en el html.\n")
        if comentarios:
            for comentario in comentarios:
                texto_limpio = comentario.strip()
                if texto_limpio:
                    archivo.write(f"\n")
        else:
            archivo.write("No se encontraron comentarios HTML.\n")
    print("""
--------------------------------------------------------------
Proceso de extracción completado.
--------------------------------------------------------------
    """)
    
url_objetivo = input("Ingresa una url válida (con puerto si no es el default [80] [8080]):")
nombre_del_archivo = "resultados_scrapping.txt"
extraer_datos_web(url_objetivo, nombre_del_archivo)
