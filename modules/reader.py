# ---------------------------------------------------
# reader.py - Reader Class
# ---------------------------------------------------
# A module that contains various methods to fetch
# data from a specific GSheet URL. Methods also
# accept references of controls for it to update the
# UI after the request has completed.
# The way this reader finds data from a spreadsheet
# is determined by the configuration of data rows
# and column placements in the settings menu of the
# application.
# ---------------------------------------------------

import gspread
import csv
import flet as ft
from pathlib import Path


class Reader:

    # Configuration Path
    BASE_PATH = Path(__file__).resolve().parent.parent
    API_KEY = BASE_PATH / "config/apikey.json"

    def __init__(self, *, url):
        """
        Reader is a module that contains various methods for retrieving
        different kinds of data on a Google spreadsheet. This relies on
        the data mapping of rows and columns configuration of the application
        to get the data on a correct location in the sheet.
        """
        self.client = gspread.service_account(
            filename=Reader.API_KEY,
            scopes=gspread.auth.READONLY_SCOPES)
        self.gsheet = self.client.open_by_url(url)

    def fetch_data(self, *, sheet_identifier, completed):
        """
        Fetch all the required data based on the application configuration
        and save it first on the dictionary variable.
        """
        # Get the worksheets with only names starting with identifier
        sheets_names = []
        for ws in self.gsheet.worksheets():
            if ws.title.startswith(sheet_identifier):
                sheets_names.append(ws.title)

        # Get the department name on F2 cell (TODO in configuration)
        first_sheet = self.gsheet.worksheet(sheets_names[0])
        department_name = first_sheet.acell("F2").value

        # Call the completed callback method after all fetching are done.
        params = {"owner": department_name}
        completed(params)


# "https://docs.google.com/spreadsheets/d/1xDew94vfttSPIZ39nA7G7V9kGs_76BI6g-URrsKHP_A/"
def generate_csv_report(url, button: ft.Ref, page: ft.Page):
    gc = gspread.service_account(filename=Reader.API_KEY)

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
        print("getting names...")
        names = sheet.col_values(4)
        print("getting date-times...")
        date_times = sheet.col_values(5)
        print("getting task names...")
        task_names = sheet.col_values(6)
        print("getting num_processed...")
        num_processed = sheet.col_values(8)
        print("getting start_times...")
        start_times = sheet.col_values(9)
        print("getting end_times...")
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
        print("generating csv file...")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_data)

        # Activate again the passed button
        button.current.disabled = False
        page.update()
    