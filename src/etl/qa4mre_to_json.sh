#!/bin/bash

if [[ "$#" -lt 1 ]]; then
  echo "Usage qa4mre_to_json <cuid_dataset_folder> <output folder>"
  exit 0
fi

input_folder=$1
output_folder=${2:-$input_folder}
processor_script="src/etl/cuid_processor.py"

[ ! -d ${output_folder} ] && mkdir -p ${output_folder}

for cuid_prefix in 'A1' 'A2' 'B1' 'B2' 'C1'; do
    cuid_input_files=$(find ${input_folder} -iname ${cuid_prefix}_* | tr '\n' ' ')
    cuid_output_file="${output_folder}/cuid_${cuid_prefix,,}.json"
    echo "${processor_script} ${cuid_input_files} -o ${cuid_output_file}"
    python3 ${processor_script}  $cuid_input_files -o "${cuid_output_file}"
done
