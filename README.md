Primero, lo que hice fue cargar un archivo JSON que está en español. 
Mi objetivo era traducir todo el contenido al inglés y además generar nuevos IDs únicos y organizados, sin perder la estructura original del archivo.

Traducción de claves (keys):
Creé un diccionario donde mapeo las claves en español como "texto", "equipo", etc., 

Traducción de textos:
Usé la librería deep_translator con Google Translate para traducir automáticamente todos los textos que estén en cadenas de texto (strings).

Generación de nuevos IDs:
Para que los IDs sean únicos y no se repitan, los generé usando un hash del ID original, 

Transformación del archivo:
Recorrí todos los nodos del JSON, incluso los que están dentro de listas o estructuras anidadas, y a cada uno le apliqué la traducción y el cambio de ID si era necesario.

Guardado del resultado:
Finalmente, guardé el archivo nuevo 
