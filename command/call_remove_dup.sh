export LOG_PATH=/tmp/pokemon
export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_transformation/remove_duplication.py s3://pengfei/mlflow-demo/pokemon-raw.csv /tmp/pokemon