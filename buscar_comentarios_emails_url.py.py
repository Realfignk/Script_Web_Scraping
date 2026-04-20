import requests
from bs4 import BeautifulSoup, Comment
import re

def extraer_datos_web(url, archivo_salida):
    print(f"Conectando a {url}...")
    
    # 1. Obtener el contenido de la página web
    try:
        # Usamos un User-Agent para simular que somos un navegador y evitar bloqueos simples
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        respuesta = requests.get(url, headers=headers)
        
        # Lanza un error si la petición no fue exitosa (ej. error 404 o 500)
        respuesta.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la página: {e}")
        return

    # 2. Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # 3. Extraer los comentarios HTML
    # Buscamos todos los elementos que sean instancias de la clase 'Comment'
    comentarios = soup.find_all(string=lambda text: isinstance(text, Comment))

    # 4. Extraer correos electrónicos
    # Patrón estándar de expresión regular para encontrar emails
    patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Buscamos el patrón en todo el texto en crudo de la página para no omitir nada
    correos_encontrados = re.findall(patron_email, respuesta.text)
    
    # Eliminamos duplicados convirtiendo la lista a un set y luego de vuelta a lista
    correos_unicos = list(set(correos_encontrados))

    # 5. Escribir los resultados en un archivo
    print(f"Guardando resultados en '{archivo_salida}'...")
    with open(archivo_salida, 'w', encoding='utf-8') as archivo:
        archivo.write(f"--- REPORTE DE EXTRACCIÓN ---\n")
        archivo.write(f"URL: {url}\n\n")

        # Guardar correos
        archivo.write("=== CORREOS ELECTRÓNICOS ENCONTRADOS ===\n")
        if correos_unicos:
            for correo in correos_unicos:
                archivo.write(f"- {correo}\n")
        else:
            archivo.write("No se encontraron correos electrónicos.\n")

        archivo.write("\n")

        # Guardar comentarios
        archivo.write("=== COMENTARIOS EN EL CÓDIGO HTML ===\n")
        if comentarios:
            for comentario in comentarios:
                # Limpiamos espacios en blanco al inicio/final del comentario
                texto_limpio = comentario.strip()
                if texto_limpio: # Evitamos imprimir comentarios vacíos
                    archivo.write(f"\n")
        else:
            archivo.write("No se encontraron comentarios HTML.\n")

    print("¡Extracción completada con éxito!")

# --- Bloque principal para ejecutar el script ---
if __name__ == "__main__":
    # Cambia esta URL por la página que deseas analizar
    url_objetivo = "https://ejemplo.com" 
    nombre_del_archivo = "resultados_extraccion.txt"
    
    extraer_datos_web(url_objetivo, nombre_del_archivo)
