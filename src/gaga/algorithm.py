import pdb

import numpy as np

import gaga.functions as F


class GeneticAlgorithm:

    def __init__(self,
                 fitness_function,
                 n_genes,
                 gene_lb=0,
                 gene_ub=1,
                 mutate=F.default_mutate,
                 cross=F.default_cross,
                 pop_size=100,
                 n_survivors=20,
                 max_generations=100,
                 mutate_ratio=0.1,
                 cross_ratio=0.1,
                 epsilon=0.0):

        self.fitness_function = fitness_function
        self.n_genes = n_genes
        self.gene_lb = gene_lb
        self.gene_ub = gene_ub
        self.mutate = mutate
        self.cross = cross
        self.pop_size = pop_size
        self.max_generations = max_generations
        self.mutate_ratio = mutate_ratio
        self.cross_ratio = cross_ratio
        self.epsilon = epsilon

    def _init_pop(self, seed_pop):
        if seed_pop is None:
            # create random population
            pop = np.random.uniform(
                low=self.gene_lb,
                high=self.gene_ub,
                size=(self.pop_size, self.n_genes))
        else:
            pop = np.array(seed_pop)
            self.pop_size = pop.shape[0]
            self.n_genes = pop.shape[1]
        assert pop.shape == (self.pop_size, self.n_genes)
        assert pop.ravel().min() >= self.gene_lb
        assert pop.ravel().max() <= self.gene_ub
        return pop


    def solve(self, seed_pop=None):
        pop = self._init_pop(seed_pop)
        pop_idx = np.arange(self.pop_size)
        mut_bounds = lambda x: self.mutate(x, gene_lb=self.gene_lb, gene_ub=self.gene_ub)

        for generation in range(self.max_generations):
            # measure fitness of population
            fitness = np.array([self.fitness_function(x) for x in pop])
            # if fitness 0 found, return solution
            if min(fitness) <= self.epsilon:
                break
            # calculate survivor probability for each chromosome
            survivor_probs = F.softmax(1/fitness)
            # select survivor population
            survivor_idx = np.random.choice(pop_idx, p=survivor_probs, size=self.pop_size)
            pop = pop[survivor_idx]
            # apply mutations
            mut_prob = np.zeros(self.pop_size) + 1/self.pop_size
            is_mutated = np.random.choice(pop_idx, p=mut_prob, replace=False)
            pop[is_mutated] = np.apply_along_axis(mut_bounds, 0, pop[is_mutated])
            # TODO: apply crossings
            n_crosses = int(2 * (0.5 * self.n_genes * self.cross_ratio))
            children = []
            for _ in range(n_crosses):
                parent_idx1, parent_idx2 = np.random.choice(pop_idx, size=2, replace=False)
                child_idx = np.random.choice(pop_idx)
                child = self.cross(pop[parent_idx1], pop[parent_idx2])
                children.append([child_idx, child])
            for child_idx, child in children:
                pop[child_idx] = child

        fitness = np.array([self.fitness_function(x) for x in pop])
        best_idx = np.argmin(fitness)
        return pop[best_idx], fitness[best_idx], generation
