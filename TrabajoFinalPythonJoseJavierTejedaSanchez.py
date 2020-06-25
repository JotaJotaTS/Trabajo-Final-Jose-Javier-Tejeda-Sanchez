#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#Jose Javier Tejeda Sanchez
import sys
import subprocess
from subprocess import call
from subprocess import Popen
import os
from Bio import SeqIO
from blast import blast
from muscle import muscle
import pandas as pd
from Bio import Phylo
import re
from Bio.ExPASy import Prosite,Prodoc
from prosite import prosite
#esta funcion se realizará cuando el usuario pida ayuda sobre el programa
def ayuda():

	mensaje= (

""" Programa final
Este programa consiste en utilizar una o varias proteinas en formato fasta,
que serán blasteadas frente a uno o varios genbanks, tras esto, se hace un
alineamiento y arbol filogenetico de los hits con la proteina con la que se
ha producido dicho hit, para ello utilizaremos muscle.
Finalmento se hará una busqueda de los dominios de los hits resultantes del
Blast en Prosite.

Para ejecutar este programa debe incluir dos argumentos:
    - El primer argumento será una carpeta que usted haya creado, en la cual
    estén las proteinas query en formato fasta.


    - El segundo argumento será una carpeta que usted haya creado, en la cual
    estén los Genbanks que serán usados como subject en el blast, tienen que
    estar en formato Genbank.

        !!!!! NO PONER ESPACIOS EN EL NOMBRE DE LA CARPETA ¡¡¡¡¡


Se recomienda que tanto el programa como las carpetas con query y subjects
estén en el mismo directorio para que solo haya que poner el nombre de la carpeta
en el argumento, de lo contrario hay que poner todo el path para llegar desde el
directorio donde se encuentre hasta el directorio donde estén las carpetas.


	"""
			)

	print(mensaje)
	sys.exit()
#Esta funcion saltará cuando el ususari no ponga 2 variables al inicio
def warning():

	message = (

"""Error: No son 2 parametros, debe introducir 2 parámaetros
Forma de usar el program: python TrabajoFinalPythonJoseJavierTejedaSanchez.py Parametro1 Parametro2
Para más informacion ponga: python TrabajoFinalPythonJoseJavierTejedaSanchez.py -h

		"""
			)
	print(message)
	sys.exit()

# Comprobamos que los query sean fasta
def VerificaFasta (fasta):
	fasta=open(fasta,'r')
	for line in fasta:
		if line.startswith(">"):
			esfasta = True
		else:
			sys.exit("\nError:uno de los query no está en formato fasta")
		break




# En caso de que el los parametros no sean el query y el subject saltan warning
arguments = sys.argv
if len(arguments)==2 and arguments[1] == "-h":
	ayuda()
elif len(arguments) != 3 or len(arguments)== 2 and arguments[1] != "-h" :
    warning()
if len(arguments) ==3:
	print('REALIZANDO EL BLAST')
#Vamos a crear un multifasta con las querys para luego blastearlo con el multifasta de los genbanks
	carpetaquery=os.listdir(arguments[1])
	q=0
	os.chdir(arguments[1])
	multiq=open('multifastaquery.fasta', "a")
	while q<len(carpetaquery):
		VerificaFasta(carpetaquery[q])
		recordq = list(SeqIO.parse(carpetaquery[q], "fasta"))
		a=0
		while a < len(recordq):
			multiq.write(f'>{recordq[a].id}\n{recordq[a].seq}\n\n')
			a=a+1
		q=q+1
		multiq.close()
	os.chdir('..')
# Para crear el multifasta con todos los genbanks 1º nos metemos en la carpeta con os.chdir
	carpetagb=os.listdir(arguments[2])
	n=0
	os.chdir(arguments[2])
#creamos el archivo de los multifasta que de momento estara en blanco
	outputgb= open("gb_multifasta.fasta", "w")
#con este bucle iremos genbank a genbank y guardando en el multifasta los locus y sus secuencias peptidicas
	while n < len(carpetagb):
		if carpetagb[n]!= 'gb_multifasta.fasta':
			try:
				inputgb= carpetagb[n]
				nombregb= open(carpetagb[n], "r")
				for seq_record in SeqIO.parse(nombregb, "genbank"):
					for seq_feature in seq_record.features:
						if seq_feature.type=="CDS":
							try:
								aminoacidos= seq_feature.qualifiers['translation'][0]
							except:
								aminoacidos = "empty"
							if aminoacidos != "empty":
								locus = seq_feature.qualifiers['locus_tag'][0]
								outputgb.write(f">{locus}\n{aminoacidos}\n")
			except:
				sys.exit(f'fallo en el parseo de los Genbanks, asegurese de que todos los archivos de la carpeta {arguments[2]} son genbanks')

			n=n+1
		else:
			n=n+1
	nombregb.close()
	outputgb.close()

#para blastear tenemos que mover el subject a la misma carpeta que el query
	call(['mv','gb_multifasta.fasta', f'../{arguments[1]}'])
	os.chdir('..')
	#creamos una carpeta donde se guardará despues el blasteo
	os.mkdir('blasteo')
#vamos a blastear los query que tenemos con el paquete blast.py
	os.chdir(arguments[1])
	blast('multifastaquery.fasta','gb_multifasta.fasta')
#movemos el blasteo a la carpeta blasteo
	os.system(f'mv blasteado.tsv ../blasteo')
	call(['mv','gb_multifasta.fasta', f'../{arguments[2]}'])
	os.chdir('..')
#en la carpeta proceso almacenamos los documentos intermedios necesarios para obtener los resultados finales
	os.mkdir('proceso')
#en la carpeta resultados_blast guardaremos todos los resultados del ejercicio
	os.mkdir('resultados_blast')
	os.chdir(arguments[1])
	print('REALIZANDO EL MUSCLE')
	muscle()
	os.chdir('..')
	print('HACIENDO COMPARACIÓN CON PROSITE')
	prosite()
	os.chdir('..')
	call(['mv', 'blasteo','resultados_blast'])
