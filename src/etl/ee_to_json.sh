#!/bin/bash

# requires xml2json, install it with npm i -g xml2json
if [[ "$#" -lt 1 ]]; then
    echo "Usage ee_prepare <ee_dataset_folder> <output folder>"
    exit 0
fi

input_folder=$1
output_folder=${2:-$input_folder}
processor_script="src/etl/ee_processor.py"

[ ! -d ${output_folder} ] && mkdir -p ${output_folder}

# convert all xml files to json, then json to RACE like format
for xml_file in $(find $input_folder -iname "*.xml"); do
    xml_file=$(basename ${xml_file})
    json_file=${xml_file%.*}.json
    echo "xml2json $xml_file /tmp/$json_file"
    cat ${input_folder}/${xml_file} | xml2json > /tmp/${json_file}
    echo "python /tmp/$json_file ${input_folder}/${json_file}"
    python3 ${processor_script} -i /tmp/${json_file} > ${output_folder}/${json_file}
done
