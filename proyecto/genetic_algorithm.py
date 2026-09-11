import numpy as np

def fitness(board):
    n = len(board)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacks += 1
    return -attacks

def create_population(size, n):
    return [np.random.permutation(n) for _ in range(size)]

def selection(population, fitness_values, num_parents):
    sorted_indices = np.argsort(fitness_values)[-num_parents:]
    return [population[i] for i in sorted_indices]

def crossover(parent1, parent2):
    n = len(parent1)
    point = np.random.randint(1, n - 1)
    child = np.concatenate((parent1[:point], parent2[point:]))
    unique_values = set(child)
    missing_values = list(set(range(n)) - unique_values)
    np.random.shuffle(missing_values)
    for i in range(n):
        if list(child).count(child[i]) > 1:
            child[i] = missing_values.pop()
    return child

def mutation(board, mutation_rate=0.2):
    if np.random.rand() < mutation_rate:
        i, j = np.random.randint(0, len(board), size=2)
        board[i], board[j] = board[j], board[i]
    return board

def genetic_algorithm(n, population_size=100, generations=500, mutation_rate=0.2):
    population = create_population(population_size, n)
    best_fitness_values = []
    best_boards_history = []  # <-- nuevo: guardamos el tablero de cada generación

    for gen in range(generations):
        fitness_values = np.array([fitness(ind) for ind in population])
        best_index = np.argmax(fitness_values)

        best_fitness_values.append(fitness_values[best_index])
        best_boards_history.append(population[best_index].tolist())  # convertido ya aquí

        if fitness_values[best_index] == 0:
            return population[best_index], best_fitness_values, best_boards_history, gen + 1, True

        parents = selection(population, fitness_values, population_size // 2)
        new_population = []
        for _ in range(population_size):
            idx1, idx2 = np.random.choice(len(parents), size=2, replace=False)
            parent1, parent2 = parents[idx1], parents[idx2]
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child)
        population = new_population

    return None, best_fitness_values, best_boards_history, generations, False