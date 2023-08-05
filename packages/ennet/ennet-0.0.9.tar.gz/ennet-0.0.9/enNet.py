import sys
import networkx as nx
from itertools import combinations
from collections import Counter
from pylab import *
import json
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
from scipy import stats
import load
import draw
import escore

def enNetWalk(G, max_iterations, pagerank, damping_factor, min_delta):
    nodes=G.nodes()
    for i in range(max_iterations):
        pagerank_last = copy.deepcopy(pagerank)
        diff = 0
        afterscore = 0
        for node in nodes:
            leftscore = damping_factor * pagerank_last[node]
            inscore = 0
            for target_node in G.neighbors(node):
                G.edge[node][target_node]["weight"]=round((1-damping_factor) * pagerank_last[node]/len(G.neighbors(node)),4)
                if len(G.neighbors(target_node)) <= 0:
                    pass
                else:
                    inscore += (1-damping_factor) * pagerank_last[target_node] / len(G.neighbors(target_node))
            afterscore = round(leftscore + inscore,4)
            pagerank[node]= afterscore
            diff += abs(afterscore - pagerank_last[node])
        print diff
        if diff < min_delta:
            break
    return G

def enNetHotspot(G, matrix, threshold, degree_num):
    G = G.to_undirected()
    nodes=G.nodes()
    for node in nodes:
        if matrix[node] < float(threshold):
            G.remove_node(node)
    nodes=G.nodes()
    for node in nodes:
        if len(G.neighbors(node)) < degree_num:
            G.remove_node(node)
    return G

def scoreFromFile(count_file, matrix):
    count = open(count_file,"r")
    i=0
    for line in count:
        items=line[0:-1].split("\t")
        if items[0] in matrix:
            i += 1
            matrix[items[0]] = float(items[1])
    return matrix

def scoreMatrix(count_dict, matrix):
    for key,value in count_dict.items():
        if key in matrix:
            matrix[key] = float(value)
    return matrix

def subNetwork(G, threshold):
    subG = nx.DiGraph()
    for n,nbrs in G.adjacency_iter():
        for nbr,eattr in nbrs.items():
            data=eattr['weight']
            if data>threshold:
                print('(%s, %s, %.3f)' % (n,nbr,data))
                subG.add_weighted_edges_from([(n,nbr,round(data,4))])
    return subG

def ennet(args):
    escore_dict, tmp=escore.snpcount(args.ep,args.sm)
    proteinNet_index_file=args.net+"_index_genes"
    proteinNet_edge_file=args.net+"_edge_list"
    G, matrix = load.getNetwork(proteinNet_edge_file, proteinNet_index_file)
    matrix=scoreMatrix(escore_dict, matrix)
    G = enNetHotspot(G, matrix, args.es, 1)
    draw.plot_hotspot_network_known(G, args.o, args.anno, layout = args.lay)

