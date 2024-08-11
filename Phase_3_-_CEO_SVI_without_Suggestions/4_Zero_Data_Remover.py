# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-11

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import os
from typing import TextIO


# Input file information
INPUT_FILE_DIRECTORY: str = r"SVI_Processed_Data"


# Output file information
OUTPUT_FILE_DIRECTORY: str = r"SVI_Final_Data"


def main():
    for filename in os.listdir(INPUT_FILE_DIRECTORY):
        input_file: TextIO = open(file=os.path.join(INPUT_FILE_DIRECTORY, filename), mode="r", encoding="utf-8",
                                  errors="ignore")
        csv_reader: csv.reader = csv.reader(input_file, delimiter=',')

        all_zero: bool = True

        for row in csv_reader:
            svi_data: int = int(row[1])
            if svi_data > 0:
                all_zero = False
                break

        input_file.close()

        if all_zero:
            os.remove(os.path.join(INPUT_FILE_DIRECTORY, filename))


if __name__ == "__main__":
    main()
