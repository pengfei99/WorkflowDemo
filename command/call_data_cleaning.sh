export LOG_PATH=/tmp/pokemon
export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_transformation/data_cleaning.py /tmp/pokemon pokemon-dedup.csv pokemon-cleaned.parquet parquet