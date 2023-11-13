# Copyright 2023 Flavien Solt, ETH Zurich.
# Licensed under the General Public License, Version 3.0, see LICENSE for details.
# SPDX-License-Identifier: GPL-3.0-only

import multiprocessing as mp
import os
import subprocess

# Set to false if you do not have modelsim installed
DO_MODELSIM = False
if not DO_MODELSIM:
    print("Info: if you want to test with Modelsim, you should set DO_MODELSIM to True to run Modelsim simulations, assuming you have it installed.")

clock_polarities = [False, True]
rst_polarities = [False, True]
data_vals = [False, True]
clock_vals = [False, True]
rst_vals = [False, True]

output_bit_vals_icarus = []
output_bit_vals_verilator = []

def get_output_bit_vals_icarus_verilator(clock_polarity: bool, rst_polarity: bool, data_val: bool, clock_val: bool, rst_val: bool):
    # First, adapt the polarities
    with open("top_template.sv", "r") as f:
        top_template = f.read()
    top_template = top_template.replace("POLARITY_0", 'posedge' if clock_polarity else 'negedge')
    top_template = top_template.replace("POLARITY_1", 'posedge' if rst_polarity else 'negedge')

    top_dir = f"top_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(rst_val)}_{int(clock_val)}"
    os.makedirs(f"{top_dir}", exist_ok=True)
    with open(f"{top_dir}/top.sv", "w") as f:
        f.write(top_template)

    input_val_str = f"{int(data_val)}{int(rst_val)}{int(clock_val)}"
    # TODO Continuer ici
    # Verilator template
    with open("verilator_tb.cc.template", "r") as f:
        template = f.read()
    template = template.replace("TEMPLATE_IN_DATA", input_val_str)
    with open(f"{top_dir}/verilator_tb.cc", "w") as f:
        f.write(template)
    # Icarus template
    with open("tb_icarus.sv.template", "r") as f:
        template = f.read()
    template = template.replace("TEMPLATE_IN_DATA", input_val_str)
    with open(f"{top_dir}/tb_icarus.sv", "w") as f:
        f.write(template)
    # Modelsim template
    with open("modelsim.tcl.template", "r") as f:
        template = f.read()
    template = template.replace("TEMPLATE_DIR", f"{top_dir}")
    with open(f"{top_dir}/modelsim.tcl", "w") as f:
        f.write(template)

    # Run Verilator
    cmd_str = f"verilator --cc --exe --build {top_dir}/verilator_tb.cc {top_dir}/top.sv -CFLAGS '-g' --Mdir obj_dir_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(clock_val)}_{int(rst_val)} && ./obj_dir_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(clock_val)}_{int(rst_val)}/Vtop"
    verilator_result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    verilator_lines = verilator_result.stdout.split("\n")
    output_bit_val_verilator = None
    for line in verilator_lines:
        if line.startswith("Output bit:"):
            output_bit_val_verilator = line.split(" ")[-1][:-1]
            break

    # Run Icarus
    os.makedirs(f"icarus_obj_dir_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(clock_val)}_{int(rst_val)}", exist_ok=True)
    cmd_str = f"iverilog -g2012 -o icarus_obj_dir_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(clock_val)}_{int(rst_val)}/Vtop {top_dir}/top.sv {top_dir}/tb_icarus.sv && vvp icarus_obj_dir_{int(clock_polarity)}_{int(rst_polarity)}_{int(data_val)}_{int(clock_val)}_{int(rst_val)}/Vtop"
    icarus_result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    icarus_lines = icarus_result.stdout.split("\n")
    output_bit_val_icarus = None
    for line in icarus_lines:
        if line.startswith("Output bit:"):
            output_bit_val_icarus = line.split(" ")[-1][:-1]
            break

    # Run Modelsim
    if DO_MODELSIM:
        cmd_str = f"vsim -64 -c -do {top_dir}/modelsim.tcl"
        modelsim_result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
        modelsim_lines = modelsim_result.stdout.split("\n")
        output_bit_val_modelsim = None
        for line in modelsim_lines:
            if "Output bit:" in line:
                output_bit_val_modelsim = line.split(" ")[-1][:-1]
                break
    else:
        output_bit_val_modelsim = "N/A"

    return output_bit_val_icarus, output_bit_val_verilator, output_bit_val_modelsim

def adapt_polarities(clock_polarity: bool, rst_polarity: bool):
    # First, adapt the polarities
    with open("top_template.sv", "r") as f:
        top_template = f.read()
    top_template = top_template.replace("POLARITY_0", 'posedge' if clock_polarity else 'negedge')
    top_template = top_template.replace("POLARITY_1", 'posedge' if rst_polarity else 'negedge')
    with open("top.sv", "w") as f:
        f.write(top_template)

workloads = []
for clock_polarity in clock_polarities:
    for rst_polarity in rst_polarities:
        for data_val in data_vals:
            for clock_val in clock_vals:
                for rst_val in rst_vals:
                    workloads.append((clock_polarity, rst_polarity, data_val, clock_val, rst_val))

with mp.Pool(processes=mp.cpu_count()) as pool:
    results = pool.starmap(get_output_bit_vals_icarus_verilator, workloads)

table_lines = [None] * (len(workloads) + 2)
table_lines[0] = "Row ID | Clock polarity | Reset polarity | Data value | Clock value | Reset value | Output bit (Verilator) | Output bit (Icarus) | Output bit (Commercial)"
table_lines[1] = "-------|----------------|----------------|------------|-------------|-------------|------------------------|---------------------|----------------------"
for i, workload in enumerate(workloads):
    table_lines[i+2] = f"{i:<6} | {workload[0]:<14} | {workload[1]:<14} | {workload[2]:<10} | {workload[3]:<11} | {workload[4]:<11} | {results[i][1]:<22} | {results[i][0]:<19} | {results[i][2]:<24}"
with open("results.txt", "w") as f:
    f.write("\n".join(table_lines))
