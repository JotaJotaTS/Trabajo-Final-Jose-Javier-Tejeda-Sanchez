# Trabajo-Final-Jose-Javier-Tejeda-Sanchez
Para utilizar este programa hay que tener en cuenta las siguientes cosas:
1ª Hay que crear una carpeta para los querys(archivos fasta) y otra para los subject(archivos Genbank, el nombtre de la carpeta sin espacios
2º Es recomendable que las carpetas esten en el mismo directorio donde se ejecute el programa, de lo contrario habrá que poner la ruta de la carpeta
3º El archivo de prosite debe estar obligatoriamente en el directorio donde se ejecuta el programa
4º Para ejecutar el programa debe ponerse en el terminal el siguiente comando:
    python TrabajoFinalPythonJoseJavierTejedaSanchez.py CarpetaQuery CarpetaSubject
Si las carpetas estan en otro directorio hay que poner la ruta.
5º Para abrir la ayuda se pone: python TrabajoFinalPythonJoseJavierTejedaSanchez.py -h
6º Ejecutar en Linux, no vale para Apple

El script sirve para realizar un blasteo de las qurys en la carpeta de las querys con un conjunto de genbanks de la carpeta de genbanks, a continuacion se hace alineamiento de las quyerys con sus hits utilizando muscle y se hace un arbol filogenetico, por último se comparan los dominios de los hits con una base de datos de prosite y se ponen las coincidencias, todo esto se guardará en una carpeta llamada 'resultados_blast', en la carpeta de querys aparecerá un multifasta con todas las querys y en la de los gen bank un multifasta con los genbanks. Se creará otra carpeta llamada 'proceso' donde se guardaran los documentos usados para obtener los resultados.
