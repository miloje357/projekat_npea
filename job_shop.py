import random
import argparse
import matplotlib.pyplot as plt


class JobShop:
    def __init__(self, jobs_file: str):
        self.jobs = []
        self.num_jobs = 0
        self.num_machines = 0
        self.set_jobs(jobs_file)

    def set_jobs(self, filename):
        with open(filename, "r") as f:
            first_line = f.readline().strip()
            self.num_jobs, self.num_machines = map(int, first_line.split())

            for _ in range(self.num_jobs):
                line = f.readline()
                parts = line.strip().split()
                job_operations = []
                for i in range(0, len(parts), 2):
                    machine = int(parts[i])
                    duration = int(parts[i + 1])
                    job_operations.append((machine, duration))
                self.jobs.append(job_operations)

    def init_chromosome(self):
        chromosome = []
        for job_id, job in enumerate(self.jobs):
            chromosome += [job_id] * len(job)
        random.shuffle(chromosome)
        return chromosome

    def decode(self, individual):
        machine_available = [0] * self.num_machines
        # belezi u kom trenutku masina zavrsava sa radom
        next_op = [0] * self.num_jobs
        # cuva koja je sledeca operacija za svaki posao
        job_availabe = [0] * self.num_jobs
        # belezi u kom trenutku se svaki posao zavrsava za svaku operaciju

        schedule = []  # (job, machine, start, finish)

        for job_id in individual:
            operation = next_op[job_id]
            # indeks operacije za posao koj treba zavrsiti
            machine, duration = self.jobs[job_id][operation]

            start = max(machine_available[machine], job_availabe[job_id])
            finish = start + duration

            machine_available[machine] = finish
            job_availabe[job_id] = finish
            next_op[job_id] += 1

            schedule.append((job_id, machine, start, finish))

        makespan = max(machine_available)
        return makespan, schedule

    def fitness(self, individual):
        if individual["fitness"] != -1:
            return individual["fitness"]
        makespan, _ = self.decode(individual["chromosome"])
        individual["fitness"] = makespan
        return makespan

    def selection(self, population, k):
        selected = random.sample(population, k)
        best = min(selected, key=lambda ind: self.fitness(ind))
        return best

    def order_crossover(self, parent1, parent2):
        counter = [0] * self.num_jobs
        size = len(parent1)
        child = [-1] * size
        a, b = sorted(random.sample(range(size), 2))
        child[a:b] = parent1[a:b]
        for i in range(a, b):
            counter[parent1[i]] += 1
        p2_pointer = 0
        for i in range(size):
            if child[i] == -1:
                while counter[parent2[p2_pointer]] >= len(
                    self.jobs[parent2[p2_pointer]]
                ):
                    p2_pointer += 1
                counter[parent2[p2_pointer]] += 1
                child[i] = parent2[p2_pointer]
                p2_pointer += 1
        return child

    def mutate(self, individual, mutation_rate):
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]

    # TODO: implementirati elitizam, tj. cuvanje najboljeg pojedinca iz prethodne generacije
    def solve(self, pop_size, generations, mutation_rate, tournament_size):
        population = [
            {"chromosome": self.init_chromosome(), "fitness": -1}
            for _ in range(pop_size)
        ]
        best_history = [-1] * generations

        for gen in range(generations):
            new_population = [
                {"chromosome": None, "fitness": -1} for _ in range(pop_size)
            ]
            for i in range(pop_size):
                parent1 = self.selection(population, tournament_size)["chromosome"]
                parent2 = self.selection(population, tournament_size)["chromosome"]

                child = self.order_crossover(parent1, parent2)
                self.mutate(child, mutation_rate)
                new_population[i]["chromosome"] = child

            population = new_population
            best = min(population, key=lambda ind: self.fitness(ind))
            best_history[gen] = self.fitness(best)

            if gen % 50 == 0:
                print(f"Generation {gen}, Best Makespan: {self.fitness(best)}")

        best_individual = min(population, key=lambda ind: self.fitness(ind))
        return best_individual, best_history


def plot_gantt(schedule):
    _, ax = plt.subplots()

    for job, machine, start, finish in schedule:
        ax.barh(machine, finish - start, left=start, edgecolor="black")
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
    parser = argparse.ArgumentParser(
        description="Genetic Algorithm for Job Shop Scheduling"
    )
    parser.add_argument(
        "--jobs_file", type=str, default="jobs.txt", help="Path to the jobs file"
    )
    parser.add_argument(
        "--population_size", type=int, default=50, help="Population size"
    )
    parser.add_argument(
        "--generations", type=int, default=300, help="Number of generations"
    )
    parser.add_argument(
        "--mutation_rate", type=float, default=0.1, help="Mutation rate"
    )
    parser.add_argument(
        "--tournament_size", type=int, default=5, help="Tournament size for selection"
    )
    args = parser.parse_args()

    js = JobShop(args.jobs_file)

    best, history = js.solve(
        args.population_size, args.generations, args.mutation_rate, args.tournament_size
    )

    best_makespan, best_schedule = js.decode(best["chromosome"])

    print("\nBest Chromosome:", best["chromosome"])
    print("Best Makespan:", best_makespan)

    plot_gantt(best_schedule)
    plot_convergence(history)


if __name__ == "__main__":
    main()
