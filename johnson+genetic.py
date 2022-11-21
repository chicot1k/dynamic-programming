from random import shuffle, randrange, sample, random
import matplotlib.pyplot as plt

Y = list([])


def johnson(times):
    job_count = len(times)
    job_ids = list(range(1, job_count + 1))
    
    l1 = []
    l2 = []
    for job_info in sorted(zip(job_ids, times), key=lambda t: min(t[1])):
        job_id = job_info[0]
        job_times = job_info[1]
        if job_times[0] < job_times[1]:
            l1.append(job_id)
        else:
            l2.insert(0, job_id)
    
    return l1 + l2 

def makespan(perm, times):
    job_count = len(perm)
    machine_count = len(times[0])
    
    makespan = [[0] * (machine_count + 1) for _ in range(0, job_count + 1)]
    for i, job in enumerate(perm):
        for machine in range(0, machine_count):
            makespan[i + 1][machine + 1] = max(makespan[i][machine + 1], makespan[i + 1][machine]) + times[job - 1][machine]
    
    return makespan[job_count][machine_count]

def genetic1(times):
    population_size = 100
    num_of_epochs = 100
    job_count = len(times)
    population = [list(range(1, job_count + 1)) for _ in range(0, population_size)]
    for individual in population:
        shuffle(individual)
        
    population_with_fitness = evaluate_fitness(population, times)    
    for _ in range(0, num_of_epochs):
        parents = choose_parents(population_with_fitness)
        children = breed(parents)
        mutate(children)
        population_with_fitness = merge(population_with_fitness, evaluate_fitness(children, times))
    return choose_best(population_with_fitness)[0]

def pmx2(a, b):
    length = len(a)
    left = randrange(0, length + 1)
    right = randrange(left, length + 1)
    
    a2 = a[left:right]
    b2 = b[left:right]
    d = dict(zip(a2, b2))
    d_inv = dict(zip(b2, a2))
   
    child1 = list(map(lambda x: translate(x, d_inv), a[0:left])) + b2 + list(map(lambda x: translate(x, d_inv), a[right:length + 1]))
    child2 = list(map(lambda x: translate(x, d), b[0:left])) + a2 + list(map(lambda x: translate(x, d), b[right:length + 1]))
    
    return [child1, child2]   

def genetic2(times):
    population_size = 200
    num_of_epochs = 200
    job_count = len(times)
    population = [list(range(1, job_count + 1)) for _ in range(0, population_size)]
    for individual in population:
        shuffle(individual)
        
    population_with_fitness = evaluate_fitness(population, times)    
    for _ in range(0, num_of_epochs):
        parents = choose_parents(population_with_fitness)
        children = breed2(parents)
        mutate(children)
        population_with_fitness = merge(population_with_fitness, evaluate_fitness(children, times))
        Y.append(choose_best(population_with_fitness)[1])
    return choose_best(population_with_fitness)[0]

def evaluate_fitness(population, times):
    return [(individual, makespan(individual, times)) for individual in population]

def choose_parents(population):
    parents = []
    for _ in range(0, len(population)):
        tournament = sample(population, 5)
        parents.append(choose_best(tournament))
    return parents

def breed(parents):
    shuffle(parents)
    children = []
    for i in range(1, len(parents), 2):
        children += pmx(parents[i - 1][0], parents[i][0])
    return children

def breed2(parents):
    shuffle(parents)
    children = []
    for i in range(1, len(parents), 2):
        children += pmx2(parents[i - 1][0], parents[i][0])
    return children

def mutate(children):
    for child in children:
        if random() > 0.6:
            left = randrange(0, len(child))
            right = randrange(left, len(child))
           
            tmp = child[left]
            child[left] = child[right]
            child[right] = tmp   

def merge(parents, children):
    both = parents + children
    both.sort(key=lambda x: x[1])
    return both[:len(parents)]

def choose_best(population):
    return min(population, key=lambda x: x[1])

def translate(x, d):
    while x in d and x != d[x]:
        x = d[x]
    return x
def shift(seq, shift=1):
    return seq[-shift:] + seq[:-shift]

def pmx(a, b):
    length = len(a)
    left = randrange(0, length + 1)
    right = randrange(left, length + 1)
    
    a2 = a[left:right]
    b2 = b[left:right]
    d = dict(zip(a2, b2))
    d_inv = dict(zip(b2, a2))
    child1 = shift(b[0:left],1) + b2 + shift(b[right:length],1)
    child2 = shift(a[0:left],1) + a2 + shift(a[right:length],1)
    
    return [child1, child2] 


A = [[1,1,1,4,3,5,5,7,6,4
],[2,5,4,3,1,9,5,4,7,0
],[5,6,8,4,4,2,5,6,7,5
],[4,1,5,6,5,7,9,2,6,2
],[4,4,2,7,3,6,5,2,4,1
],[7,6,2,5,4,1,4,7,5,5
],[8,5,8,7,9,5,3,5,1,5
],[4,2,5,8,9,9,4,7,5,8
],[2,7,4,2,5,4,5,8,4,3
],[6,5,1,9,4,4,7,6,5,1
],[5,4,7,3,9,1,4,7,3,2
],[2,4,9,2,4,5,2,1,4,2
],[4,0,1,2,2,3,1,4,2,8
],[1,2,5,7,8,6,2,1,4,8
],[6,4,5,1,2,4,5,6,2,9
],[4,5,3,1,8,7,0,1,4,6
],[7,3,1,4,7,0,4,1,5,6
],[5,2,4,1,2,7,5,3,2,3
],[8,6,8,5,7,4,2,5,9,5
],[4,5,3,5,7,9,2,4,5,8]]
B = [[1,6],[2,9],[4,8],[5,9],[9,5],[4,3],[7,2],[6,3]]
B_res = genetic2(B)
A1_res = genetic1(A)
A2_res = genetic2(A)
print(A1_res,makespan(A1_res,A))
print(A2_res,makespan(A2_res,A))
print("------------------------")
print(B_res,makespan(B_res,B))
print(johnson(B),makespan(johnson(B),B))
Y = Y[200:]
X = list(range(1, 201))
fig = plt.subplots()
plt.plot(X,Y)
plt.show()
