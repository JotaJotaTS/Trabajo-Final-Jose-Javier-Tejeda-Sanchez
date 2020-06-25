#!/usr/bin/python
#-*- coding: utf-8 -*-
#Jose Javier Tejeda Sanchez
import sys
import os
import subprocess
from Bio import SeqIO
from subprocess import Popen
import pandas as pd
from Bio import Phylo

def muscle():
    m=0
#parseamos el multifasta para poder crear un fasta con cada proteina query y sus respectivos hits
    record = list(SeqIO.parse('multifastaquery.fasta', "fasta"))
    while m<len(record):
        fasta=open(f"fasta{record[m].id}.fasta","a")
        fasta.write(f'>{record[m].id}\n{record[m].seq}\n')
        os.system(f'mv fasta{record[m].id}.fasta ../proceso')
        m=m+1
    os.chdir('../blasteo')
#Guardamos los elementos de la tabla del blasteo utilizando el modulo pandas
    tablablast= pd.read_table('blasteado.tsv', sep='\t', names=['qseqid', 'sseqid', 'qseq', 'sseq', 'qcovs', 'pident', 'evalue'])
    #convertir una tabla en una lista
    idq= tablablast['qseqid'].tolist()
    ids= tablablast['sseqid'].tolist()
    qseq=tablablast['qseq'].tolist()
    sseq= tablablast['sseq'].tolist()
    cov= tablablast['qcovs'].tolist()
    iden= tablablast['pident'].tolist()
    os.chdir('../proceso')
    n=0
#en este caso ponemos el limite de identidad y el coverage para filtrar datos y los datos filtrados los metemos en un documento donde esten la querys con sus hits, un documento por query
    print('introduzca el coverage number mínimo para hacer el alineamiento (si no hay hits con este numero, mas adelante dará error): ')
    cove=float(input())
    print('introduzca el porcentaje de identidad minimo para hacer el alineamiento(si no hay hits con este numero, mas adelante dará error):')
    pide=float(input())
    while n<len(idq):
        todo=open(f'fasta{idq[n]}.fasta',"a")
        if cov[n]>cove and iden[n]>pide:
            todo.write(f">{ids[n]}\n{sseq[n]}\n")
        n=n+1
    os.chdir('..')
    fastamusc=os.listdir('proceso')
    os.chdir('proceso')
    f=0
#ejecutamos el muscle y creamos los arboles de cada query con sus hits
    while f<len(fastamusc):
        os.system(f'muscle -in {fastamusc[f]} -out muscle{fastamusc[f]}')
        os.system(f'muscle -maketree -in muscle{fastamusc[f]} -out arbol{fastamusc[f]}.nw -cluster neighborjoining')
        os.system(f'mv muscle{fastamusc[f]} ../resultados_blast')
        os.system(f'mv arbol{fastamusc[f]}.nw ../resultados_blast')
        f=f+1
