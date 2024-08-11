# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-11

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import datetime
import os
import re
import tkinter
from tkinter import filedialog
from typing import TextIO


# Requirements of the CEO's name and role
REQUIREMENTS: dict[str, str | list[str]] = {
    "NAME_EXCLUDE": r"[^A-Za-z\-' ]",
    "ROLE": r'(ceo)|(chief executive officer)',
    "ROLE_EXCLUDE": r'((((regional)|(division)|(vice)|(deputy)|(associate)|(assistant)) .*?/?ceo)|(ceo - insurance))',
    "SUFFIX_IGNORED": ["Jr", "III", "Sr", "II", "IV", 'V', "lll", "ll"],
    "PREFIX_IGNORED": ["Doctor", "Professor", "Major", "Colonel", "Captain", "Ambassador", "General", "Sir", "Senator",
                       "Admiral", "Governor", "Sister", "Vice", "Lieutenant", "Commander", "Dean", "Bishop", "Brother",
                       "Father", "Jr"]
}


OUTPUT_COLUMNS: list[str] = [
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
]

# Input file information
SVI_DATA_DIRECTORY: str = r"SVI_Processed_Data"

# Output file information
OUTPUT_FILE_DIRECTORY: str = r"Output_Files"
OUTPUT_FILENAME: str = r"5_Data_to_be_Merged.csv"


def reformat_name(name: str) -> str | None:
    """ Reformats a CEO name for queries on Google Trends.
        :param name: the CEO name to reformat
        :return: the reformatted CEO name, or {None} if the CEO name does not meet out standards
    """

    # A valid name should contain only English letters, dash, apostrophe, and space.
    if re.search(REQUIREMENTS["NAME_EXCLUDE"], name, re.IGNORECASE) is not None:
        return None

    tokens: list[str] = name.split()

    # Remove the ignored prefix and suffix from the name.
    flag: bool = False
    while len(tokens) > 2:
        if len(tokens) > 2 and tokens[-1].lower() in [s.lower() for s in REQUIREMENTS["SUFFIX_IGNORED"]]:
            tokens.pop(-1)
            flag = True
        if len(tokens) > 2 and tokens[0].lower() in [t.lower() for t in REQUIREMENTS["PREFIX_IGNORED"]]:
            tokens.pop(0)
            flag = True
        if not flag:
            break
        else:
            flag = False

    return ' '.join(tokens)


def valid_role_name(role_name: str) -> bool:
    """ Tests whether a rolename is valid.
        :param role_name: the rolename to test
        :return: {True} if the rolename is valid; {False} otherwise
    """
    return re.search(REQUIREMENTS["ROLE"], role_name, re.IGNORECASE) is not None \
        and re.search(REQUIREMENTS["ROLE_EXCLUDE"], role_name, re.IGNORECASE) is None


def main():
    # Get all the director IDs with SVI.
    director_ids: set[int] = set()
    for filename in os.listdir(SVI_DATA_DIRECTORY):
        director_id: int = int(filename.split('.')[0])
        director_ids.add(director_id)

    # Open the raw database file (.csv only).
    root: tkinter.Tk = tkinter.Tk()
    root.withdraw()
    pathname_raw_database: str = filedialog.askopenfilename(
        title="Open the Raw Database File",
        initialdir='/',
        filetypes=[("CSV File", "*.csv")]
    )
    if not os.path.isfile(pathname_raw_database):
        print("[Error] Pathname of the raw database file is invalid.")
        return
    raw_database_file: TextIO = open(file=pathname_raw_database, mode='r', encoding="utf-8", errors="ignore")
    raw_database_file_reader: csv.reader = csv.reader(raw_database_file, delimiter=',')
    next(raw_database_file_reader, None)

    # Create the output file.
    if not os.path.isdir(OUTPUT_FILE_DIRECTORY):
        os.mkdir(OUTPUT_FILE_DIRECTORY)
    output_file: TextIO = open(file=os.path.join(OUTPUT_FILE_DIRECTORY, OUTPUT_FILENAME), mode='w', encoding="utf-8",
                               errors="ignore")
    output_file.write(f"{','.join(OUTPUT_COLUMNS)}\n")
    output_file.flush()

    count: int = 1
    for row in raw_database_file_reader:
        # Tests whether the director ID has SVI data.
        p_director_id: int = int(row[6])
        if p_director_id not in director_ids:
            continue

        # Tests whether the role start date and role end date are valid.
        p_date_start_role: str = row[8].replace(',', ' ').strip()
        p_date_end_role: str = row[9].replace(',', ' ').strip()
        if p_date_start_role.lower() == 'n' or p_date_end_role.lower() == 'n':
            continue
        if p_date_end_role.lower() == 'c':
            p_date_end_role = datetime.datetime.today().strftime("%m/%d/%Y")

        # Tests whether the role name is valid.
        p_role_name: str = row[3].replace(',', ' ').strip()
        if not valid_role_name(p_role_name):
            continue

        # Tests whether the director name is valid.
        p_director_name: str = row[0].replace(',', ' ').strip()
        p_query_name: str | None = reformat_name(p_director_name)
        if p_query_name is None:
            continue

        # Write the valid data to the output file.
        p_company_name: str = row[1].replace(',', ' ').strip()
        p_brd_position: str = row[2].replace(',', ' ').strip()
        p_ned: str = row[5].replace(',', ' ').strip()
        p_company_id: int = int(row[7])
        p_ho_country_name: str = row[10].replace(',', ' ').strip()
        p_sector: str = row[11].replace(',', ' ').strip()
        p_org_type: str = row[12].replace(',', ' ').strip()
        p_isin: str = row[13].replace(',', ' ').strip()

        output_file.write(','.join([
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
        ]) + '\n')
        print(f"Number of records: {count}")
        count += 1

    raw_database_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
