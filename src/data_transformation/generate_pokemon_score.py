#!/usr/bin/python
import os
import sys
from string import Template

import pandas as pd

from src.log.LogManager import LogManager

my_logger = LogManager(__file__, enable_file_handler=True, log_file_path=os.getenv("LOG_PATH")).get_logger()
my_logger.debug(f"Init {__file__}")


#
def generate_pokemon_stats_col(input_df):
    """
    In this func, we add 4 new columns to indicates the strength of a pokemon

    :param input_df: the input pokemon data source
    :return: the transformed data frame with newly added column
    """
    mod_attack = input_df['attack'] * 1.5
    mod_sp_attack = input_df['special_attack'] * 1.5
    mod_speed = input_df['speed'] * 2

    # add a new column into df called base_stats, which is the sum of attack, defense, hp, etc. It indicates the
    # overall strength of a pokemon
    input_df['base_stats'] = input_df['attack'] + input_df['defense'] + input_df['hp'] + input_df['special_attack'] + \
                             input_df[
                                 'special_defense'] + input_df['speed']
    # add a new column into df called off_stats, It indicates the attack strength
    input_df['off_stats'] = input_df['attack'] + input_df['special_attack'] + input_df[
        'speed']
    # add a new column into df called def_stats. It indicates the def strength
    input_df['def_stats'] = input_df['defense'] + input_df['hp'] + input_df[
        'special_defense']
    # add a new column into df called mod_stats. It indicates the overall strength more accurately. Because after EDA,
    # we found speed has more impact.
    input_df['overall_score'] = (mod_attack + input_df['defense'] + input_df['hp'] + mod_sp_attack + input_df[
        'special_defense'] + mod_speed)
    return input_df


def main():
    if len(sys.argv) != 4:
        my_logger.error(
            'Number of arguments that you give is wrong, please enter the path of the file which you want to analyze.')
    else:
        data_folder = sys.argv[1]
        input_file_name = sys.argv[2]
        output_file_name = sys.argv[3]
        input_path = f"{data_folder}/{input_file_name}"
        input_df = pd.read_csv(input_path)
        output_df = generate_pokemon_stats_col(input_df)
        head = output_df.head(5).to_string()
        output_path = f"{data_folder}/{output_file_name}"
        output_df.to_csv(output_path, index=0)
        result_str = '###################################################\n' \
                     'Four new columns has been added in the data set in path:\n' \
                     '$input_path\n' \
                     '###################################################\n' \
                     'The new data set is in path: $output_path\n' \
                     '###################################################\n' \
                     'The head of the data set is : \n' \
                     '$head\n' \
                     '###################################################\n'
        temp_obj = Template(result_str)
        result = temp_obj.substitute(input_path=input_path,
                                     output_path=output_path, head=head)
        my_logger.info("\n" + result)


if __name__ == "__main__":
    main()
