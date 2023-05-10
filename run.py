from pathlib import Path
import subprocess, re

noxim_path: Path = Path("noxim")


class Variable:
    name: str
    argument_name: str
    values: list
    
    def __init__(self, name: str, argument_name: str, values: list) -> None:
        self.name = name
        self.argument_name = argument_name
        self.values = values


def run(directory: Path, variable: Variable) -> None:
    with open(directory.joinpath("results.csv"), "w") as results_file:
        results_file.write(
            f"{variable.name},Total received packets,Total received flits,Received/Ideal flits ratio,Average wireless utilization,Global average delay (cycles),Max delay (cycles),Network throughput (flits/cycle),Average IP throughput (flits/cycle/IP),Total energy (J),Dynamic energy (J),Static energy (J)\n"
        )

        for iteration, value in enumerate(variable.values):
            progress = iteration / len(variable.values) * 10
            print(f"[{'#' * int(progress)}{' ' * int(10 - progress)}] {progress * 10:.2f}", end='\r')

            command = f"./{noxim_path.joinpath('bin', 'noxim')} -power {noxim_path}/bin/power.yaml -config {noxim_path.joinpath('configuration.yaml')} -{variable.argument_name} {value}"
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.DEVNULL, text=True
            )

            data_points = {
                "total_received_packets": r"(?<=Total received packets: )[0-9]+",
                "total_received_flits": r"(?<=Total received flits: )[0-9]+",
                "received_ideal_flits_ratio": r"(?<=Received/Ideal flits Ratio: )[0-9.]+",
                "average_wireless_utilization": r"(?<=Average wireless utilization: )[0-9]+",
                "global_average_delay": r"(?<=Global average delay \(cycles\): )[0-9.]+",
                "max_delay": r"(?<=Max delay \(cycles\): )[0-9]+",
                "network_throughput": r"(?<=Network throughput \(flits/cycle\): )[0-9.]+",
                "average_IP_throughput": r"(?<=Average IP throughput \(flits/cycle/IP\): )[0-9.]+",
                "total_energy": r"(?<=Total energy \(J\): )[0-9.e-]+",
                "dynamic_energy": r"(?<=Dynamic energy \(J\): )[0-9.e-]+",
                "static_energy": r"(?<=Static energy \(J\): )[0-9.e-]+",
            }

            extracted_data = [
                value,
                *[re.search(regex, output).group() for regex in data_points.values()],
            ]

            results_file.write(",".join(str(val) for val in extracted_data) + "\n")
            results_file.flush()


if __name__ == "__main__":
    import numpy as np
    
    start = 0.001
    step = 0.001
    
    variable = Variable("Packet injection rate", "pir", list(np.arange(start, 0.1, step)))

    run(Path.cwd(), variable)