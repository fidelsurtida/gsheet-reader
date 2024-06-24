import gspread
import flet as ft
from pathlib import Path
import csv

BASE_PATH = Path(__file__).resolve().parent.parent


# "https://docs.google.com/spreadsheets/d/1xDew94vfttSPIZ39nA7G7V9kGs_76BI6g-URrsKHP_A/"
def generate_csv_report(url, button: ft.Ref, page: ft.Page):
    apikey = BASE_PATH / "config/apikey.json"
    gc = gspread.service_account(filename=apikey)

    # open an existing spreadsheet using the gsheet url
    sh = gc.open_by_url(url)

    # Get the worksheets with only names starting ing "*-"
    sheets_names = []
    worksheets = sh.worksheets()
    for ws in worksheets:
        if ws.title.startswith("*-"):
            sheets_names.append(ws.title)

    def sanitize_time(strtime):
        if len(strtime.split()) > 1:
            time, ampm = strtime.split()
            hour, minutes = time.split(":")[:2]
            return f"{hour}:{minutes} {ampm}"
        return ""

    # Header and Final Data vars
    headers = ["Name", "Date and Time", "Task Done",
               "Processed", "START", "END"]
    final_data = []

    # Iterate over the sheet names and get the config per employee
    for sheet_name in sheets_names[:1]:
        sheet = sh.worksheet(sheet_name)

        # Get the column config based from the structure of excel
        # Column D(4) - Name
        # Column E(5) - Date and Time
        # Column F(6) - Task Name
        # Column H(8) - Processed
        # Column I(9) - Start Time
        # Column J(10) - End Time
        names = sheet.col_values(4)
        date_times = sheet.col_values(5)
        task_names = sheet.col_values(6)
        num_processed = sheet.col_values(8)
        start_times = sheet.col_values(9)
        end_times = sheet.col_values(10)

        # Format the times to datetime object
        for i, stime in enumerate(start_times):
            start_times[i] = sanitize_time(stime)
        for i, etime in enumerate(end_times):
            end_times[i] = sanitize_time(etime)

        columns = [names, date_times, task_names, num_processed,
                   start_times, end_times]

        for index in range(5, len(names)):
            result = []
            for column in columns:
                try:
                    result.append(column[index])
                except IndexError:
                    result.append("")
            # Don't append the 3rd index which is the num_processed if empty
            if result[3]:
                final_data.append(result)

        # pprint.pprint(final_data, width=300)

    # Create the csv file
    filename = "kpi_records.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_data)

    # Activate again the passed button
    button.current.disabled = False
    page.update()
    