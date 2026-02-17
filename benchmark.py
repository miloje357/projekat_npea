import job_shop


def run_benchmark(
    filename,
    generations=job_shop.GENERATIONS,
    population_size=job_shop.POP_SIZE,
    mutation_rate=job_shop.MUTATION_RATE,
    tournament_size=job_shop.TOURNAMENT_SIZE,
    runs=10,
):
    print(f"Running benchmark on {filename} with {runs} runs...")
    print(
        f"Generations: {generations}, Population Size: {population_size}, Mutation Rate: {mutation_rate}, Tournament Size: {tournament_size}"
    )
    with open(filename) as f:
        num_jobs, _ = map(int, f.readline().split())
        for _ in range(num_jobs):
            f.readline()
        best_makespan = int(f.readline().strip())

    # TODO: Bolja statistika
    js = job_shop.JobShop(filename)
    avg = 0
    for i in range(runs):
        best, _ = js.solve(generations, population_size, mutation_rate, tournament_size)
        makespan, _ = js.decode(best["chromosome"])
        print(f"Run {i+1}: Makespan = {makespan}")
        avg += makespan

    avg /= runs
    print(f"Average Makespan: {avg:.2f}")
    print(f"Best Known Makespan: {best_makespan}")


def main():
    # TODO: Biranje benchmark-a preko komandne linije
    # TODO: Rezultati u fajl
    run_benchmark("benchmarks/ft06.txt")


if __name__ == "__main__":
    main()
