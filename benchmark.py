import job_shop
import argparse
from datetime import datetime


def run_benchmark(
    filename,
    generations=job_shop.GENERATIONS,
    population_size=job_shop.POP_SIZE,
    mutation_rate=job_shop.MUTATION_RATE,
    tournament_size=job_shop.TOURNAMENT_SIZE,
    keep=job_shop.KEEP,
    runs=30,
):
    print(f"Running benchmark on {filename} with {runs} runs...")
    print(
        f"Generations: {generations}, Population Size: {population_size}, Mutation Rate: {mutation_rate}, Tournament Size: {tournament_size}, Keep: {keep}"
    )
    with open(filename) as f:
        num_jobs, _ = map(int, f.readline().split())
        for _ in range(num_jobs):
            f.readline()
        bks = int(f.readline().strip())

    js = job_shop.JobShop(filename)
    solutions = []
    for i in range(runs):
        best, _ = js.solve(
            population_size, generations, mutation_rate, tournament_size, keep
        )
        makespan, _ = js.decode(best["chromosome"])
        print(f"Run {i+1}: Makespan = {makespan}")
        solutions.append(makespan)

    median = sorted(solutions)[runs // 2]
    avg = sum(solutions) / runs
    best = min(solutions)
    worst = max(solutions)
    rpd = (avg - bks) / bks * 100

    print(f"Best Makespan: {best}")
    print(f"Worst Makespan: {worst}")
    print(f"Median Makespan: {median}")
    print(f"Average Makespan: {avg:.2f}")
    print(f"Best Known Solution: {bks}")
    print(f"RPD: {rpd:.2f}%")

    with open("benchmark_results.txt", "a") as f:
        if f.tell() == 0:
            f.write(
                "Ran,Filename,Generations,Population Size,Mutation Rate,Tournament Size,Keep,Best,Worst,Median,Average,BKS,RPD\n"
            )
        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_line = f"{datetime_str},{filename},{generations},{population_size},{mutation_rate},{tournament_size},{keep},{best},{worst},{median},{avg:.2f},{bks},{rpd:.2f}\n"
        f.write(csv_line)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark Job Shop Scheduling Algorithm",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Path to the benchmark file",
        required=True,
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=job_shop.GENERATIONS,
        help="Number of generations",
    )
    parser.add_argument(
        "--population_size", type=int, default=job_shop.POP_SIZE, help="Population size"
    )
    parser.add_argument(
        "--mutation_rate",
        type=float,
        default=job_shop.MUTATION_RATE,
        help="Mutation rate",
    )
    parser.add_argument(
        "--tournament_size",
        type=int,
        default=job_shop.TOURNAMENT_SIZE,
        help="Tournament size for selection",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=job_shop.KEEP,
        help="Number of elite individuals to keep",
    )
    args = parser.parse_args()

    run_benchmark(
        filename=parser.parse_args().filename,
        generations=args.generations,
        population_size=args.population_size,
        mutation_rate=args.mutation_rate,
        tournament_size=args.tournament_size,
        keep=args.keep,
    )


if __name__ == "__main__":
    main()
