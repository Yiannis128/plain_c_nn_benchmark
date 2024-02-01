#!/usr/bin/env python3

import os
from shutil import move

"""Script designed to fix a bug that plagued the initial run, all samples were placed
in reinforcement_learning folder, this bug uses patched-src-2 to place all the files
in esbmc_output in the correct subfolder."""

ESBMC_OUTPUT_PATH: str = "esbmc_output"
SOURCE_PATH: str = "patched-src-2"

# Mapping of filename to correct folder.
file_folders_map: dict[str, str] = {}

# Create mapping
for sub_folder in os.listdir(SOURCE_PATH):
    for file in os.listdir(f"{SOURCE_PATH}/{sub_folder}"):
        out_file: str = f"{file}.stdout.txt"
        file_folders_map[out_file] = sub_folder

# Move ESBMC folder to sync
for sub_folder in os.listdir(ESBMC_OUTPUT_PATH):
    for file in os.listdir(f"{ESBMC_OUTPUT_PATH}/{sub_folder}"):
        from_path: str = f"{ESBMC_OUTPUT_PATH}/{sub_folder}/{file}"
        to_path: str = f"{ESBMC_OUTPUT_PATH}/{file_folders_map[file]}/{file}"
        move(from_path, to_path)
        print(f"{from_path} ===> {to_path}")

