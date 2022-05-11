import pygad
import numpy
import pandas
import matplotlib.pyplot as plt
from scipy import stats

def fitness_func(solution, solution_idx):
    pv, sv = kolmogorov_smirnov(solution)
    fitness = 2 / (numpy.abs(1 - pv) + sv*20)
    return fitness

def on_generation(ga_instance):
    global last_fitness
    print("Generation = {}".format(ga_instance.generations_completed))
    print("Fitness = {}".format(ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
    print("Change = {}".format(ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
    last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

def kolmogorov_smirnov(solution):
    df = pandas.DataFrame(data={
        'solution': solution
    })
    if (ga_instance.generations_completed == num_generations or ga_instance.generations_completed == 0):
        df.to_csv("solution_{}.csv".format(ga_instance.generations_completed))

    return stats.kstest(df, 'norm', (df.mean(), df.std()), N=5000)

num_generations = 100
num_parents_mating = 10
sol_per_pop = 20
num_genes = 50
gene_space = range(25)


last_fitness = 0

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       gene_space=gene_space,
                       fitness_func=fitness_func,
                       on_generation=on_generation)

ga_instance.run()

df1 = pandas.read_csv("solution_0.csv")
df2 = pandas.read_csv("solution_{}.csv".format(num_generations))
df1['solution'].plot(kind='bar')
plt.show()
df2['solution'].plot(kind='bar')
plt.show()
df12 = pandas.DataFrame(data={
    'Первое поколение': df1['solution'],
    'Последнее поколение': df2['solution'],
})
df12.plot.kde()
plt.show()

filename = 'genetic'
ga_instance.save(filename=filename)
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()
plt.show()

solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
print("Parameters of the best solution : {solution}".format(solution=solution))
