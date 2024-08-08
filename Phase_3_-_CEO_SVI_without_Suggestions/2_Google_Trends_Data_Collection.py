# Created by Dayu Wang (dwang@stchas.edu) on 2024-08-07

# Last updated by Dayu Wang (dwang@stchas.edu) on 2024-08-07


import csv
import os
import serpapi
import shutil
from typing import TextIO


API_KEY_FILE_PATH = os.path.join(r"C:\Users\wangb\OneDrive\Wang_Buhuai\Dayu_Wang\Study_and_Research\["
                                 r"Research]_Superstar_CEOs_and_Short_Selling\API_Keys", "SerpAPI_Key.txt")


def main():
    # Let the user provide a plain text file storing his/her SerpAPI key.
    pathname_api_key: str = API_KEY_FILE_PATH
    if not os.path.isfile(pathname_api_key):
        print("[Error] You must provide a valid API key for SerpAPI.")
        return
    file_api_key: TextIO = open(file=pathname_api_key, mode='r', encoding="utf-8", errors="ignore")
    api_key: str = file_api_key.read().strip()
    file_api_key.close()

    # Open the input file.
    if not os.path.isdir(r'Output_Files'):
        print("[Error] Folder \"Output_Files\" does not exist.")
        return
    input_filename: str | None = None
    for filename in os.listdir(r'Output_Files'):
        if filename.startswith('1_'):
            input_filename = filename
            break
    if input_filename is None:
        print("[Error] Required input file does not exist.")
        return
    input_file: TextIO = open(file=os.path.join(r'Output_Files', input_filename), mode='r', encoding="utf-8",
                              errors="ignore")
    input_file_reader: csv.reader = csv.reader(input_file, delimiter=',')
    next(input_file_reader, None)

    # A set to store the director IDs that have already been processed.
    director_ids: set[int] = set()

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
        # Get the director ID.
        p_director_id: int = int(row[7])

        # Find the next row to process.
        if current < row_number:
            director_ids.add(p_director_id)
            current += 1
            continue

        # Test whether the current CEO has already been processed.
        if p_director_id in director_ids or p_director_id in current_ceos.keys():
            current += 1
            continue

        # Add the current CEO to the lists storing the current 5 CEOs.
        p_query_name: str = row[1].strip()
        current_ceos[p_director_id] = p_query_name

        # Collect the data on Google Trends through SerpAPI when 5 CEOs are accumulated.
        if len(current_ceos) == 5:
            params['q'] = ','.join([current_ceos[k] for k in sorted(current_ceos.keys())])

            search_result: serpapi.GoogleSearch = serpapi.GoogleSearch(params)

            csv_result = search_result.get_dict()
            csv_result[1] = f",{','.join(str(i) for i in sorted(current_ceos.keys()))}\n"

            with open(file=os.path.join(r"Output_Files", f"{sorted(current_ceos.keys())[0]:07d}-"
                                                         f"{sorted(current_ceos.keys())[-1]:07d}.csv"),
                      mode='w',
                      encoding="utf-8",
                      errors="ignore") as f_out:
                f_out.write('\n'.join(csv_result))

            print(f"[Success] {sorted(current_ceos.keys())[0]:07d}-{sorted(current_ceos.keys())[-1]:07d}")
            params.pop('q')
            director_ids.update(current_ceos.keys())
            current_ceos.clear()

        current += 1

    if len(current_ceos) > 0:
        params['q'] = ','.join([current_ceos[k] for k in sorted(current_ceos.keys())])

        try:
            search_result: serpapi.SerpResults = serpapi.search(params)
        except:
            temp_file: TextIO = open(file=os.path.join(r"Temp", r"next_row_to_process.txt"), mode='w',
                                     encoding="utf-8", errors="ignore")
            temp_file.write(f"{current}")
            temp_file.close()
            print(f"[Error] Search Failed -> Row Number: {current}")
            return

        csv_result: list[str] = search_result["csv"]
        csv_result[1] = f",{','.join(str(i) for i in sorted(current_ceos.keys()))}\n"

        with open(file=os.path.join(r"Output_Files", f"{sorted(current_ceos.keys())[0]:07d}-"
                                                     f"{sorted(current_ceos.keys())[-1]:07d}.csv"),
                  mode='w',
                  encoding="utf-8",
                  errors="ignore") as f_out:
            f_out.write('\n'.join(csv_result))

        print(f"[Success] {sorted(current_ceos.keys())[0]:07d}-{sorted(current_ceos.keys())[-1]:07d}")

    input_file.close()

    # Clean up.
    if os.path.isfile(os.path.join(r"Output_Files", r"next_row_to_process.txt")):
        os.remove(os.path.join(r"Output_Files", r"next_row_to_process.txt"))
    if os.path.isdir(r"Temp"):
        shutil.rmtree(r"Temp")


if __name__ == "__main__":
    main()
