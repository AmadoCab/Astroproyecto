#!/usr/bin/env python3

import os
import subprocess

input_directory = 'LightCurves'
output_file = 'results.csv'

# Open the output file in write mode
with open(output_file, 'w') as f:
    # Iterate over all files in the directory
    f.write('Name,Modulation Index,Fractional Variability,Fractional Variability Error\n')
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            csv_path = os.path.join(input_directory, filename)

            result = subprocess.run(['python3', 'main.py', csv_path], capture_output=True, text=True)
            print(' '.join(['python3', 'main.py', csv_path]))

            # Check if the execution was successful
            if result.returncode == 0:
                # Split the output by comma and get the results
                output = result.stdout.strip()
                f.write(f'{filename.rsplit("_",4)[0]},{output}\n')
            else:
                # Write the error message if execution failed
                f.write(f'{filename}: Error executing main.py - {result.stderr.strip()}\n')

print(f'Processing complete. Results saved in {output_file}.')
