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
import json
import time
import os
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from gspread.utils import Dimension, DateTimeOption, ValueRenderOption
from controls.settingsmanager import SettingsManager

# WORKING SHEETS URL
# "https://docs.google.com/spreadsheets/d/1xDew94vfttSPIZ39nA7G7V9kGs_76BI6g-URrsKHP_A/"
# "https://docs.google.com/spreadsheets/d/126fd7j8aLGGegctt45V4r10qE6EJ2LR8XffcZU7NcMc/"
# "https://docs.google.com/spreadsheets/d/1nur0MNyZ9Zyx2nYtAN_9Xagiqt6bdBIDbLG-_yRmXok/"
# "https://docs.google.com/spreadsheets/d/1tN14S_VZionNZ-Qky-qJffK8zxVjKhZpt6JS0sqfEb8/"
# WITH ERROR SHEETS URL
# "https://docs.google.com/spreadsheets/d/1Rajey786y2rOpDzsclhnreexd4AMUdOjA6m68343S9Y/"
# "https://docs.google.com/spreadsheets/d/1i2HylLwYeRIem-9pL8MqpW6S7W2MwHpNf-FYUBVgZNY/"

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
        self.timestamp = None

        # If API_KEY is not found then specify the client to None
        # Return the FileNotFound Error on call of fetch_data.
        try:
            self.client = gspread.service_account(
                filename=Reader.API_KEY,
                scopes=gspread.auth.READONLY_SCOPES)
        except FileNotFoundError:
            self.client = None

    def fetch_data(self, *, sheet_identifier, progress, completed):
        """
        Fetch all the required data based on the application configuration
        and save it first on the dictionary variable.
        """
        # Check first if client is valid
        if not self.client:
            return gspread.exceptions.APIError

        # Get the gsheet from the url
        progress(left="Opening Sheet from URL...", value=0)
        try:
            gsheet = self.client.open_by_url(self.url)
        except (gspread.exceptions.SpreadsheetNotFound,
                gspread.exceptions.NoValidUrlKeyFound):
            return gspread.exceptions.SpreadsheetNotFound
        except PermissionError:
            return gspread.exceptions.GSpreadException

        # Get the settings saved configuration data
        settings = SettingsManager.get_settings_data()
        date_col = settings["required"][0]
        start_col = settings["required"][1]
        end_col = settings["required"][2]
        task_col = settings["other_columns"][0]
        proccessed_col = settings["other_columns"][1]
        sorted_cols = [start_col[0], end_col[0],
                       task_col[0], proccessed_col[0]]
        sorted_cols.sort()
        # Create a list of sorted columns to use later in merging data
        min_col, max_col = sorted_cols[0], sorted_cols[-1]
        col_range = [chr(i) for i in range(ord(min_col), ord(max_col) + 1)]

        # Get the worksheets with only names starting with identifier
        sheets_names = []
        progress(left="Filtering Worksheet Names...", value=0.05)
        for ws in gsheet.worksheets():
            if ws.title.startswith(sheet_identifier):
                sheets_names.append(ws.title)

        # Get the department name on F2 cell (Should be in configuration)
        progress(left="Fetching Sheet Ownership...", value=0.1)
        sheet_source = gsheet.worksheet("Instructions")
        department_name = sheet_source.acell("H2").value
        month_sheet, month_sheet_numeric = "", None

        # Iterate over the sheet names and get the data columns
        # The configuration of columns should be on the app configuration
        final_data = []
        cur_prog = 0.1
        per_job_prog = (0.8 / len(sheets_names))

        for sheet_name in sheets_names:
            # Get the sheet and the ownership names
            sheet = gsheet.worksheet(sheet_name)
            ownerships = sheet.get(range_name="F1:F2",
                                   major_dimension=Dimension.cols)
            sheet_owner, account_name = ownerships[0]
            time.sleep(1)

            # Get the column config based from the structure of Excel
            # Column E - Date and Time
            # Column F - Task Name
            # Column H - Processed
            # Column I - Start Time
            # Column J - End Time
            cur_prog = cur_prog + per_job_prog
            progress(left="Downloading", center=sheet_owner,
                     right="Sheet Data...", value=cur_prog)
            datedata = sheet.get(
                range_name=f"{date_col[0]}:{date_col[0]}",
                major_dimension=Dimension.cols,
                date_time_render_option=DateTimeOption.serial_number,
                value_render_option=ValueRenderOption.unformatted)
            time.sleep(1)
            # Get and merge the column letters with the data
            data = sheet.get(range_name=f"{min_col}:{max_col}",
                             major_dimension=Dimension.cols)
            data_merged = dict(zip(col_range, data))
            time.sleep(2)

            # Select only the required columns and assign to each variable
            # Also disregard the first 5 initial row of it's column
            date_times = datedata[0][5:]
            task_names = data_merged[task_col[0]][5:]
            num_processed = data_merged[proccessed_col[0]][5:]
            start_times = data_merged[start_col[0]][5:]
            end_times = data_merged[end_col[0]][5:]
            durations = []

            # Format the times to datetime object
            try:
                for i, strdate in enumerate(date_times):
                    if strdate:
                        date = (datetime(1899, 12, 30) +
                                timedelta(days=int(strdate)))
                        date_times[i] = str(date.date())
                        month_sheet = date.strftime("%B %Y")
                        month_sheet_numeric = date.strftime("%m-%Y")
                for i, stime in enumerate(start_times):
                    start_times[i] = self._sanitize_time(stime)
                for i, etime in enumerate(end_times):
                    end_times[i] = self._sanitize_time(etime)
                # Get the duration of difference in end times and start times
                for st, et in zip(start_times, end_times):
                    if st and et:
                        start_time = datetime.strptime(st, "%I:%M %p")
                        end_time = datetime.strptime(et, "%I:%M %p")
                        duration_str = str(end_time - start_time)
                        durations.append(duration_str.split("day, ")[-1])
                    else:
                        durations.append("")

            except Exception as e:
                progress(left="Download Failed", center=sheet_owner,
                         right="Sheet Data...", value=cur_prog)
                return e

            columns = [date_times, task_names, num_processed,
                       start_times, end_times, durations]

            for index in range(6, len(date_times)):
                result = [department_name, account_name, sheet_owner]
                for column in columns:
                    try:
                        result.append(column[index])
                    except IndexError:
                        result.append("")
                # Don't append the 5th index which is the num_processed if empty
                if result[5]:
                    final_data.append(result)

        # Call the completed callback method after all fetching are done.
        self.timestamp = datetime.now()
        kwargs = {"url": self.url, "owner": department_name,
                  "month": month_sheet, "month_num": month_sheet_numeric,
                  "timestamp": self.timestamp.strftime("%B %d, %Y - %I:%M %p"),
                  "final_data": final_data}
        progress(center=department_name, right="Download Completed", value=1)
        completed(**kwargs)
        return True

    @staticmethod
    def _sanitize_time(strtime):
        """ Helper method to correct the format of datetime string. """
        if len(strtime.split()) > 1:
            timestr, ampm = strtime.split()
            hour, minutes = timestr.split(":")[:2]
            return f"{hour}:{minutes} {ampm}"
        return ""

    @staticmethod
    def generate_csv_report(progress):
        """
        Standalone method to generate a csv report based
        on all the saved JSON from data folder
        """
        # Create first the downloads folder
        path = Reader.BASE_PATH / "downloads"
        data_path = path / "data"
        path.mkdir(exist_ok=True)

        # Get the settings saved configuration data
        settings = SettingsManager.get_settings_data()
        date_name = settings["required"][0][1]
        start_name = settings["required"][1][1]
        end_name = settings["required"][2][1]
        task_name = settings["other_columns"][0][1]
        proccessed_name = settings["other_columns"][1][1]

        # Header column names for the CSV
        headers = ["Department", "Account", "Name", date_name,
                   task_name, proccessed_name, start_name,
                   end_name, "DURATION"]

        # Reset and prime the progress bar
        progress.reset()
        progress.update_progress(left="Generating CSV Report...", value=0)
        time.sleep(2)

        # Create the csv file
        filepath = path / "dataexport.csv"
        with open(filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            # Iterate the data folder and get the final_data key from
            # each JSON file, also skip the recents.json
            total_files = len(list(data_path.iterdir())) - 1
            progress_count = 0
            per_file_prog = 0.9 / total_files
            for path_name in data_path.iterdir():
                if not path_name.name.startswith("recents"):
                    with open(path_name, "r") as file:
                        final_rows = json.loads(file.read())["final_data"]
                        csvwriter.writerows(final_rows)
                        progress_count = progress_count + per_file_prog
                        progress.update_progress(
                            left="Writing",
                            center=path_name.name,
                            right="CSV Data...", value=progress_count)
                        time.sleep(1)
            progress.update_progress(center="CSV REPORT",
                                     right="Generation Completed", value=1)

        # Determine first the OS then call the correct
        # command to open the downloads folder
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
    