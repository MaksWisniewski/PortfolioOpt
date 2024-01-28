import numpy as np
from tqdm import trange
from .evolutionary_operators import *
from ..seedSetter import SeedSetter


def random_population(population_size, chromosome_length):
    population = np.random.random(size=(population_size, chromosome_length))
    return population / population.sum(axis=1).reshape(-1,1)


def dominates(x, y):
    '''Check if x dominates y'''
    return np.all(x <= y) and np.any(x < y)


def default_weight_vectors(N):
    return np.c_[np.linspace(0,1,N), 1-np.linspace(0,1,N)]


@SeedSetter
def moead(objective_function,
          chromosome_length=20,
          number_of_iterations=200,
          weight_vectors=default_weight_vectors(100),
          neighborhood_size=20,
          mutation_probability=0.2,
          normalize=True,
          crossover_operator=single_point_crossover,
          mutation_operator=swap_mutation,
          population_generator=random_population):
    number_of_subproblems = weight_vectors.shape[0]

    # initialize population
    pareto_population = np.empty(0)
    pareto_values = np.empty(0)
    population = population_generator(population_size=number_of_subproblems,
                                      chromosome_length=chromosome_length)
    # evaluate population
    population_values = objective_function(population)

    # initialize reference point
    reference_point = np.min(population_values, axis=0)

    # initialize neighborhoods
    weight_vectors_2 = np.sum(weight_vectors**2, axis=1)
    distance_matrix = weight_vectors_2.reshape(-1,1) - 2*(weight_vectors @ weight_vectors.T) + weight_vectors_2

    neighborhoods = np.empty((number_of_subproblems, neighborhood_size))
    neighborhoods = np.argsort(distance_matrix)[:,:neighborhood_size]

    # scalar function - decomposition
    def g(f_value, weight_vector, ref_point):
        return np.max(weight_vector * np.abs(f_value - ref_point))

    # main loop
    for _ in trange(number_of_iterations, desc='MOEA/D'):
        for i in range(number_of_subproblems):
            # select parents
            k,l = np.random.choice(neighborhoods[i], size=2, replace=False)

            # create offspring
            offspring = crossover_operator(population[k], population[l])
            if np.random.uniform(0,1) < mutation_probability:
                offspring = mutation_operator(offspring)

            # evaluate offspring
            offspring_value = objective_function(offspring.reshape(1,-1))

            # update reference point
            reference_point = np.min(np.vstack([reference_point, offspring_value]), axis=0)

            # normalization factor
            if normalize:
                all_values = np.vstack([population_values, offspring_value, reference_point])
                normalization_factor = np.max(all_values, axis=0) - np.min(all_values, axis=0)
            else:
                normalization_factor = 1

            # update population and population_values
            for j in neighborhoods[i]:
                if (g(offspring_value/normalization_factor, weight_vectors[j], reference_point/normalization_factor) <
                    g(population_values[j]/normalization_factor, weight_vectors[j], reference_point/normalization_factor)):
                    population_values[j] = offspring_value
                    population[j] = offspring

            # update nondominated population (pareto)
            if pareto_population.size == 0:
                pareto_population = offspring.reshape(1,-1)
                pareto_values = offspring_value
            else:
                # remove elements dominated by offspring
                idx_to_remove = np.array([dominates(offspring_value, v) for v in pareto_values])
                pareto_population = pareto_population[~idx_to_remove]
                pareto_values = pareto_values[~idx_to_remove]
                # add offspring if it's nondominated
                if not np.any([dominates(v, offspring_value) for v in pareto_values]):
                    pareto_population = np.vstack([pareto_population, offspring])
                    pareto_values = np.vstack([pareto_values, offspring_value])

    return pareto_population
