#!/usr/bin/env python3

import os
from socket import gethostname
from subprocess import Popen, PIPE, STDOUT

# Inclusive lower bound
START_IDX = 0
# Inclusive upper bound
END_IDX = 999999999

SOURCE_DIRS: str = sorted([
    "patched-src-2/hopfield_nets",
    "patched-src-2/poly_approx",
    "patched-src-2/reach_prob_density",
    "patched-src-2/reinforcement_learning",
])
ESBMC_OUTPUT_DIR: str = "esbmc_output"
ESBMC_PARAMS: str = "--interval-analysis --goto-unwind --unlimited-goto-unwind --incremental-bmc --state-hashing --add-symex-value-sets --k-step 2 --floatbv --unlimited-k-steps --memory-leak-check --context-bound 2 --timeout 300 -Iincludes -Inetworks"

if not os.path.exists(ESBMC_OUTPUT_DIR):
   os.mkdir(f"{ESBMC_OUTPUT_DIR}")

# Get total file count to keep track.
total: int = 0
# Create missing directories
for source_dir in SOURCE_DIRS:
    folder_name: str = os.path.basename(source_dir)
    if not os.path.exists(f"{ESBMC_OUTPUT_DIR}/{folder_name}"):
        os.mkdir(f"{ESBMC_OUTPUT_DIR}/{folder_name}")
    total += len(os.listdir(source_dir))

# If end index is specified, use it.
if total > END_IDX:
    total = END_IDX

hostname: str = gethostname().split(".")[0]

overall_idx: int = 0
# Go through all category folders.
for source_dir in SOURCE_DIRS:
    # Iterate over the files.
    for file_name in sorted(os.listdir(source_dir)):
        # Get file path of the input file.
        file_path: str = f"{source_dir}/{file_name}"
        folder_name: str = os.path.basename(os.path.dirname(file_path))
        # Skip samples until reached range of indexes to work through.
        if overall_idx < START_IDX:
            print(f"Skipping {overall_idx} ... {START_IDX} - {END_IDX}: {folder_name}/{file_name}")
            overall_idx += 1
            continue
        # Stop scanning samples, as soon as the final index is passed.
        elif overall_idx > END_IDX:
            print("Reached end... {overall_idx}")
            exit(0)
        print(f"{START_IDX}/{overall_idx}/{total}: {folder_name}/{file_name}")
	
	    # Save current progress
        with open(f"progress-{hostname}", "w") as out:
            out.write(f"{START_IDX}/{overall_idx}/{total}: {folder_name}/{file_name}\n")

        # Run cmd
        process = Popen(f"esbmc {ESBMC_PARAMS} {file_path}".split(" "), stdout=PIPE, stderr=STDOUT)
        (output_bytes, output_err_bytes) = process.communicate()
        exit_code = process.wait()

        # Format outputs
        output: str = str(output_bytes).replace("\\n", "\n")
        output_err: str = str(output_err_bytes).replace("\\n", "\n") if output_err_bytes is not None else None

        # Save stdout
        with open(f"{ESBMC_OUTPUT_DIR}/{folder_name}/{file_name}.stdout.txt", "w") as out:
            out.write(output)

        # Save stderr
        if output_err is not None:
            with open(f"{ESBMC_OUTPUT_DIR}/{folder_name}/{file_name}.stderr.txt", "w") as out:
                out.write(output_err)

        overall_idx += 1

