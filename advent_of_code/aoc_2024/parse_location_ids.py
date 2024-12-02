import argparse
from errno import ENOENT as errno_ENOENT
from os import strerror as os_strerror
import pandas
from pathlib import Path
from sys import argv


def validate_non_empty_existing_path(file_or_dir):
    """
    This function checks whether the provided file or dir exists and is not empty.

    Args:
        file_or_dir (string): Input file or directory

    Raises:
        FileNotFoundError: If input string file_or_dir is neither a file nor a dir.
        OSError: If input is not a dir and file is empty.

    Returns:
        string: Provided input file or directory. If dir, suffix '/' might be added.
    """
    input_path = Path(file_or_dir)
    if not input_path.is_file() and not input_path.is_dir():
        raise FileNotFoundError(errno_ENOENT, os_strerror(errno_ENOENT), file_or_dir)
    elif not input_path.is_dir() and not input_path.stat().st_size:
        raise OSError(f"File {file_or_dir} is empty.")
    elif input_path.is_dir() and file_or_dir[::-1][0] != "/":
        return f"{file_or_dir}/"
    else:
        return file_or_dir


def parse_arguments_and_check(args_in):
    """
    Parses arguments and validates / checks format of input.

    Args:
        args_in (list of strings): Commandline input arguments.

    Returns:
        Namespace: Convert argument strings to objects and assign them as attributes of the namespace.
    """
    parser = argparse.ArgumentParser(description="Parse location IDs as instructed by puzzles of Advent Of Code 2024.")
    parser.add_argument(
        "input_file",
        type=validate_non_empty_existing_path,
        help="Input file with numbers.",
    )
    arguments = parser.parse_args(args_in)
    return arguments


def read_data_and_get_columns_as_list(in_file, sep="\t"):
    """
    Read input data and parse columns as sorted lists.

    Args:
        in_file (str): Path to input .txt file
        sep (str, optional): Separator used in input file. Defaults to '\t'.

    Returns:
        tuple of two lists: columns 'left' and 'right' as sorted lists.
    """
    df_numbers = pandas.read_csv(
        in_file,
        quotechar="'",
        sep=sep,
        names=["left", "right"],
        skip_blank_lines=True,
        dtype=int,
    )
    lst_left_sorted = df_numbers.left.sort_values(ascending=True).tolist()
    lst_right_sorted = df_numbers.right.sort_values(ascending=True).tolist()
    return lst_left_sorted, lst_right_sorted


def get_distance_two_lists(lst_left, lst_right):
    """
    Calculate distance between integers in list (by order)

    Args:
        lst_left (list): list with integers
        lst_right (list): list with integers

    Raises:
        ValueError: When input lists are of unequal lengths.

    Returns:
        int: Sum of retrieved distances of pairwise comparison in list.
    """
    if len(lst_left) != len(lst_right):
        raise ValueError(f"Unequal length of lists, {len(lst_left)} vs {len(lst_right)}")
    distances = [abs(int_left - int_right) for int_left, int_right in zip(sorted(lst_left), sorted(lst_right))]
    return sum(distances)


def main():
    arguments = parse_arguments_and_check(args_in=argv[1:])
    lst_left, lst_right = read_data_and_get_columns_as_list(arguments.input_file)
    summed_distance = get_distance_two_lists(lst_left, lst_right)
    print(f"The summed distance is: {summed_distance}")


if __name__ == "__main__":
    main()
