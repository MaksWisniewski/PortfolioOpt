# Optymalizacja Portfela 💹💸

# Opis 
Optymalizacja portfela jest szeroko badaną dziedziną we współczesnych finansach. 
Problem optymalizacji polega na znalezieniu optymalnego stosunku między dwoma sprzecznymi celami i.e ryzykiem i zwrotem. Wraz ze wzrostem liczby aktywów znacznie wzrasta złożoność portfeli, co stanowi wyzwanie obliczeniowe.

Celem projektu jest zbadanie zastosowania algorytmu NMOEA/D (Normalized Multi-Objective Evolutionary Algorithm based on decomposition) oraz algorytmu genetycznego (Non-dominated Sorting Genetic Algorithm).


## Definicja problemu optymalizacji

Rozważamy problem optymalizacji dwukryterialnej. 

wzorki


## Szczegółowy opis algorytmów xd

```python
    # initialize reference point
    reference_point = np.min(population_values, axis=0)

    # initialize neighborhoods
    weight_vectors_2 = np.sum(weight_vectors**2, axis=1)
    distance_matrix = weight_vectors_2.reshape(-1,1) - 2*(weight_vectors @ weight_vectors.T) + weight_vectors_2

    neighborhoods = np.empty((number_of_subproblems, neighborhood_size))
    neighborhoods = np.argsort(distance_matrix)[:,:neighborhood_size]

```

## Opis implementacji 

## Opis Wyników

## Wnioski końcowe 