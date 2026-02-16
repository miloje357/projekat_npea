import random
import matplotlib.pyplot as plt

jobs = []
num_machines = -1
num_jobs = -1


def set_jobs(filename):
    global jobs, num_jobs, num_machines
    with open(filename, "r") as f:
        first_line = f.readline().strip()
        num_jobs, num_machines = map(int, first_line.split())

        jobs = []
        for line in f:
            parts = line.strip().split()
            job_operations = []
            for i in range(0, len(parts), 2):
                machine = int(parts[i])
                duration = int(parts[i + 1])
                job_operations.append((machine, duration))
            jobs.append(job_operations)


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


def selection(population, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: fitness(ind))
    return selected[0]


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
    _, ax = plt.subplots()

    colors = ["red", "blue", "green", "orange", "purple"]

    for job, machine, start, finish in schedule:
        ax.barh(
            machine, finish - start, left=start, color=colors[job], edgecolor="black"
        )
        ax.text(
            start + (finish - start) / 2,
            machine,
            f"J{job}",
            ha="center",
            va="center",
            color="white",
        )

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
    set_jobs("jobs.txt")

    best, history = genetic_algorithm()

    best_makespan, best_schedule = decode(best)

    print("\nBest Chromosome:", best)
    print("Best Makespan:", best_makespan)

    plot_gantt(best_schedule)
    plot_convergence(history)


if __name__ == "__main__":
    main()
