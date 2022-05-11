# Генетическое программирование при помощи PyGAD

Задача: создать с помощью генетического программирования 50 чисел в диапозоне от 0 до 25 и проверить нормальное ли распределение при помощи критерия Колмогорова-Смирнова

Нам понадобится `pip install pygad pandas scipy` (последнии два для работы с массивами данных)

```python
import pygad

num_generations = 100 # Количество поколений
num_parents_mating = 10 # Количество решений, которые будут выбраны в качестве родителей
sol_per_pop = 20 # Количество решений в популяции
num_genes = 50 # Количество чисел
gene_space = range(25) # Диапазон чисел

# Класс GA для построения генетического алгоритма
ga_instance = pygad.GA(num_generations=num_generations,    
                       num_parents_mating=num_parents_mating,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       gene_space=gene_space,
                       fitness_func=fitness_func,
                       on_generation=on_generation)
```
```python
last_fitness = 0

# Эта функция запускается в конце каждого поколения, в нашем случае, для того, чтобы узнать изменения между поколениями
def on_generation(ga_instance):
    global last_fitness
    print("Generation = {}".format(ga_instance.generations_completed))
    print("Fitness = {}".format(ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change = {}".format(ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]
```
```python
import numpy

# Функция, которая возращает значение пригодности решения
def fitness_func(solution, solution_idx):
    pv, sv = kolmogorov_smirnov(solution) # Критерий К-С (см. ниже)
    # Чем больше pv и ниже sv тем более вероятнее нормальность распределения
    # sv умножаю на 20, потому что по моему опыту sv часто принимает довольно маленькие значения, а 20 выявленно опытным путем
    fitness = 2 / (numpy.abs(1 - pv) + sv*20) 
    return fitness 
```
```python
import pandas
from scipy import stats

# Критерий Колмогорова-Смирнова
def kolmogorov_smirnov(solution):
    df = pandas.DataFrame(data={
        'solution': solution
    })
    # Первое и последнее поколение записываю для того, чтобы потом сравнить
    if (ga_instance.generations_completed == num_generations or ga_instance.generations_completed == 0):
        df.to_csv("solution_{}.csv".format(ga_instance.generations_completed))

    return stats.kstest(df, 'norm', (df.mean(), df.std()), N=5000) # Возвращает два значения: К-С-статитстика и Р-значение
```
```python 
# Для запуска генетического алгоритма
ga_instance.run()
```
