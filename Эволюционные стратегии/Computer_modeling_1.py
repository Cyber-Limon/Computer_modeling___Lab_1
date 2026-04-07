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



def path_length(solution):
    length = cities[solution[-1]][solution[0]]

    for i in range(len(solution) - 1):
        length += cities[solution[i]][solution[i + 1]]

    return length



def evolutionary_strategies(cities):
    # Инициализация начального решения
    initial_solution = random.sample(range(len(cities)), len(cities))

    # Построение начальной популяции
    neighborhood  = city_swap(initial_solution)
    lengths       = [path_length(solution) for solution in neighborhood]
    _, population = zip(*sorted(zip(lengths, neighborhood)))
    population    = population[:u]

    for t in range(t_max):
        new_population = []

        for j in range(l):
            # Выбор родителя
            rand = random.sample(population, 1)[0]

            # Мутация
            i1 = i2 = 0
            while i1 >= i2:
                i1 = random.randint(0, len(rand) - 1)
                i2 = random.randint(0, len(rand) - 1)

            new_population.append(rand[:i1] + rand[i1:i2][::-1] + rand[i2:])

        # Выбор 'u' лучших из 'l' возможных
        lengths       = [path_length(solution) for solution in new_population]
        _, population = zip(*sorted(zip(lengths, new_population)))
        population    = population[:u]

    # Получение лучшего решения
    lengths = [path_length(solution) for solution in population]
    lengths = min(lengths)

    return lengths



print("Результаты:")

t_max = 10000   # Количество итераций
l     = 300     # Количество родителей
u     = 150     # Количество потомков

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

    print(f"- {test:<15} - длина найденного решения {evolutionary_strategies(cities)}")
