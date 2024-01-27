import numpy as np


def single_point_crossover(parent1, parent2):
    crossover_point = np.random.randint(1, parent1.size)
    offspring = np.hstack([parent1[:crossover_point], parent2[crossover_point:]])
    return offspring / offspring.sum()


def swap_mutation(x):
    j,k = np.random.choice(x.size, size=2, replace=False)
    x[j], x[k] = x[k], x[j]
    return x
