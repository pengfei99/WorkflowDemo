
export LOG_PATH=/tmp/pokemon

export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_ingestion/ingest_source_data.py s3://pengfei/mlflow-demo/pokemon-cleaned.csv /tmp/pokemon