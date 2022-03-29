export LOG_PATH=/tmp/pokemon
export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_transformation/generate_pokemon_score.py /tmp/pokemon pokemon-cleaned.csv pokemon-enriched.csv