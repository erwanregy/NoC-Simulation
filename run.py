from pathlib import Path
import subprocess, re, argparse, time

noxim_path: Path = Path("~/noxim")


class Variable:
    name: str
    values: list
    arguments: list[str]

    def __init__(self, name: str, values: list, arguments: list[str]) -> None:
        self.name = name
        self.values = values
        self.arguments = arguments


data_patterns = [
    r"(?<=Total received packets: )[0-9]+",
    r"(?<=Total received flits: )[0-9]+",
    r"(?<=Received/Ideal flits Ratio: )[0-9.]+",
    r"(?<=Average wireless utilization: )[0-9]+",
    r"(?<=Global average delay \(cycles\): )[0-9.]+",
    r"(?<=Max delay \(cycles\): )[0-9]+",
    r"(?<=Network throughput \(flits/cycle\): )[0-9.]+",
    r"(?<=Average IP throughput \(flits/cycle/IP\): )[0-9.]+",
    r"(?<=Total energy \(J\): )[0-9.e-]+",
    r"(?<=Dynamic energy \(J\): )[0-9.e-]+",
    r"(?<=Static energy \(J\): )[0-9.e-]+",
]


def run(directory: Path, variable: Variable) -> None:
    with open(directory.joinpath("results.csv"), "w") as results_file:
        results_file.write(
            f"{variable.name},Total received packets,Total received flits,Received/Ideal flits ratio,Average wireless utilization,Global average delay (cycles),Max delay (cycles),Network throughput (flits/cycle),Average IP throughput (flits/cycle/IP),Total energy (J),Dynamic energy (J),Static energy (J)\n"
        )
        results_file.flush()

        for iteration, (value, argument) in enumerate(
            zip(variable.values, variable.arguments)
        ):
            progress = iteration / (len(variable.values) - 1) * 20
            print(
                f"\r[{'=' * int(progress)}{' ' * (20 - int(progress))}] {int(progress * 5)}% ",
                end="",
            )

            command = f"{noxim_path.joinpath('bin', 'noxim')} -power {noxim_path.joinpath('bin', 'power.yaml')} -config '{directory.joinpath('configuration.yaml')}' {argument}"
            output = subprocess.check_output(
                command, shell=True, text=True, stderr=subprocess.DEVNULL
            )

            data = [str(value)]
            for pattern in data_patterns:
                match = re.search(pattern, output)
                if match:
                    data.append(match.group())
                else:
                    data.append("")

            results_file.write(",".join(data_point for data_point in data) + "\n")
            results_file.flush()
    print()

def part_a():
    print("Part A")

    import numpy as np

    start = 0.001
    step = 0.001
    end = 0.1

    values = np.arange(start, end + step, step).round(3).tolist()
    
    arguments = [f"-pir {value} poisson" for value in values]

    packet_injection_rate = Variable(
        "Packet injection rate",
        values,
        arguments
    )

    run(Path.cwd().joinpath("Part A"), packet_injection_rate)


def part_b():
    print("Part B")
    
    import numpy as np

    start = 0.001
    step = 0.001
    end = 0.1

    values = np.arange(start, end + step, step).round(3).tolist()

    arguments = [
        f"-pir {value} poisson -hs 0 0.05 -hs 1 0.05 -hs 2 0.05 -hs 3 0.05 -hs 8 0.05 -hs 9 0.05 -hs 10 0.05 -hs 11 0.05"
        for value in values
    ]

    packet_injection_rate = Variable(
        "Packet injection rate",
        values,
        arguments
    )

    run(Path.cwd().joinpath("Part B"), packet_injection_rate)


def part_c_buffer_size():
    print("Part C: Buffer size")
    values = [2 ** size for size in range(1, 7)]

    arguments = [
        f"-buffer {value} -pir 0.01 poisson -hs 0 0.05 -hs 1 0.05 -hs 2 0.05 -hs 3 0.05 -hs 8 0.05 -hs 9 0.05 -hs 10 0.05 -hs 11 0.05"
        for value in values
    ]

    buffer_size = Variable(
        "Buffer size",
        values,
        arguments,
    )

    run(Path.cwd().joinpath("Part C", "Buffer Size"), buffer_size)


def part_c_routing_algorithm():
    print("Part C: Routing Algorithm")
    
    values = [
        "XY",
        "West First",
        "North Last",
        "Negative First",
        "Odd Even",
        "Dyad",
    ]

    arguments = [
        f"-routing {value.upper().replace(' ', '_')}{' 0.6' if value == 'Dyad' else ''} -pir 0.01 poisson -hs 0 0.05 -hs 1 0.05 -hs 2 0.05 -hs 3 0.05 -hs 8 0.05 -hs 9 0.05 -hs 10 0.05 -hs 11 0.05"
        for value in values
    ]
    
    routing_algorithm = Variable(
        "Routing algorithm",
        values,
        arguments,
    )
    
    run(Path.cwd().joinpath("Part C", "Routing Algorithm"), routing_algorithm)


def part_c_buffer_selection_strategy():
    print("Part C: Buffer selection strategy")
    values = [
        "Random",
        "Buffer level",
        "Nop",
    ]

    arguments = [
        f"-sel {value.upper().replace(' ', '_')} -pir 0.1 poisson -hs 0 0.05 -hs 1 0.05 -hs 2 0.05 -hs 3 0.05 -hs 8 0.05 -hs 9 0.05 -hs 10 0.05 -hs 11 0.05"
        for value in values
    ]

    buffer_selection_strategy = Variable(
        "Buffer selection strategy",
        values,
        arguments,
    )

    run(
        Path.cwd().joinpath("Part C", "Buffer Selection Strategy"),
        buffer_selection_strategy,
    )


def part_c_hotspot_distribution():
    print("Part C: Hotspot distribution")
    
    values = [
        "Corner",
        "Centre",
        "Sides",
        "Diagonals",
    ]

    arguments = [
        "-pir 0.01 poisson -hs 0 0.05 -hs 1 0.05 -hs 2 0.05 -hs 3 0.05 -hs 8 0.05 -hs 9 0.05 -hs 10 0.05 -hs 11 0.05",
        "-pir 0.01 poisson -hs 26 0.05 -hs 27 0.05 -hs 28 0.05 -hs 29 0.05 -hs 34 0.05 -hs 35 0.05 -hs 36 0.05 -hs 37 0.05",
        "-pir 0.01 poisson -hs 0 0.05 -hs 3 0.05 -hs 7 0.05 -hs 31 0.05 -hs 32 0.05 -hs 56 0.05 -hs 60 0.05 -hs 63 0.05",
        "-pir 0.01 poisson -hs 0 0.05 -hs 7 0.05 -hs 18 0.05 -hs 21 0.05 -hs 42 0.05 -hs 45 0.05 -hs 56 0.05 -hs 63 0.05",
    ]

    hotspot_distribution = Variable(
        "Hotspot distribution",
        values,
        arguments,
    )

    run(Path.cwd().joinpath("Part C", "Hotspot Distribution"), hotspot_distribution)


def main():
    parser = argparse.ArgumentParser(description="Run Noxim simulations")

    parser.add_argument(
        "parts",
        choices=["a", "b", "c", "all"],
        help="Part to run",
    )
    parser.add_argument(
        "-m",
        "--modifications",
        choices=[
            "buffer_size",
            "routing_algorithm",
            "buffer_selection_strategy",
            "hotspot_distribution",
            "all",
        ],
        help="Part C modification to run",
        nargs="+",
    )

    args = parser.parse_args()

    start_time = time.time()
    
    if "a" in args.parts:
        part_a()
    if "b" in args.parts:
        part_b()
    if "c" in args.parts:
        if "buffer_size" in args.modifications:
            part_c_buffer_size()
        if "buffer_selection_strategy" in args.modifications:
            part_c_buffer_selection_strategy()
        if "routing_algorithm" in args.modifications:
            part_c_routing_algorithm()
        if "hotspot_distribution" in args.modifications:
            part_c_hotspot_distribution()
        elif "all" in args.modifications:
            part_c_buffer_size()
            part_c_routing_algorithm()
            part_c_buffer_selection_strategy()
            part_c_hotspot_distribution()
        else:
            raise ValueError("No modifications specified")
    elif "all" in args.parts:
        part_a()
        part_b()
        part_c_buffer_size()
        part_c_routing_algorithm()
        part_c_buffer_selection_strategy()
        part_c_hotspot_distribution()
    else:
        raise ValueError("No parts specified")
        
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
