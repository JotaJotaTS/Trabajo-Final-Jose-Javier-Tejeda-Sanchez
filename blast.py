#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#!/usr/bin/python
#Jose Javier Tejeda Sanchez
import sys
import os
from Bio import SeqIO
def blast(query, subject):
    os.system(f'touch blasteado.tsv')
    os.system (f'blastp -query {query} -subject {subject} -evalue "0.000001" -outfmt "6 qseqid sseqid qseq sseq qcovs pident evalue" > blasteado.tsv')
