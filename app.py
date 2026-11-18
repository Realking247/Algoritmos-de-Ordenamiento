from flask import Flask, jsonify, request, render_template
import json, time, random, copy, os, urllib.request

app = Flask (__name__)

# Contenido del catálogo alojado en Pinata/IPFS (el JSON sí se puede servir en el gateway)
PINATA_GATEWAY = os.environ.get('PINATA_GATEWAY', 'https://magenta-faithful-scallop-75.mypinata.cloud')
PINATA_CID = os.environ.get('PINATA_CID', 'bafybeienrc6o2dcj7ny5efqpdqga3muzhgk3xe23ugwgxe3p4svm3dk6ta')
PINATA_URL = f'{PINATA_GATEWAY}/ipfs/{PINATA_CID}/productos.json'

_CACHE = {'datos': None, 'ts': 0.0, 'fuente': 'local'}
_CACHE_TTL = 300  # segundos


def _productos_desde_pinata():
    peticion = urllib.request.Request(
        PINATA_URL, headers={'User-Agent': 'catalogo-flask-lpii/1.0'}
    )
    with urllib.request.urlopen(peticion, timeout=3) as respuesta:
        datos = json.loads(respuesta.read().decode('utf-8'))
    if not isinstance(datos, list) or not datos:
        raise ValueError('Pinata devolvió un catálogo vacío o inválido')
    return datos


#(soporte de acentos)
def cargar_productos():
    ahora = time.time()
    if _CACHE['datos'] is not None and ahora - _CACHE['ts'] < _CACHE_TTL:
        return copy.deepcopy(_CACHE['datos'])

    try:
        datos = _productos_desde_pinata()
        _CACHE.update({'datos': datos, 'ts': ahora, 'fuente': 'pinata'})
        return copy.deepcopy(datos)
    except Exception:
        # Si Pinata no responde, se usa el JSON local incluido en el despliegue
        with open('productos.json', 'r', encoding='utf-8') as f:
            _CACHE.update({'datos': json.load(f), 'ts': ahora, 'fuente': 'local'})
            return copy.deepcopy(_CACHE['datos'])

   #1.Quicksort modular
    
def quicksort(items, clave, reverse = False):
         if len (items) <= 1:
               return items
         pivote = items[len(items) // 2][clave]
         izq = [x for x in items if (x[clave] > pivote if reverse else x[clave] < pivote)]
         centro = [x for x in items if x[clave] == pivote]
         der = [x for x in items if (x[clave] < pivote if reverse else x[clave] > pivote)]

         return quicksort(izq, clave, reverse) + centro + quicksort(der, clave, reverse)

    #2.Busqueda Binaria
def busqueda_binaria(items_ordenados, objetivo_id):
    izquierda, derecha = 0, len(items_ordenados) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        id_actual = items_ordenados[medio]['id']
        if id_actual == objetivo_id:
            return items_ordenados[medio]
        elif id_actual < objetivo_id:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None

    #3.BubbleSort
def bubble_sort(items, clave):
    arr = copy.deepcopy(items)
    n = len(arr)
    for i in range(n):
        hubo_cambio = False
        for j in range(0, n - i - 1):
            if arr[j][clave] > arr[j + 1][clave]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return arr

    # Ruta principal: entrega la interfaz HTML al navegador
@app.route('/')
def index():
 return render_template('index.html')

    #  Listar y ordenar productos con Quicksort
@app.route('/api/productos')
def get_productos():
  productos = cargar_productos()
  sort_by = request.args.get('sort_by', 'precio')
  order = request.args.get('order', 'asc') == 'desc'
  if productos and sort_by not in productos[0]:
    sort_by = 'precio'
  respuesta = jsonify(quicksort(productos, sort_by, reverse=order))
  respuesta.headers['X-Fuente-Datos'] = _CACHE['fuente']
  return respuesta

    # Estado de la integración con Pinata/IPFS
@app.route('/api/pinata')
def estado_pinata():
    productos = cargar_productos()
    return jsonify({
        'gateway': PINATA_GATEWAY,
        'cid': PINATA_CID,
        'url': PINATA_URL,
        'fuente': _CACHE['fuente'],
        'productos': len(productos)
    })

    # Buscar producto por ID mediante Búsqueda Binaria
@app.route('/api/productos/buscar')
def buscar_producto():
    id_param = request.args.get('id', '').strip()
    if not id_param.isdigit():
       return jsonify ({'encontrado': False, 'mensaje': 'Ingrese un ID numérico válido.'}), 400
    productos_ordenados = quicksort(cargar_productos(), 'id', reverse=False)
    resultado = busqueda_binaria(productos_ordenados, int(id_param))
    if resultado:
        return jsonify({'encontrado': True, 'producto': resultado})
    return jsonify({'encontrado': False, 'mensaje': f'No existe el ID {id_param}.'}), 404

   # Benchmark de 1.000 elementos (Quicksort vs Burbuja)
@app.route('/api/benchmark')
def ejecutar_benchmark():
    total = 1000
    muestra = [
        {'id': i, 'nombre': f'Item-{i}', 'precio': round(random.uniform(1.0, 999.0), 2)}
        for i in range(1, total + 1)
    ]
    random.shuffle(muestra)
    datos_quick, datos_burbuja = copy.deepcopy(muestra), copy.deepcopy(muestra)

    t0 = time.perf_counter()
    quicksort(datos_quick, 'precio', reverse=False)
    ms_quicksort = (time.perf_counter() - t0) * 1000
      
    t1 = time.perf_counter()
    bubble_sort(datos_burbuja, 'precio')
    ms_burbuja = (time.perf_counter() - t1) * 1000
     
    velocidad = round(ms_burbuja / ms_quicksort, 1) if ms_quicksort > 0 else 0
    return jsonify({
        'elementos': total,
        'quicksort_ms': round(ms_quicksort, 4),
        'burbuja_ms': round(ms_burbuja, 4),
        'comparativa': f'Quicksort fue {velocidad}x más rápido que BubbleSort'
    })
if __name__ == '__main__':
    app.run(debug=True)