# Practicas_MB
Prácticas de motores de búsqueda

## Práctica 1

### Objetivo

El objetivo de esta práctica es indexar una colección de documentos (LISA) en Apache Solr, realizar búsquedas en lote según el fichero [LISA.QUE](https://github.com/AlmuHS/Practicas_MB/blob/master/lisa/LISA.QUE), y analizar los resultados con ayuda de trec_eval

### Requisitos

- Apache Solr
- Python 3
	+ pysolr
- trec_eval
	
### Instalación

- **Instalación de dependencias**
	- En Ubuntu

			sudo apt install git python3-pip
			pip3 install pysolr
		
- **Descarga de la aplicación**
		
		git clone https://github.com/AlmuHS/Practicas_MB.git
	

### Ficheros

La aplicación se distribuye en forma de scripts, que hay que ejecutar desde línea de comandos. El propio repositorio incluye la colección de ficheros LISA, en el directorio [`lisa`](https://github.com/AlmuHS/Practicas_MB/tree/master/lisa)

Los ficheros correspondientes a la práctica 1 se encuentra en el directorio [`Practica1`](https://github.com/AlmuHS/Practicas_MB/tree/master/Practica1)
	
		cd Practicas_MB/Practica1

Los ficheros incluidos en esta práctica son:

- [`parse_LISA.py`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/parse_LISA.py): script principal de la aplicación
- [`write_xml.py`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/write_xml.py): script para pasar los documentos extraidos de los ficheros LISA, a formato XML (no utilizado en esta práctica)
- [`trec_rel_file`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/trec_rel_file): fichero resultante del procesado de `LISARJ.NUM`, preparado para ser utilizado en trec_eval
- [`trec_top_file`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/trec_top_file): fichero con los resultados de las consultas de `LISA.QUE`, preparado para ser utilizado por trec_eval
- [`trec_evaluation`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/trec_evaluation): fichero con la evaluación resultante de los ficheros anteriores en trec_eval
- [`trec_q_evaluation`](https://github.com/AlmuHS/Practicas_MB/blob/master/Practica1/trec_q_evaluation): fichero con la evaluación detallada de los ficheros anteriores en trec_eval


### Funcionamiento

Esta herramienta está hecha para funcionar mediante línea de comandos.

Para ejecutarla, debes llamar al script `parse_LISA.py` desde python, con esta sintaxis

	python3 parse_LISA.py [opciones] [argumentos]
	
Las opciones disponibles son:

- `add [fichero]`: parsea un fichero LISA, y sube sus documentos a Solr

	Por ejemplo:
	
		python3 parse_LISA.py add ../lisa/LISA1.001

- `query [cadena]`: ejecuta una consulta, definida en forma de cadena de caracteres, sobre Solr 

	Ejemplo: 
		
		python3 parse_LISA.py query "text: COMPUTER and TITLE: AMERICA"
		

- `query_batch [fichero_consultas] [fichero_resultados]`: Ejecuta una serie de consultas, provenientes de un fichero `LISA.QUE` o equivalente, devolviendo los resultados en un fichero con formato `trec_top_file`

	Ejemplo:
		
		python3 parse_LISA.py query_batch ../lisa/LISA.QUE trec_top_file
		
- `trec_eval [fichero resultados] [fichero_trec]`: Parsea un fichero `LISARJ.NUM`, escribiendo su contenido en otro fichero con formato `trec_ref_file`

	Ejemplo:
	
		python3 parse_LISA.py trec_eval ../lisa/LISARJ.NUM trec_ref_file
		
- `delete_all`: Elimina todos los ficheros existentes en el servidor Solr

	Ejemplo:
	
		 python3 parse_LISA.py delete_all


### Evaluación mediante TREC Eval


#### Instalación de TREC Eval sobre GNU/Linux

Para ejecutar TREC Eval sobre GNU/Linux, podemos compilar los fuentes desde su repositorio GitHub (https://github.com/usnistgov/trec_eval)

- **Descargar fuentes**

		git clone https://github.com/usnistgov/trec_eval.git
		
- **Compilar el código**

	Entramos al directorio
		
		cd trec_eval
		
	Ejecutamos `make`
	
		make 
		
	Esperamos a que compile
	
- **Instalar programa**

	Instalamos el programa con `make install`
	
		make install
		
	Con esto, ya podremos ejecutar `trec_eval` para comenzar la evaluación
		
#### Evaluación de las consultas

Para evaluar las consultas, nos vamos al directorio donde tenemos los ficheros `trec_rel_file` y `trec_top_file`, y ejecutamos `trec_eval`

	cd Practicas_MD/Practica1
	trec_eval trec_rel_file trec_top_file
	
Si queremos una evaluación consulta a consulta, podemos usar la opción `-q`

	trec_eval -q trec_rel_file trec_top_file