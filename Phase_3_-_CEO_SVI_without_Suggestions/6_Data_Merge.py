# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-11

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import datetime
import os
import tkinter
from tkinter import filedialog
from typing import TextIO


# Input file information
SVI_DATA_DIRECTORY: str = r"SVI_Processed_Data"
PREPARED_DATA_DIRECTORY: str = r"Output_Files"
PREPARED_DATA_FILENAME: str = r"5_Data_to_be_Merged.csv"


# Output file information
OUTPUT_FILE_DIRECTORY: str = r"Output_Files"
OUTPUT_FILENAME: str = r"6_CEO_SVI_without_Suggestions.csv"
OUTPUT_COLUMNS: list[str] = [
    "P_DATA_DATE",
    "CEO_SVI",
    "P_DIRECTOR_NAME",
    "P_COMPANY_NAME",
    "P_BRD_POSITION",
    "P_ROLE_NAME",
    "P_NED",
    "P_DIRECTOR_ID",
    "P_COMPANY_ID",
    "P_DATE_START_ROLE",
    "P_DATE_END_ROLE",
    "P_HO_COUNTRY_NAME",
    "P_SECTOR",
    "P_ORG_TYPE",
    "P_ISIN",
    "INDICATOR_ON_JOB"
]


def in_between(d: str, d_1: str, d_2: str) -> str:
    """ Tests whether a date is between two dates.
        :param d: the date string to test
        :param d_1: the early date string to test
        :param d_2: the late date string to test
        :return: testing result
    """
    d = datetime.datetime.strptime(d, "%Y-%m-%d")
    d_1 = datetime.datetime.strptime(d_1, "%m/%d/%Y")
    d_2 = datetime.datetime.strptime(d_2, "%m/%d/%Y")
    return "Yes" if d_1 <= d <= d_2 else "No"


def main():
    # Open the prepared data.
    if not os.path.isfile(os.path.join(PREPARED_DATA_DIRECTORY, PREPARED_DATA_FILENAME)):
        print("[Error] Missing the prepared data file")
        return
    prepared_data_file: TextIO = open(file=os.path.join(PREPARED_DATA_DIRECTORY, PREPARED_DATA_FILENAME), mode='r',
                                      encoding="utf-8", errors="ignore")
    csv_reader_1: csv.reader = csv.reader(prepared_data_file, delimiter=',')
    next(csv_reader_1, None)

    # Open the output file.
    output_file: TextIO = open(file=os.path.join(OUTPUT_FILE_DIRECTORY, OUTPUT_FILENAME), mode='w', encoding="utf-8",
                               errors="ignore")
    output_file.write(f"{','.join(OUTPUT_COLUMNS)}\n")

    # Data merge
    for row_1 in csv_reader_1:
        p_director_name: str = row_1[0].strip()
        p_company_name: str = row_1[1].strip()
        p_brd_position: str = row_1[2].strip()
        p_role_name: str = row_1[3].strip()
        p_ned: str = row_1[4].strip()
        p_director_id: int = int(row_1[5])
        p_company_id: int = int(row_1[6])
        p_date_start_role: str = row_1[7].strip()
        p_date_end_role: str = row_1[8].strip()
        p_ho_country_name: str = row_1[9].strip()
        p_sector: str = row_1[10].strip()
        p_org_type: str = row_1[11].strip()
        p_isin: str = row_1[12].strip()

        with open(file=os.path.join(SVI_DATA_DIRECTORY, f"{p_director_id}.csv"), mode='r', encoding="utf-8",
                  errors='ignore') as svi_file:
            csv_reader_2: csv.reader = csv.reader(svi_file, delimiter=',')
            for row_2 in csv_reader_2:
                data_date: str = row_2[0].strip()
                svi: int = int(row_2[1])

                output_file.write(','.join([
                    f"{data_date}",
                    f"{svi}",
                    f"{p_director_name}",
                    f"{p_company_name}",
                    f"{p_brd_position}",
                    f"{p_role_name}",
                    f"{p_ned}",
                    f"{p_director_id}",
                    f"{p_company_id}",
                    f"{p_date_start_role}",
                    f"{p_date_end_role}",
                    f"{p_ho_country_name}",
                    f"{p_sector}",
                    f"{p_org_type}",
                    f"{p_isin}",
                    f"{in_between(data_date, p_date_start_role, p_date_end_role)}"
                ]))
                output_file.write('\n')

    prepared_data_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
