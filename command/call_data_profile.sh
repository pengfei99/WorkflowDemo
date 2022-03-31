export LOG_PATH=/tmp/pokemon
export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_profiling/generate_data_profile.py /tmp/pokemon pokemon-cleaned.csv pokemon-profile-report.html