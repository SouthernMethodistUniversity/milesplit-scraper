#!/bin/bash

lim=$1

# Submit the first job manually and store its job ID
jid=$(sbatch --parsable /users/mlangstonsmith/milesplit-scraper/get_data_links.sbatch 91 150)

# Start chunking from index 92
start=151
step=100

while [ $start -le $lim ]; do
    end=$((start + step - 1))
    if [ $end -gt $lim ]; then
        end=$lim
    fi

    # Submit batch job with dependency on the previous job
    jid=$(sbatch --parsable --dependency=afterany:$jid /users/mlangstonsmith/milesplit-scraper/get_data_links.sbatch $start $end)

    start=$((end + 1))
done