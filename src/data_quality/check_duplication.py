#!/usr/bin/python

import os
import sys
from string import Template

import pandas as pd

from src.log.LogManager import LogManager
from src.utile import get_local_input_file_path

my_logger = LogManager(__file__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug(f"Init {__file__}")


def get_duplicated_rows(data_frame):
    duplicated_element = data_frame.duplicated()
    return data_frame[duplicated_element]


def get_duplicated_row_numbers(duplicate_row_df):
    return len(duplicate_row_df.index)


def main():
    if len(sys.argv) != 3:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
    else:
        remote_file_path = sys.argv[1]
        data_folder = sys.argv[2]
        input_file_path, file_name = get_local_input_file_path(remote_file_path, data_folder)
        df = pd.read_csv(input_file_path, index_col=0)
        result_str = '###################################################\n' \
                     'The total number of duplicated rows is $duplicated_row_number\n' \
                     '###################################################\n' \
                     'The duplicated rows are: \n' \
                     '$duplicated_rows\n' \
                     '###################################################\n'
        temp_obj = Template(result_str)
        duplicated_rows = get_duplicated_rows(df)
        duplicated_row_numbers = get_duplicated_row_numbers(duplicated_rows)
        result = temp_obj.substitute(duplicated_row_number=duplicated_row_numbers,
                                     duplicated_rows=duplicated_rows.to_string())
        my_logger.info("\n"+result)


if __name__ == "__main__":
    main()
