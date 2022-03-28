import sys

import pandas as pd
from pandas_profiling import ProfileReport

from src.log.LogManager import LogManager
from src.utile import get_local_input_file_path

my_logger = LogManager(__name__).get_logger()
my_logger.debug("Init ingest_source_data")


def main():
    remote_file_path = sys.argv[1]
    data_folder = sys.argv[2]
    input_file_path, file_name = get_local_input_file_path(remote_file_path, data_folder)
    df = pd.read_csv(input_file_path, sep=",", na_values=[""],index_col=0)
    my_logger.info("data sample :\n" + str(df.head(5)))
    profile = ProfileReport(df, title="pokemon_data_profiling", minimal=False, explorative=False)
    report_full_path = f"{data_folder}/{file_name}_profile.html"
    profile.to_file(report_full_path)


if __name__ == "__main__":
    main()
