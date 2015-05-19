

Introducción
============

Implementar un filtro CBR, para identificar tarjetas de crédito sospechosas, utilizando Knn

El resultado del proyecto es encontrar un valor de sospecha para una tarjeta de crédito, dependiendo ciertas reglas.

Utilizando KNN Sobre propiedades:

* Precio
* Categoría
* Día y hora

Podemos obtener una predicción de que una operación o no es inválida.

Obtención de la base de datos de conocimiento
---------------------------------------------
Para utilizar el algoritmo de KNN ( el vecino mas cercano), necesitamos tener una base de conocimiento con la cual podamos
entrenar.

La BDK (Base de datos de conocimiento), era necesario juntar productos con sus categorías, encontré el api de mercadolibre,
el cual permite obtener productos directamente de su interfaz rest.

Con el pude obtener 24 categorías y mas de 100 productos.

.. code-block:: python

    resp = ml_api.get("/sites/%s/categories" % SITE )
    cat_list = resp.json()
    data = []
    cat_count = 0
    item_count = 0
    for cat in cat_list:
        cat_id = cat.get("id")
        cat_name = cat.get("name")
        d = {'cat_id':cat_id, 'cat_name':cat_name, 'items':[]}
        cat_count +=1
        for page in range(0,TIMES):
            page = random.randint(1,NUM_PAGE)
            url = "/sites/{}/hot_items/search?limit={}&category={}&page={}".format(SITE,LIMIT,cat_id, page)
            resp = ml_api.get(url)
            item_list = resp.json()["results"]
            for item in item_list:
                item_count +=1
                item_name = item.get("title")
                item_id = item.get("id")
                item_price = item.get("price")
                if item_name:
                    tran = random.randint(0,1)
                    d["items"].append({'item_id': item_id,
                        'item_price':item_price, 'item_name': item_name, 'item_transaction':tran})
        data.append(d)
    print "fetch"
    print "cats: {} items: {}".format(cat_count, item_count)
    return data

El campo de la fecha,hora,operación fueron generados con números aleatorios.

.. code-block::

    code

===
CBR
===

Para implementar el CBR es necesario pasar por los 4 pasos:

.. image:: https://i.imgur.com/bkfRHh0.png

Recuperar
~~~~~~~~~

El proceso de recuperar consta de obtener los datos, esto podemos obtenerlos de nuestra DBK. Obtendríamos un registro nuevo.

.. code-block:: txt

    shuf -n 10 out.csv > test.csv
    "Corral Para Bebe Super Seguro Lindos Colores Con Regalos","Bebés","349","08/30/00","10:49:13","0"
    "Tricicleta Playera Rodada 24","Deportes y Fitness ","3595","05/26/03","09:50:15","0"
    "Snow White Crema Secret Key Cosméticos Coreanos","Salud y Belleza","245","10/21/00","22:29:16","1"
    "Flash Tattoo  4 Planillas Envío Gratis Tatuajes Metálicos","Salud y Belleza","399","07/26/13","02:43:19","0"
    "Joyero / Alhajero Tipo Maniqui !!! Herreria 28 Cm Blanco","Joyas y Relojes","135","02/29/12","13:52:47","1"
    "Kit Imprimible Empresarial Invitaciones Recuerdos Tarjetas","Otras Categorías","399","08/01/05","09:33:32","0"
    "Hielera De Madera","Arte y Antigüedades","82","12/15/01","17:05:05","0"
    "Beyblade Storm Pegasus Y Rock Aquario Metal Fusión...unico","Juegos y Juguetes","349","04/01/08","17:10:49","1"
    "Banca Para Pecho Gold's Gym","Deportes y Fitness ","1290","01/22/15","10:28:21","1"
    "Batman Death Of The Family, Lo Mejor De Dc Nuevo Español","Coleccionables","160","08/11/00","09:13:45","0"

De nuestra BDK sacamos 10 registros aleatorios ( shuf ) y lo guardamos en un archivo test.csv

Estos datos son los que vamos a predecir.

Los registros de entrenamientos son agregados a una base de datos. Para su manipulación posterior.

Casos similares
~~~~~~~~~~~~~~~

Con el primer registro tenemos que buscar en nuestra base de conocimiento los registros que sean similares,
los cuales nos servirán para entrar:

* Tengan la misma categoría (en este caso que sea de bebés)



Aplicando KNN
~~~~~~~~~~~~~
Teniendo los casos similares, es necesario encontrar los vecinos mas cercanos (10 vecinos mas próximos).

"test_data" es nuestro dato que queremos predecir.


.. code-block:: python

    def get_neighbors(test_data, k=10):
        Distance.delete().execute()
        cat = test_data[0]
        datas = Data.select().where(Data.category == cat)
        for d in datas:
            dist = euclidean_distance(test_data, d)
            Distance.create(distance=dist, data=d)
        distances = Distance.select().order_by(Distance.distance.desc()).limit(k)
        return distances


Distancia entre vecinos
-----------------------
Para sacar la distancia entre vecino, se utilizo los siguientes datos de valor:

- Precio.
- Día de la semana de la operación (0-6).
- Horario diurno o nocturno.

.. code-block:: python

    def euclidean_distance(test_data, data_obj):
        distance = 0
        data_list = [data_obj.price,
                     data_obj.weekday(),
                     Data.is_light(data_obj.timestamp)
                     ]
        test_data = [test_data[1], 
                    datetime.fromtimestamp(test_data[2]).weekday(),
                    Data.is_light(test_data[2])
                    ]
        for i, elem in enumerate(data_list):
            distance += pow((Decimal(test_data[i]) - elem), 2)
        return math.sqrt(distance)

Las distancias fueron almacenadas en otro tabla de la base de datos para poder ordenarlas.
Dependiendo de la cantidad de vecinos, se procesaron estos contando cuantos fueron afirmativos y cuantos negativos el tenia la mayoría fue 
el resultado que se estimó.

.. code-block:: python

    def get_response(neighbors):
        SUCCESS = 1
        FAIL = 0
        k = {SUCCESS: 0, FAIL: 0}
        for i in neighbors:
            k[i.data.success] += 1
        sortedVotes = sorted(k.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]


Reusar, revisar, retener
~~~~~~~~~~~~~~~~

*Reusar*: Con la nueva estimación, esta se inserta  a la base datos en la tabla de entrenamiento.

*Revisar*: lo que hace es pedir interacción al usuario para saber si la operación de estimación fue correcta.

*Retener*: es guardar la información final una vez ya revisada.

.. code:: python

        print "%s %s >>>>>>>>>>>>> prediction: %s" % (cat,data[:-1], result)
        yes_no = raw_input("Desea validar el valor (y/[n])? ")
        if yes_no is 'y':
            result = raw_input("nuevo valor 1 or 0: ")
            

        data[-1] = result
        insert_data(*data)

demo:

.. raw:: html

    <iframe src="http://showterm.io/7571088a4c1f37a0a0942" style="width:100%;height:300px"></iframe>


http://showterm.io/7571088a4c1f37a0a0942#fast


Código fuente.
http://github.com/zodman/cbr

.. raw:: html
    <div data-theme="default" data-height="150" data-width="400" data-github="zodman/cbr" class="github-card"></div>
    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
