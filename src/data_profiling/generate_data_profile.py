import os
import sys

import pandas as pd
from pandas_profiling import ProfileReport

from src.log.LogManager import LogManager

my_logger = LogManager(__name__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug(f"Init {__file__}")


def main():
    if len(sys.argv) != 4:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
        sys.exit(1)
    else:
        data_folder = sys.argv[1]
        file_name = sys.argv[2]
        report_name = sys.argv[3]
    input_file_path = f"{data_folder}/{file_name}"
    df = pd.read_csv(input_file_path, sep=",", na_values=[""], index_col=0)
    my_logger.info("data sample :\n" + str(df.head(5)))
    profile = ProfileReport(df, title="pokemon_data_profiling", minimal=False, explorative=False)
    report_full_path = f"{data_folder}/{report_name}"
    try:
        profile.to_file(report_full_path)
        my_logger.info(f"Generate report {report_name} for data {file_name} in {data_folder}")
    except Exception as e:
        my_logger.error(f"Fail to generate report for data {file_name}. \n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
