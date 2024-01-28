import numpy as np
import time
from functools import cmp_to_key
from tqdm import trange

from .evolutionary_operators import *
from ..seedSetter import SeedSetter


def random_population(population_size, chromosome_length):
    population = np.random.random(size=(population_size, chromosome_length))
    return population / population.sum(axis=1).reshape(-1,1)


def dominates(x, y):
    '''Check if x dominates y'''
    return np.all(x <= y) and np.any(x < y)


def fast_nondominated_sorting(values):
    N,M = values.shape

    domination_count = np.zeros(N)
    dominated_elems = [[] for x in range(N)]

    for x in range(N):
        for y in range(x+1, N):
            if dominates(values[x], values[y]):
                dominated_elems[x].append(y)
                domination_count[y] += 1
            elif dominates(values[y], values[x]):
                domination_count[x] += 1
                dominated_elems[y].append(x)

    pareto_front_numbers = np.empty(N)
    current_number = 0
    Q = np.arange(N)[domination_count == 0]

    while Q.size > 0:
        pareto_front_numbers[Q] = current_number
        current_number += 1
        domination_count[Q] = -1
        for x in Q:
            domination_count[dominated_elems[x]] -= 1
        Q = np.arange(N)[domination_count == 0]

    return pareto_front_numbers


def calculate_crowding_distance(values):
    N,M = values.shape
    crowding_distance = np.zeros(N)
    for i in range(M):
        sorted_idx = np.argsort(values[:,i])
        crowding_distance[sorted_idx[[0, -1]]] = 1e40
        for j in range(1, M-1):
            crowding_distance[sorted_idx[j]] += (values[j+1, i] - values[j-1, i])
    return crowding_distance


def rank_population(population_values):
    pareto_front_numbers = fast_nondominated_sorting(population_values)
    crowding_dists = calculate_crowding_distance(population_values)

    def compare(x, y):
        if pareto_front_numbers[x] == pareto_front_numbers[y]:
            return crowding_dists[y] - crowding_dists[x]
        else:
            return pareto_front_numbers[x] - pareto_front_numbers[y]

    return np.array(list(sorted(np.arange(population_values.shape[0]), key=cmp_to_key(compare))))


@SeedSetter
def nsga2(objective_function,
          chromosome_length=20,
          population_size=100,
          number_of_offspring=200,
          number_of_iterations=100,
          max_time=np.inf, # in seconds
          crossover_probability = 0.95,
          mutation_probability = 0.25,
          crossover_operator=single_point_crossover,
          mutation_operator=change_pair_mutation,
          population_generator=random_population,
          alpha=0.5):

    beta = 2-alpha # used for ranking based selection

    # generate initial population
    population = population_generator(population_size=population_size,
                                      chromosome_length=chromosome_length)
    # evaluate initial population
    population_values = objective_function(population)

    end_time = time.time() + max_time

    for i in trange(number_of_iterations, desc='NSGA-II'):
        if time.time() >= end_time:
            print('NSGA-II: exceeded maximum execution time!')
            break

        # rank population (first - best, last - worst)
        population_ranking_idx = rank_population(population_values)

        # parent selection (ranking based)
        probabilities = (alpha + (np.arange(population_size-1,-1,-1)/(population_size-1)) * (beta - alpha)) / population_size
        parent_idx = np.random.choice(population_ranking_idx, size=number_of_offspring, replace=True, p=probabilities)

        # crossover
        offspring = crossover_operator(population[parent_idx], crossover_probability)

        # mutation
        offspring = mutation_operator(offspring, mutation_probability)

        # evaluate offspring
        offspring_values = objective_function(offspring)

        # rank population + offspring
        population = np.vstack([population, offspring])
        population_values = np.vstack([population_values, offspring_values])
        population_ranking_idx = rank_population(population_values)

        # select best to create new population
        population_ranking_idx = population_ranking_idx[:population_size]
        population = population[population_ranking_idx]
        population_values = population_values[population_ranking_idx]

    return population[fast_nondominated_sorting(population_values) == 0]
    # return population
