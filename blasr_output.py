#!/usr/bin/env python

import os, sys, string

# Reverse complement
complement_table = string.maketrans('ACGT', 'TGCA')
def reverse_comp(dna):
    '''
    reverse complelement function
    '''
    complement = dna[::-1].translate(complement_table)
    return complement

# using generator and yield function to read 4 lines at a time
def getStanza (infile):
    while True:
        fasta_id = infile.readline().rstrip()
        fasta_seq = infile.readline().rstrip()
        qual_id = infile.readline().rstrip()
        qual_scr = infile.readline().rstrip()
        if fasta_id != '':
            yield [fasta_id, fasta_seq, qual_id, qual_scr]
        else:
            print >> sys.stderr, 'Warning: End of Sequence'
            break

# Fasta parser
class Fastaseq():
    '''
    fasta reader
    '''
    def __init__(self):
        self.id = None
        self.seq = ''
        self.length = ''
      
    @staticmethod 
    def readline(infile):
        seqobj = Fastaseq()
        for line in infile:
            if len(line)==0: 
                print >> sys.stderr, 'empty line'
                continue
            if line.startswith('>'):
                if seqobj.id is None:
                    seqobj.id = line.rstrip()
                    continue
                else:
                    yield seqobj
                    seqobj = Fastaseq()
                    seqobj.id = line.rstrip()
            else:
                seqobj.seq += line.rstrip('\n\r').upper()
        yield seqobj    

blasr_file = sys.argv[1]
blasr = open(blasr_file, 'r')
main_dict = {}
for line in blasr:
    line = line.strip().split()
    if line[0] == 'Query:':
        key = line[1].split('/')[0]
        main_dict[key] = {'mapping':None, 'query_coords':[], 'target_coords':[]}
    if line[0] == 'Target':
        main_dict[key]['mapping'] = int(line[2])
    if line[0] == 'TargetRange:' :
        main_dict[key]['target_coords'] = [int(line[1]), int(line[3]), int(line[5])]
    if line[0] == 'QueryRange:' :
        main_dict[key]['query_coords'] = [int(line[1]), int(line[3]), int(line[5])]

blasr.close()

filter_main_dict = {}
for key in main_dict:
    query_start = main_dict[key]['query_coords'][0]
    query_end = main_dict[key]['query_coords'][1]
    read_len = main_dict[key]['query_coords'][2]
    target_start = main_dict[key]['target_coords'][0]
    target_end = main_dict[key]['target_coords'][1]
    mapping = float(main_dict[key]['mapping'])
    if not query_end - query_start > 3000: #6000:
        continue
    filter_main_dict[key] = [query_start, query_end, target_start, target_end, mapping]

in_fasta_file = sys.argv[2]
in_fasta = open(in_fasta_file, 'r')
for seq in Fastaseq.readline(in_fasta):
    key = seq.id.strip().split()[0].replace('>', '')
    if key in filter_main_dict:
        query_start = main_dict[key]['query_coords'][0]
        query_end = main_dict[key]['query_coords'][1]
        read_len = main_dict[key]['query_coords'][2]
        mapping = main_dict[key]['mapping']
        if mapping == 0:
            print '>' + key + '_' + str(read_len) + '_' + '_'.join(map(str, filter_main_dict[key])) 
            print seq.seq[query_start:] + seq.seq[:query_start]
        if mapping == 1:
            print '>' + key + '_' + str(read_len) + '_' + '_'.join(map(str, filter_main_dict[key])) + '_rev'
            print reverse_comp(seq.seq[query_end:] + seq.seq[:query_end])

