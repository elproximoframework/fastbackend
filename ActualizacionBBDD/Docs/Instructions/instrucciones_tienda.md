# Instrucciones para añadir Productos a la Tienda (Shop)

Este documento es la referencia para que el Agente IA pueda poblar automáticamente la base de datos de la tienda y gestionar las imágenes usando Cloudinary.

## Flujo de Trabajo

1. **El Usuario provee la información**: El usuario proporciona el enlace de afiliado (ej. Amazon), opcionalmente el nombre que le quiere dar, el precio aproximado o la descripción a resumir. 
2. **Descarga de la Imagen**: El Agente IA extrae/descarga o crea la imagen del producto y la nombra adecuadamente (ej: `maqueta-starship.png`).
3. **Guardado en Cloudinary**: La imagen se moverá / guardará bajo el directorio local `D:\YoutubeElProximoFrameworkEnElEspacio\Web\Cloudinary\shop` temporalmente y después se subirá al repositorio de Cloudinary.
4. **Inserción en Base de Datos**: El agente IA preparará un diccionario o JSON de los detalles usando las propiedades mencionadas y ejecutará el script `backendfast/ActualizacionBBDD/Scripts/insert_shop.py`. 

## Propiedades Requeridas

Asegúrate de preparar los siguientes campos para la inserción:

- **name** (String): Nombre del producto en español (ej: "Maqueta Starship & Torre de Lanzamiento").
- **name_en** (String): Nombre del producto en inglés (ej: "SpaceX Starship & Launch Tower Model").
- **description** (String): Una pequeña descripción atractiva del producto en español.
- **description_en** (String): Una pequeña descripción atractiva del producto en inglés.
- **price** (String): El precio actual o aproximado como texto, ej "89.99€".
- **image** (String): ¡Atención! Solo debes guardar el **Nomenclador (nombre.png)**. No guardar rutas completas ni la URL pública (ejemplo: `maqueta_starship.png`).
- **affiliateUrl** (String): El enlace final de afiliado.
- **category** (String): Clasificación. Valores recomendados:
  - `models`: Maquetas, Legos.
  - `books`: Libros, revistas y formatos de lectura.
  - `gear`: Herramientas, electrónica y merchandising de uso físico.
  - `clothing`: Ropa y moda.
- **featured** (Boolean): Si el producto debe estar destacado. Por defecto "False".
- **show** (Boolean): Por defecto "True".

## Modo de Ejecución

Para automatizar la entrada, utilizar:
```bash
python insert_shop.py --name "..." --name_en "..." --description "..." --description_en "..." --price "..." --image "..." --url "..." --category "..." --featured True
```
(O la estructura JSON equivalente si el script lo soporta).
