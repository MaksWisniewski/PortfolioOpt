import numpy as np


def single_point_crossover(parent1, parent2):
    crossover_point = np.random.randint(1, parent1.size)
    offspring = np.hstack([parent1[:crossover_point], parent2[crossover_point:]])
    return offspring / offspring.sum()


def arithmetic_crossover(parent1, parent2):
    a = np.random.uniform(0,1)
    return a*parent1 + (1-a)*parent2


def differential_crossover(parent1, parent2):
    a = np.random.uniform(0,1)
    offspring = np.abs(parent1 + a*(parent1 - parent2))
    return offspring / offspring.sum()


def swap_mutation(x):
    j,k = np.random.choice(x.size, size=2, replace=False)
    x[j], x[k] = x[k], x[j]
    return x


def change_pair_mutation(x):
    j,k = np.random.choice(x.size, size=2, replace=False)
    delta = np.abs(np.random.normal(0, min(x[j], 1-x[k])/2))
    if x[j] - delta >= 0 and x[k] + delta <= 1:
        x[j] -= delta
        x[k] += delta
    return x
