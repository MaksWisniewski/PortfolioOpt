import numpy as np

# to change
# single point crossover, result divided by sum
def single_point_crossover(parents, crossover_probability):
    N,D = parents.shape
    offspring = np.empty((N,D))
    for i in range(int(N/2)):
        if np.random.uniform(0,1) < crossover_probability:
            crossover_point = np.random.randint(1,D)
            offspring[2*i] = np.hstack([parents[2*i, :crossover_point], parents[2*i+1, crossover_point:]])
            offspring[2*i+1] = np.hstack([parents[2*i+1, :crossover_point], parents[2*i, crossover_point:]])
        else:
            offspring[2*i] = parents[2*i]
            offspring[2*i+1] = parents[2*i+1]
    return offspring / offspring.sum(axis=1).reshape(-1,1)


def differential_crossover(F=0.5):
    def _differential_crossover(parents, crossover_probability):
        N,D = parents.shape
        offspring = np.empty((N,D))
        for i in range(int(N/3)):
            if np.random.uniform(0,1) < crossover_probability:
                offspring[3*i] = parents[3*i] + F*(parents[3*i+1] - parents[3*i+2])
                offspring[3*i+1] = parents[3*i+1] + F*(parents[3*i+2] - parents[3*i])
                offspring[3*i+2] = parents[3*i+2] + F*(parents[3*i] - parents[3*i+1])
            else:
                offspring[3*i] = parents[3*i]
                offspring[3*i+1] = parents[3*i+1]
                offspring[3*i+2] = parents[3*i+2]
        offspring = np.abs(offspring)
        return offspring / offspring.sum(axis=1).reshape(-1,1)

    return _differential_crossover


def change_pair_mutation(population, mutation_probability):
    N,D = population.shape
    for i in range(N):
        if np.random.uniform(0,1) < mutation_probability:
            j,k = np.random.choice(D, size=2, replace=False)
            delta = np.abs(np.random.normal(0, min(population[i,j], 1-population[i,k])/2))
            if population[i,j] - delta >= 0 and population[i,k] + delta <= 1:
                population[i,j] -= delta
                population[i,k] += delta
    return population


def swap_mutation(population, mutation_probability):
    N,D = population.shape
    for i in range(N):
        if np.random.uniform(0,1) < mutation_probability:
            j,k = np.random.choice(D, size=2, replace=False)
            population[i,j], population[i,k] = population[i,k], population[i,j]
    return population
