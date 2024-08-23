# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-22

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-23


import csv
from typing import TextIO


# Pathnames of input files
RAW_DATABASE: str = r"C:/Users/wangb/OneDrive/Wang_Buhuai/Dayu_Wang/Study_and_Research/[Research]_Superstar_CEOs_and_" \
                    r"Short_Selling/Python_Project_Databases/raw_firm_database.csv"
OLD_OUTPUT_FILE: str = r"C:\Users\wangb\OneDrive\Wang_Buhuai\Dayu_Wang\Study_and_Research\[Research]_Superstar_CEOs_a" \
                       r"nd_Short_Selling\Final_Output_Files\2024-07-29_-_Firm_SVI_Final_Output_File.csv"


# Pathname of output file
OUTPUT_FILE: str = r"C:/Users/wangb/OneDrive/Wang_Buhuai/Dayu_Wang/Study_and_Research/[Research]_Superstar_CEOs_and_S" \
                   r"hort_Selling/Final_Output_Files/2024-08-23_-_Firm_SVI_Final_Output_File_with_PERMNO.csv"


# Columns in output file
COLUMNS: list[str] = [
    "PERMNO",
    "F_DATADATE",
    "F_SVI",
    "COMNAM",
    "TICKER"
]


def main():
    # Generate "TICKER-PERMNO" relationship.
    tickers: dict[str, int] = dict()

    with open(file=RAW_DATABASE, mode='r', encoding="utf-8", errors="ignore") as input_file_1:
        csv_reader_1: csv.reader = csv.reader(input_file_1, delimiter=',')
        next(csv_reader_1, None)

        for row_1 in csv_reader_1:
            ticker: str = row_1[5].upper().strip()

            # Ignore the ticker if it is already in the map.
            if ticker in tickers.keys():
                continue

            permno: int = int(row_1[0])
            tickers[ticker] = permno

    # Initialize the output file.
    output_file: TextIO = open(
        file=OUTPUT_FILE,
        mode='w',
        encoding="utf-8",
        errors="ignore"
    )
    output_file.write(','.join(COLUMNS) + '\n')

    # Update the old output file.
    with open(file=OLD_OUTPUT_FILE, mode='r', encoding="utf-8", errors="ignore") as input_file_2:
        csv_reader_2: csv.reader = csv.reader(input_file_2, delimiter=',')
        next(csv_reader_2, None)

        for row_2 in csv_reader_2:
            f_datadate: str = row_2[1].strip()
            f_svi: int = int(row_2[2])
            conam: str = row_2[3].strip()
            ticker: str = row_2[4].upper().strip()

            permno: int = tickers[ticker]

            output_file.write(','.join([
                f"{permno}",
                f"{f_datadate}",
                f"{f_svi}",
                f"{conam}",
                f"{ticker}"
            ]) + '\n')

    output_file.close()


if __name__ == "__main__":
    main()
