export LOG_PATH=/tmp/pokemon
export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_ingestion/postgres_data_loader.py /tmp/pokemon pokemon-enriched.csv pliu pliu 127.0.0.1 5432 north_wind pokemon_stat