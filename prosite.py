#!/usr/bin/python
#-*- coding: utf-8 -*-
#Jose Javier Tejeda Sanchez
import sys
import os
import subprocess
from Bio import SeqIO
from subprocess import Popen
import pandas as pd
import re
from Bio.ExPASy import Prosite,Prodoc
def prosite():
	handle = open("prosite.dat","r")
	prosite = Prosite.parse(handle)
	lista=os.listdir('proceso')
	for record in prosite:
	# ponemos este if distinto de 49 porque en la base de datos de prosyte existen entradas sin ningún pattern, y estas entradas tienen una longitud de 49 caracteres, esto los averigüé haciendo un print de los tamaños de cada entrada
		if sys.getsizeof(record.pattern)!=49:
#Cambiamos los simbolos de prosite para que sean reconocidos por el modulo re
			rec= record.pattern.replace('x','[ARNDCEQGHIULKMFPSTWYVO]')
			rec= rec.replace('-','')
			rec= rec.replace('{','[^')
			rec= rec.replace('}',']')
			rec=rec.replace('(','{')
			rec=rec.replace(')','}')
			rec= rec.replace('.','')
			rec= rec.replace('>','$')
			rec= rec.replace('<','^')

			os.chdir('proceso')
			n=0
#creamos los archivos donde se pondrán los resultados
			while n<len(lista):
				seq = list(SeqIO.parse(f'{lista[n]}', "fasta"))
				archivo=open(f'DominiosProsite_{lista[n]}.txt','a')
				m=0
				while m<len(seq):
					secuencia=seq[m].seq
					secuencia=str(secuencia)
					proteina= seq[m].id
					if re.search(rec, secuencia):
						archivo.write(f'Nombre proteina: {proteina}\n Secuencia proteína: {secuencia}\n Dominio de Prosite: {record.name}\n Accession:{record.accession}\n Patrón encontrado:{record.pattern}\n\n ')
						m=m+1
					else:
						m=m+1

				n=n+1
			os.chdir('..')
	lista=os.listdir('proceso')
	os.chdir('proceso')
	i=0
	while i<len(lista):
		archivo=lista[i]

		if re.search(r".txt",archivo):
			os.system(f'mv {archivo} ../resultados_blast')

		i=i+1
