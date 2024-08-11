# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-11

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import os
from typing import TextIO


# Input file information
INPUT_FILE_DIRECTORY: str = r"../Output_Files"
INPUT_FILENAME: str = r"6_CEO_SVI_without_Suggestions.csv"


def main():
    if not os.path.isfile(os.path.join(INPUT_FILE_DIRECTORY, INPUT_FILENAME)):
        print("[Error] Missing the input file")
        return
    input_file: TextIO = open(file=os.path.join(INPUT_FILE_DIRECTORY, INPUT_FILENAME), mode='r', encoding="utf-8",
                              errors="ignore")
    csv_reader: csv.reader = csv.reader(input_file, delimiter=',')
    next(csv_reader, None)

    count: int = 0
    for row in csv_reader:
        count += 1
    print(count)

    input_file.close()


if __name__ == "__main__":
    main()
