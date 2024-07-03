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
import time
from pathlib import Path
from gspread.utils import Dimension, DateTimeOption


# "https://docs.google.com/spreadsheets/d/1xDew94vfttSPIZ39nA7G7V9kGs_76BI6g-URrsKHP_A/"
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
        self.url = url
        self.client = gspread.service_account(
            filename=Reader.API_KEY,
            scopes=gspread.auth.READONLY_SCOPES)

    def fetch_data(self, *, sheet_identifier, progress, completed):
        """
        Fetch all the required data based on the application configuration
        and save it first on the dictionary variable.
        """
        # Get the gsheet from the url
        progress("Opening Sheet from URL...", 0)
        gsheet = self.client.open_by_url(self.url)

        # Get the worksheets with only names starting with identifier
        sheets_names = []
        progress("Filtering Worksheet Names...", 0.05)
        for ws in gsheet.worksheets():
            if ws.title.startswith(sheet_identifier):
                sheets_names.append(ws.title)

        # Get the department name on F2 cell (Should be in configuration)
        progress("Fetching Sheet Department...", 0.1)
        first_sheet = gsheet.worksheet(sheets_names[0])
        department_name = first_sheet.acell("F2").value

        # Iterate over the sheet names and get the data columns
        # The configuration of columns should be on the app configuration
        final_data = []
        cur_prog = 0.1
        per_job_prog = (0.8 / len(sheets_names))

        for sheet_name in sheets_names:
            sheet = gsheet.worksheet(sheet_name)
            sheet_owner = sheet.acell("F1").value

            # Get the column config based from the structure of Excel
            # Column E - Date and Time
            # Column F - Task Name
            # Column H - Processed
            # Column I - Start Time
            # Column J - End Time
            cur_prog = cur_prog + per_job_prog
            progress(f"Downloading [{sheet_owner} Sheet Data]...", cur_prog)
            data = sheet.get(range_name="E:J",
                             major_dimension=Dimension.cols)
            time.sleep(3)

            # Select only the required columns and assign to each variable
            # Also disregard the first 5 initial row of it's column
            date_times = data[0][5:]
            task_names = data[1][5:]
            num_processed = data[3][5:]
            start_times = data[4][5:]
            end_times = data[5][5:]

            # Format the times to datetime object
            for i, stime in enumerate(start_times):
                start_times[i] = self._sanitize_time(stime)
            for i, etime in enumerate(end_times):
                end_times[i] = self._sanitize_time(etime)

            columns = [date_times, task_names, num_processed,
                       start_times, end_times]

            for index in range(5, len(date_times)):
                result = [department_name, sheet_owner]
                for column in columns:
                    try:
                        result.append(column[index])
                    except IndexError:
                        result.append("")
                # Don't append the 3rd index which is the num_processed if empty
                if result[3]:
                    final_data.append(result)

        # Call the completed callback method after all fetching are done.
        args = {"owner": department_name, "final_data": final_data}
        progress(f"{department_name} - COMPLETED", 1)
        completed(args)

    @staticmethod
    def _sanitize_time(strtime):
        """ Helper method to correct the format of datetime string. """
        if len(strtime.split()) > 1:
            timestr, ampm = strtime.split()
            hour, minutes = timestr.split(":")[:2]
            return f"{hour}:{minutes} {ampm}"
        return ""

    @staticmethod
    def generate_csv_report(data):
        """
        Standalone method to generate a csv report based
        on the passed DATA library.
        """
        # Header column names for the CSV
        headers = ["Department", "Name", "Date and Time", "Task Done",
                   "Processed", "START", "END"]

        # Create the csv file
        filename = "kpi_records.csv"
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            for rows in data.values():
                csvwriter.writerows(rows)
    