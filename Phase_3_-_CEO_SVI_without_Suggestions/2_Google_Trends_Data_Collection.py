# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-07

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-11


import csv
import datetime
import os
import serpapi
import shutil
import time
import tkinter
from tkinter import filedialog
from typing import TextIO


# Input file information
INPUT_FILE_DIRECTORY: str = r"Output_Files"
INPUT_FILE_NAME: str = r"1_Prepared_Search_Data.csv"

# Output file information
OUTPUT_FILE_DIRECTORY: str = r"SVI_Raw_Data"


def main():
    # Let the user provide a plain text file storing his/her SerpAPI key.
    root: tkinter.Tk = tkinter.Tk()
    root.withdraw()
    pathname_api_key: str = filedialog.askopenfilename(
        title="Select the file containing the API key",
        initialdir='/',
        filetypes=[("Plain Text File", "*.txt")]
    )
    if not os.path.isfile(pathname_api_key):
        print("[Error] You must provide a valid API key for SerpAPI.")
        return
    file_api_key: TextIO = open(file=pathname_api_key, mode='r', encoding="utf-8", errors="ignore")
    api_key: str = file_api_key.read().strip()
    file_api_key.close()

    # Open the input file.
    if not os.path.isdir(INPUT_FILE_DIRECTORY):
        print("[Error] Input file directory does not exist.")
        return
    if not os.path.isfile(os.path.join(INPUT_FILE_DIRECTORY, INPUT_FILE_NAME)):
        print("[Error] Required input file does not exist.")
        return
    input_file: TextIO = open(file=os.path.join(INPUT_FILE_DIRECTORY, INPUT_FILE_NAME), mode='r', encoding="utf-8",
                              errors="ignore")
    input_file_reader: csv.reader = csv.reader(input_file, delimiter=',')
    next(input_file_reader, None)

    # Get the next row number to process from the temporary file.
    if not os.path.isdir(r'Temp'):
        os.mkdir(r'Temp')
    if not os.path.isfile(os.path.join(r'Temp', r'next_row_to_process.txt')):
        temp_file: TextIO = open(file=os.path.join(r'Temp', r'next_row_to_process.txt'), mode='w', encoding="utf-8",
                                 errors="ignore")
        temp_file.write('2')
        temp_file.close()
    temp_file: TextIO = open(file=os.path.join(r'Temp', r'next_row_to_process.txt'), mode='r', encoding="utf-8",
                             errors="ignore")
    row_number: int = int(temp_file.read())  # Next row number to process in the raw database csv file
    temp_file.close()

    # Current 5 CEOs
    current_ceos: dict[int, str] = dict()

    # SVI search parameters
    params: dict[str, str] = {
        "engine": "google_trends",
        "data_type": "TIMESERIES",
        "geo": "US",
        "tz": "360",
        "date": "all",
        "csv": "true",
        "api_key": api_key
    }

    # Process the input file.
    current: int = 2
    for row in input_file_reader:
        # Find the next row to process.
        if current < row_number:
            current += 1
            continue

        # Add the current CEO to the lists storing the current 5 CEOs.
        p_query_name: str = row[0].strip()
        p_director_id: int = int(row[1])
        current_ceos[p_director_id] = p_query_name

        # Collect the data on Google Trends through SerpAPI when 5 CEOs are accumulated.
        if len(current_ceos) == 5:
            params['q'] = ','.join([current_ceos[k] for k in sorted(current_ceos.keys())])

            csv_result: list[str] | None = None

            # Stop running the program is consecutive 10 errors are accumulated on the same piece of data.
            error_count: int = 0

            while True:
                try:
                    search_result: serpapi.GoogleSearch = serpapi.GoogleSearch(params)
                    csv_result = search_result.get_dict()["csv"]
                    error_count = 0
                    break
                except KeyError:
                    error_count += 1
                    print(f"[Key Error] -> {sorted(current_ceos.keys())} -> "
                          f"{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')}")
                except:
                    error_count += 1
                    print(f"[Other Error] -> {sorted(current_ceos.keys())} -> "
                          f"{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')}")
                finally:
                    if error_count >= 10:
                        print(f"[Consecutive 10 Errors] -> {sorted(current_ceos.keys())} -> "
                              f"{datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')}")
                        break
                    time.sleep(10)

            # Process the collected data.
            csv_result[1] = f",{','.join(str(i) for i in sorted(current_ceos.keys()))}\n"
            if not os.path.isdir(OUTPUT_FILE_DIRECTORY):
                os.mkdir(OUTPUT_FILE_DIRECTORY)
            with open(file=os.path.join(OUTPUT_FILE_DIRECTORY, f"{sorted(current_ceos.keys())[0]}-"
                                                               f"{sorted(current_ceos.keys())[-1]}.csv"),
                      mode='w',
                      encoding="utf-8",
                      errors="ignore") as f_out:
                f_out.write('\n'.join(csv_result))

            print(f"[Success] {sorted(current_ceos.keys())[0]}-{sorted(current_ceos.keys())[-1]}")
            params.pop('q')
            current_ceos.clear()

        current += 1
        temp_file: TextIO = open(file=os.path.join(r'Temp', r'next_row_to_process.txt'), mode='w', encoding="utf-8",
                                 errors="ignore")
        temp_file.write(f"{current}")
        temp_file.close()

    if len(current_ceos) > 0:
        params['q'] = ','.join([current_ceos[k] for k in sorted(current_ceos.keys())])

        search_result: serpapi.GoogleSearch = serpapi.GoogleSearch(params)
        csv_result = search_result.get_dict()["csv"]

        # Process the collected data.
        csv_result[1] = f",{','.join(str(i) for i in sorted(current_ceos.keys()))}\n"

        if not os.path.isdir(OUTPUT_FILE_DIRECTORY):
            os.mkdir(OUTPUT_FILE_DIRECTORY)
        with open(file=os.path.join(OUTPUT_FILE_DIRECTORY, f"{sorted(current_ceos.keys())[0]}-"
                                                           f"{sorted(current_ceos.keys())[-1]}.csv"),
                  mode='w',
                  encoding="utf-8",
                  errors="ignore") as f_out:
            f_out.write('\n'.join(csv_result))

        print(f"[Success] {sorted(current_ceos.keys())[0]}-{sorted(current_ceos.keys())[-1]}")

    input_file.close()

    # Clean up.
    if os.path.isdir(r"Temp"):
        shutil.rmtree(r"Temp")


if __name__ == "__main__":
    main()
