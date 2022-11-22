import os
import subprocess

# Constants
results_dir = 'results'

# Cmds
build_sample_cmd = lambda m, f, p: f"python sample.py --method {m} --factor {f} {p}"
sample_cmd = 'python sample.py --method random --factor 0.15 source/adult.csv'

mv = lambda old_path, new_path: f"mv {old_path} {new_path}"

build_plot_cmd = lambda fd_json_folder, sources: f"python analyze_fds/fd_count/src/main.py --save --data-path {fd_json_folder} --data-sources {' '.join(sources)}"


def mv_to_results(file_name: str, path:str=None):
    src_path = os.path.join(path, file_name) if path else file_name
    target_path = os.path.join(results_dir, file_name)

    subprocess.run(mv(src_path, target_path), shell=True)

def run_cmd_get_last_line(cmd: str):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # TODO: this is synchronous, so not working for large pipes...
    out, err = p.communicate() 
    # Output ends with \n, so we need second last line
    return out.decode().split('\n')[-2]
    


def main():
    # Sample something
    sample_path = run_cmd_get_last_line(sample_cmd)

    # TODO: Run Metanome CLI

    # TODO: Rust not working on my machine :D

    # save fd_count plot
    plot_cmd = build_plot_cmd('data', ['full', 'kmeans_10'])
    plot_file_path = run_cmd_get_last_line(plot_cmd)

    mv_to_results(plot_file_path)


if __name__ == '__main__':
    main()