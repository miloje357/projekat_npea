import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

jobs = None
num_machines = None
num_jobs = None

def load_jobs(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    num_jobs, num_machines = map(int, lines[0].split())
    machines = []
    durations = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        machines.append(values[0::2])
        durations.append(values[1::2])

    jobs = []
    for i in range(len(machines)):
        jobs.append(list(zip(machines[i], durations[i])))

    return jobs, num_jobs, num_machines

def initialize_individual():
    individual = []
    for job_id, job in enumerate(jobs):
        individual += [job_id] * len(job)
    random.shuffle(individual)
    return individual

def decode(individual):
    machine_available = [0] * num_machines
    # belezi u kom trenutku masina zavrsava sa radom
    next_op = [0] * num_jobs
    # cuva koja je sledeca operacija za svaki posao
    job_availabe = [0] * num_jobs
    # belezi u kom trenutku se svaki posao zavrsava za svaku operaciju

    schedule = []  # (job, machine, start, finish)
 
    for job_id in individual:
        operation = next_op[job_id]
        # indeks operacije za posao koj treba zavrsiti
        machine, duration = jobs[job_id][operation]

        start = max(machine_available[machine], job_availabe[job_id])
        finish = start + duration

        machine_available[machine] = finish
        job_availabe[job_id] = finish
        next_op[job_id] += 1

        schedule.append((job_id, machine, start, finish))

    makespan = max(machine_available)
    return makespan, schedule

def fitness(individual):
    makespan, _ = decode(individual)
    return makespan

def selection(population, k = 3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: fitness(ind))
    return selected[0]

# pola iz roditelja 1
# pola iz roditelja 2
def order_crossover(parent1, parent2):
    counter = [0] * num_jobs
    size = len(parent1)
    child = [-1] * size
    a, b = sorted(random.sample(range(size), 2))
    child[a:b] = parent1[a:b]
    for i in range(len(counter)):
        counter[i] = child.count(i)
    p2_pointer = 0
    for i in range(size):
        if child[i] == -1:
            while counter[parent2[p2_pointer]] >= len(jobs[parent2[p2_pointer]]):
                p2_pointer += 1
            counter[parent2[p2_pointer]] += 1
            child[i] = parent2[p2_pointer]
            p2_pointer += 1
    return child

def mutate(individual, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm(pop_size=50, generations=300):
    population = [initialize_individual() for _ in range(pop_size)]
    best_history = []

    for gen in range(generations):
        new_population = []
        for _ in range(pop_size):
            parent1 = selection(population)
            parent2 = selection(population)

            child = order_crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population
        best = min(population, key=lambda ind: fitness(ind))
        best_history.append(fitness(best))

        if gen % 50 == 0:
            print(f"Generation {gen}, Best Makespan: {fitness(best)}")

    best_individual = min(population, key=lambda ind: fitness(ind))
    return best_individual, best_history

def plot_gantt(schedule):
    fig, ax = plt.subplots()

    colors = ['red', 'blue', 'green', 'orange', 'purple']
 
    for job, machine, start, finish in schedule:
        ax.barh(machine, finish - start, left=start, color=colors[job], edgecolor='black')
        ax.text(start + (finish - start)/2, machine, f'J{job}', ha='center', va='center', color='white')

    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title("Gantt Chart")
    plt.show()

def plot_convergence(history):
    plt.plot(history)
    plt.xlabel("Generation")
    plt.ylabel("Best Makespan")
    plt.title("Convergence")
    plt.show()

def main():
    global jobs, num_jobs, num_machines
    jobs, num_jobs, num_machines = load_jobs("jobs.txt")

#    parent1 = [1, 0, 0, 1, 1, 2, 2, 0, 2]
#    parent2 = [0, 2, 1, 2, 2, 0, 0, 1, 1]
#
#    child = order_crossover(parent1, parent2)
#    print(child)

    best, history = genetic_algorithm()

    best_makespan, best_schedule = decode(best)

    print("\nBest Chromosome:", best)
    print("Best Makespan:", best_makespan)

    plot_gantt(best_schedule)
    plot_convergence(history)

if __name__ == "__main__":
    main()
