
export LOG_PATH=/tmp/pokemon

export PYTHONPATH="${PYTHONPATH}:/home/pliu/git/WorkflowDemo"
python ../src/data_ingestion/s3_data_loader.py /tmp/pokemon pokemon-cleaned.parquet s3://pengfei/workflow-demo/pokemon/target