import random
import tsplib95



def city_swap(solution):
    neighborhood = []
    n = len(solution)

    for i in range(n):
        for j in range(i + 1, n):
            new_solution = solution.copy()
            new_solution[i] = solution[j]
            new_solution[j] = solution[i]
            neighborhood.append(new_solution)

    return neighborhood



def genetic_algorithm(population):
    while True:
        # Выбор родителей
        lengths = [path_length(solution) for solution in population]
        weights = [(1 / length) for length in lengths]

        best = rand = population[lengths.index(min(lengths))]
        while best == rand:
            rand = population[lengths.index(*random.choices(lengths, weights))]



        # Скрещивание
        l = random.randint(0, len(best) - 1)

        new_1 = best[:l]
        new_2 = rand[:l]
        for i in range(len(best)):
            if rand[i] not in new_1:
                new_1.append(rand[i])

            if best[i] not in new_2:
                new_2.append(best[i])



        # Мутация
        i1 = i2 = 0
        while i1 == i2:
            i1 = random.randint(0, len(best) - 1)
            i2 = random.randint(0, len(best) - 1)

        new_1[i1], new_1[i2] = new_1[i2], new_1[i1]
        new_2[i1], new_2[i2] = new_2[i2], new_2[i1]



        # Добавление в окрестность
        new_population =  population + [new_1, new_2]
        lengths        += [path_length(new_1), path_length(new_2)]

        for i in range(2):
            new_population.pop(lengths.index(max(lengths)))
            lengths.remove(max(lengths))

        if population == new_population:
            return min(lengths)
        else:
            population = new_population



def path_length(solution):
    length = cities[solution[-1]][solution[0]]

    for i in range(len(solution) - 1):
        length += cities[solution[i]][solution[i + 1]]

    return length



for test in ('test_1(29).tsp', 'test_2(58).tsp', 'test_3(561).tsp'):
    data   = tsplib95.load(test)
    n      = data.dimension
    cities = [[0] * n for _ in range(n)]

    for i in range(0, n):
        for j in range(0, n):
            if test != 'test_2(58).tsp':
                cities[i][j] = data.get_weight(i + 1, j + 1)
            else:
                cities[i][j] = data.get_weight(i, j)

    initial_solution = [i for i in range(len(cities))]

    print(test, "- длина найденного решения:", genetic_algorithm(city_swap(initial_solution)))
