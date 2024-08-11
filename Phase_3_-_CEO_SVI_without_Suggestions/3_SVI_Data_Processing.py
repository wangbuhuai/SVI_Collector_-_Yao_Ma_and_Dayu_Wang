# Created by Dayu Wang (dwang@stchas.edu) on 2024-07-28

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import os
from typing import TextIO


# Input file information
INPUT_FILE_DIRECTORY: str = r"SVI_Raw_Data"


# Output file information
OUTPUT_FILE_DIRECTORY: str = r"SVI_Processed_Data"


def main():
    # Directory to store output files.
    if not os.path.isdir(OUTPUT_FILE_DIRECTORY):
        os.mkdir(OUTPUT_FILE_DIRECTORY)

    for filename in os.listdir(INPUT_FILE_DIRECTORY):
        with open(file=os.path.join(INPUT_FILE_DIRECTORY, filename), mode='r', encoding="utf-8",
                  errors="ignore") as f_in:
            reader: csv.reader = csv.reader(f_in, delimiter=',')
            next(reader, None)

            output_files: list[TextIO] = []
            output_files_created: bool = False

            for row in reader:
                if not output_files_created:
                    for length in range(1, 6):
                        if len(row) > length:
                            output_files.append(open(file=f"{OUTPUT_FILE_DIRECTORY}/{int(row[length])}.csv", mode='w',
                                                     encoding="utf-8", errors="ignore"))
                    output_files_created = True
                    next(reader, None)
                    next(reader, None)
                    continue

                date: str = '-'.join(row[0].strip().split('-') + ["01"])
                for i in range(len(output_files)):
                    output_files[i].write(date + ',')
                    if row[i + 1].find('<') != -1:
                        row[i + 1] = '0'
                    output_files[i].write(f"{int(row[i + 1])}\n")

            for i in range(len(output_files)):
                output_files[i].close()


if __name__ == "__main__":
    main()
