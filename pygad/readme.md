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

