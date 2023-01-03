import csv
import datetime
import errno
import os
from pathlib import Path
import subprocess
from Dataset import Dataset
from constants import METANOME_ALGORITHM_LOCATION, METANOME_CLI_LOCATION, RESULTS_DIR


def build_sample_cmd(method, factor, table):
    return f"python sample.py --method {method} --factor {factor} {table}"


def build_metanome_cmd(table_path: str, output_path: str, separator: str):
    return f"""java -Dtinylog.level=trace \
        -cp {METANOME_CLI_LOCATION}:{METANOME_ALGORITHM_LOCATION} de.metanome.cli.App \
        --algorithm de.metanome.algorithms.hyfd.HyFD \
        --files {table_path} --file-key INPUT_GENERATOR \
        --header --separator "{separator}"\
        -o file:{output_path}
    """


def build_fd_error_cmd(
    mode: str, table_path: str, fd_jsons: list[Path], out_file: str = "errors.json"
):
    return f"""cargo run --manifest-path analyze_fds/error-measures/Cargo.toml --release -- '{str(table_path)}' {mode} '{"' '".join(map(str, fd_jsons))}' > {out_file}"""


def build_violin_plot_cmd(errors_json_path: str):
    return f"cat {errors_json_path} | ./analyze_fds/error-measures/violin_plot.py"


build_mv_cmd = lambda old_path, new_path: f"mv {str(old_path)} {str(new_path)}"

build_plot_cmd = (
    lambda fd_json_sources: f"python analyze_fds/fd_count/src/main.py --save --data-sources {' '.join(map(str, fd_json_sources))}"
)


def build_uniqueness_cmd(experiment_dir: str):
    return f"""
        python analyze_fds/fd_count/src/unique_values.py -s "{str(experiment_dir)}"
        python analyze_fds/fd_count/src/plot_uniques.py -s {os.path.join(str(experiment_dir), "uniques.csv")}
    """


def run_cmd_get_last_line(cmd: str):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # TODO: this is synchronous, so not working for large pipes...
    out, err = p.communicate()
    # Output ends with \n, so we need second last line
    return out.decode().split("\n")[-2]


def runShell(cmd: str):
    return subprocess.run(cmd, shell=True)


def create_results_dir(folder_name: str):
    mydir = os.path.join(
        os.getcwd(),
        RESULTS_DIR,
        datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S_{folder_name}"),
    )
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return mydir


def rewrite_separator(dataset, source_table):
    bak_path = source_table + ".bak"
    if not os.path.exists(bak_path):
        runShell(build_mv_cmd(source_table, bak_path))
        reader = csv.reader(open(bak_path, newline=None), delimiter=dataset.separator)
        writer = csv.writer(open(source_table, "w"), delimiter=Dataset.separator)
        writer.writerows(reader)
    dataset.separator = Dataset.separator


def sample_with_method(method, factor, experiment_dir, source_table) -> Path:
    # Sample something
    if method != "full":
        sample_path = Path(
            run_cmd_get_last_line(build_sample_cmd(method, factor, source_table))
        )
    else:
        sample_path = Path(experiment_dir, "full.csv")
        runShell(f"cp {source_table} {sample_path}")

    return sample_path
