import pdb
import numpy as np

def mutate_swap(x, gene_lb=None, gene_ub=None):
    """swap two elements"""
    x = np.array(x)
    idx = range(len(x))
    i1, i2 = np.random.choice(idx, size=2, replace=False)
    x[i1], x[i2] = x[i2], x[i1]
    return x

def mutate_change(x, gene_lb=None, gene_ub=None):
    """swap two elements"""
    gene_lb = x.min() if gene_lb is None else gene_lb
    gene_ub = x.max() if gene_ub is None else gene_ub
    x = np.array(x)
    idx = np.random.choice(range(len(x)))
    x[idx] = np.random.uniform(low=gene_lb, high=gene_ub)
    return x

def cross_single_point(a, b):
    """single point cross over"""
    cross_point = np.random.randint(0,len(a))
    return np.concatenate([a[:cross_point], b[cross_point:]])

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(np.array(x) - np.max(x))
    return e_x / e_x.sum(axis=0) # only difference


default_mutate = mutate_change

default_cross = cross_single_point
