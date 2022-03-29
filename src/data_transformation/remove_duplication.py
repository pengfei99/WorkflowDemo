#!/usr/bin/python
import os
import sys
from string import Template

import pandas as pd

from src.log.LogManager import LogManager
from src.utile import get_local_input_file_path

my_logger = LogManager(__file__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug(f"Init {__file__}")


def remove_duplicated_rows(input_df):
    duplicate_row_df = input_df[input_df.duplicated()]
    duplicated_row_number = len(duplicate_row_df.index)
    if duplicated_row_number > 0:
        df_result = input_df.drop_duplicates()
    else:
        df_result = input_df
    return duplicated_row_number, df_result


def main():
    if len(sys.argv) != 3:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
        exit(1)
    else:

        remote_file_path = sys.argv[1]
        data_folder = sys.argv[2]
        input_file_path, file_name = get_local_input_file_path(remote_file_path, data_folder)
        input_df = pd.read_csv(input_file_path)
        result_str = '###################################################\n' \
                     '$duplicated_row_number duplicated lines has been removed from the data set in path:\n' \
                     '$input_path\n' \
                     '###################################################\n' \
                     'The cleaned data set is in path: $output_path\n' \
                     '###################################################\n'
        temp_obj = Template(result_str)
        duplicated_row_number, output_df = remove_duplicated_rows(input_df)
        output_path = f"{data_folder}/pokemon-dedup.csv"
        output_df.to_csv(output_path, index=0)
        result = temp_obj.substitute(duplicated_row_number=duplicated_row_number, input_path=input_file_path,
                                     output_path=output_path)
        my_logger.info("\n" + result)


if __name__ == "__main__":
    main()
