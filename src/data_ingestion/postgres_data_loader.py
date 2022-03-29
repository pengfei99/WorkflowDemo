import os
import sys

import pandas as pd
from sqlalchemy import create_engine

from src.log.LogManager import LogManager

my_logger = LogManager(__name__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug("Init postgres data loader")


def main():
    if len(sys.argv) != 9:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
        sys.exit(1)
    else:
        data_folder = sys.argv[1]
        input_file_name = sys.argv[2]
        login = sys.argv[3]
        pwd = sys.argv[4]
        host_url = sys.argv[5]
        port = sys.argv[6]
        db_name = sys.argv[7]
        table_name = sys.argv[8]
        input_file_path = f"{data_folder}/{input_file_name}"
    db_location = f"{host_url}:{port}/{db_name}"
    engine = create_engine(f"postgresql://{login}:{pwd}@{db_location}")
    df = pd.read_csv(input_file_path, sep=",", na_values=[""], index_col=0)
    try:
        df.to_sql(table_name, engine)
        my_logger.info(f"Table {table_name} has been created in database {db_location}")
    except ValueError as e:
        my_logger.error(f"Failed to load table {table_name} into database {db_location}")
        my_logger.error(e)


if __name__ == "__main__":
    main()
