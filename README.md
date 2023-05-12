# Noxim Simulation Runner

This script automates running Noxim simulations for different network configurations and parameters. It supports running simulations for parts A, B, and C, with specific modifications for part C.

## Requirements

- Python 3.7 or higher
- Noxim simulator installed and compiled

## Usage

To run the script, open a terminal and navigate to the directory containing the script. Then, run the following command:

```sh
python run.py <parts> --modifications <modifications>
```

Replace `<parts>` with the desired part to run (`a`, `b`, `c`, or `all`), and, optionally, `<modifications>` with the desired modification within part C (`buffer_size`, `hotspot_distribution`, `buffer_selection_strategy`, `routing_algorithm`, or `all`).

For example, to run all parts:

```sh
python run.py all
```

To run part C with the buffer size modifications:

```sh
python run.py c --modifications buffer_size
```

## Output

The script will create and store results in CSV format in each part's respective directory. The CSV files will contain the relevant metrics for each configuration or parameter value.

## Notes

Before running the script, make sure to set the correct path to the Noxim simulator by updating the `noxim_path` variable at the beginning of the script.
