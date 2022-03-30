#!/usr/bin/python
import os
import sys
from string import Template

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from src.log.LogManager import LogManager

my_logger = LogManager(__file__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug(f"Init {__file__}")


def rename_column_names(input_df, column_rename_list):
    rename_col_size = len(column_rename_list)
    df_result = input_df.rename(index=str, columns=column_rename_list)
    return rename_col_size, df_result


def main():
    if len(sys.argv) != 5:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
    else:
        data_folder = sys.argv[1]
        input_file_name = sys.argv[2]
        output_file_name = sys.argv[3]
        output_file_format = sys.argv[4]
        input_path = f"{data_folder}/{input_file_name}"
        input_df = pd.read_csv(input_path)
        result_str = '###################################################\n' \
                     '$rename_col_size columns has been renamed from the data set in path:\n' \
                     '$input_path\n' \
                     '###################################################\n' \
                     'The new data set is in path: $output_path\n' \
                     '###################################################\n' \
                     'The head of the data set is : \n' \
                     '$head\n' \
                     '###################################################\n'
        temp_obj = Template(result_str)
        column_rename_list = {"#": "index",
                              "Name": "name",
                              "Type 1": "type_1",
                              "Type 2": "type_2",
                              "Total": "total",
                              "HP": "hp",
                              "Attack": "attack",
                              'Defense': "defense",
                              "SP. Atk": "special_attack",
                              "SP. Def": "special_defense",
                              'Speed': "speed",
                              'Generation': "generation",
                              'Legendary': "legendary"
                              }

        rename_col_size, output_df = rename_column_names(input_df, column_rename_list)
        output_path = f"{data_folder}/{output_file_name}"
        if output_file_format == "parquet":
            table = pa.Table.from_pandas(df=output_df)
            pq.write_table(table, output_path)
        elif output_file_format == "csv":
            output_df.to_csv(output_path, index=0)
        else:
            my_logger.error("unsupported file format")
            sys.exit(1)
        head = output_df.head(5).to_string()
        result = temp_obj.substitute(rename_col_size=rename_col_size, input_path=input_path,
                                     output_path=output_path, head=head)
        my_logger.info("\n" + result)


if __name__ == "__main__":
    main()
