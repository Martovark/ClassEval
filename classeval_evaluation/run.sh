#!/bin/bash

eval_file=$1
dump=$2

echo "Dump folder ${dump}"

folder_path="../output/model_output"

source ../proj_env/bin/activate
mv $dump "../"
mkdir -p $folder_path

mv "../${dump}/cache/${eval_file}.jsonl" "${folder_path}"

for file_path in "$folder_path"/*; do
    echo "$file_path"
    if [ -f "$file_path" ]; then
        file_name=$(basename "$file_path")

        file_name_no_extension="${file_name%.*}"
        echo "$file_name_no_extension"

        IFS="_" read -ra elements <<< "$file_name_no_extension"
        last_element="${elements[-1]}"

        python evaluation.py --source_file_name "${file_name_no_extension}" --dump "${dump}" \
            --eval_data ClassEval_data --eval_file $eval_file --greedy 1 --custom
    fi
done

mv "${folder_path}/${eval_file}.jsonl" "../${dump}/cache/"
mv "../${dump}" "./"
