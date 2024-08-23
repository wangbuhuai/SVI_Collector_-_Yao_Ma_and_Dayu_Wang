# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-23

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-23


import csv
from typing import TextIO


# Input CSV file
INPUT_FILE: str = r"C:/Users/wangb/OneDrive/Wang_Buhuai/Dayu_Wang/Study_and_Research/[Research]_Superstar_CEOs_and_Sh" \
                  r"ort_Selling/Final_Output_Files/2024-08-23_-_Firm_SVI_Final_Output_File_with_PERMNO.csv"


def main():
    input_file: TextIO = open(
        file=INPUT_FILE,
        mode='r',
        encoding="utf-8",
        errors="ignore",
    )
    csv_reader: csv.reader = csv.reader(input_file, delimiter=',')

    row_count: int = 0
    for _ in csv_reader:
        row_count += 1

    input_file.close()
    print(row_count)


if __name__ == "__main__":
    main()
