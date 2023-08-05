import matplotlib
matplotlib.use('Agg')
import sys
from argparse import ArgumentParser
import networkx as nx
from itertools import combinations
from collections import Counter
from pylab import *
import json
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import load,draw,enNet,escore
import numpy as np
from scipy import stats

def getArgs():
    parser = ArgumentParser(usage='python runEnnet.py -sm [path/to/somatic mutations file] -ep [path/to/enhancer-promoter interactions file] -net [path/to/network file] -out [path/to/outprefix]', description='Ennet version: 0.8.0')
    parser.add_argument('-sm', required=True, help='Path to tab-separated somatic mutations file containing chr, start and end fields.')
    parser.add_argument('-ep', required=True, help='Path to tab-separated enhancer-promoter interactions file containing chr, start, end and gene name fields.')
    parser.add_argument('-net', required=True, help='Path to network file.')
    parser.add_argument('-o', required=True, help='Outprefix, out file path + outprefix')
    parser.add_argument('-es', default=10.0, help='E score')
    parser.add_argument('-anno', default="./data/anno/netpath.tab", help='Path to gene annotation file')
    parser.add_argument('-lay', default="graphviz", help='Choose layout style: graphviz, circular, random, spring, shell')
    return parser.parse_args()

if __name__ == '__main__':
    #python runEnnet.py -es 12 -sm ./data/somatic_mutations/somatic_mutation.txt -ep ./data/ep/ep.txt -net ./data/network/hprd/hprd -o ex
    enNet.ennet(getArgs())

