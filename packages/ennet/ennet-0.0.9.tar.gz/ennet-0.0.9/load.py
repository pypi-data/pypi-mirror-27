import sys
import networkx as nx
from itertools import combinations
from collections import Counter
from pylab import *
import json
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

def getIndex(index_file):
    """Load gene index information from file and return as a dict mapping index to gene name.
    
    Arguments:
    path to TSV file containing an index in the first column and the name of the gene
                  represented at that index in the second column
    
    """
    with open(index_file) as index:
        arrs  = [l.split() for l in index]
        return dict((int(arr[0]), arr[1]) for arr in arrs)

def getMatrix(index_file):
    matrix={}
    index = open(index_file,"r")
    for l in index:
        items=l.split()
        matrix[items[1]]=0
    return matrix

def getNetwork(edgelist_file, gene_index_file):
    """Load gene index and edge information from file and return network G.
    
    Arguments:
    path to gene index file and nodes edge file.
    
    """
    index2gene = getIndex(gene_index_file)
    matrix = getMatrix(gene_index_file)
    edgelist=[map(int, l.rstrip().split()[:3]) for l in open(edgelist_file)]
    for item in edgelist:
        item[0]=index2gene[item[0]]
        item[1]=index2gene[item[1]]
        item[2]=0

    edgelist2=[map(int, l.rstrip().split()[:3]) for l in open(edgelist_file)]
    for item in edgelist2:
        aaa=index2gene[item[0]]
        bbb=index2gene[item[1]]
        item[0]=bbb
        item[1]=aaa
        item[2]=0

    G = nx.DiGraph()
    G.add_weighted_edges_from(edgelist)
    G.add_weighted_edges_from(edgelist2)

    G.remove_edges_from([(u,v) for u, v in G.edges() if u == v])
    G.remove_nodes_from([n for n in G.nodes() if G.degree(n) == 0])

    print "\t{} nodes with {} edges remaining".format(len(G.nodes()), len(G.edges()))
    return G, matrix

