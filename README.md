# Catálogo de Productos Desacoplado (Flask + Fetch API) — LPII
Aplicación web desacoplada desarrollada para **Lenguaje de Programación II**. 
Implementa un backend REST en **Flask** con algoritmos de ordenamiento 
(**Quicksort**), **Búsqueda Binaria** con precondición de ordenamiento y un 
**Benchmark** de rendimiento frente a Ordenamiento Burbuja (1.000 elementos).
## Estructura del Proyecto- `app.py`: Servidor Flask y algoritmos en Python.- `productos.json`: Catálogo base de productos.- `templates/index.html`: Interfaz web responsiva con HTML5, CSS y JS 
(`fetch()`).- `LICENSE`: Licencia de código abierto.
## Instalación y Ejecución Local
1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear entorno virtual: `python -m venv venv` y activarlo.
3. Instalar Flask: `pip install flask`
4. Ejecutar el servidor: `python app.py`
5. Abrir `http://127.0.0.1:5000` en el navegador.