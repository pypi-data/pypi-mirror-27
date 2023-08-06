import csv
import datetime
import logging
import os
import re

import me
import me.spreadsheet

def parse_date(string):
    return datetime.datetime.strptime(str(string), "%Y-%m-%d").date()


def read_csv(path):
    with open(path) as infile:
        reader = csv.reader(infile)
        rows = []
        first = True
        for row in reader:
            if first:
                rows.append(row)
                first = False
            else:
                rows.append([parse_date(row[0])] + row[1:])
    return rows


def get_row(data, date):
    for row in data[1:]:
        if row[0] > date:
            return [''] * (len(data[0]) - 1)
        elif row[0] == date:
            return row[1:]
    return [''] * (len(data[0]) - 1)


def aggregate(outdir, keypath, share_with):
    csvs = [
        "Step Count.csv",
        "Heart Rate.csv",
        "Distance.csv",
        "Calories Burned.csv",
        "Calories Consumed.csv",
        "Water.csv",
        "Caffeine.csv",
        "Weight.csv",
        "BMI.csv",
        "OmniFocus Tasks.csv",
    ]

    csv_data = [read_csv(f"{outdir}/{x}") for x in csvs]

    # Get the earlest reading date
    start_date = min(x[1][0] for x in csv_data)
    end_date = max(x[1][0] for x in csv_data)
    nrecords = sum(len(x) - 1 for x in csv_data)
    logging.info(f'Aggregating {nrecords} records from {start_date} to {end_date} in "{outdir}/me.csv"')

    with open(f"{outdir}/me.csv", "w") as outfile:
        writer = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        header = []
        for data in csv_data:
            header += data[0][1:]
        writer.writerow(['Date'] + header)
        for date in me.daterange(start_date, end_date, reverse=True):
            row = []
            for data in csv_data:
                row += get_row(data, date)
            writer.writerow([date] + row)

    logging.info(f'Updating worksheet "Data"')
    gc = me.spreadsheet.get_connection(keypath)
    sh = me.spreadsheet.get_or_create_spreadsheet(gc, "me.csv", share_with)
    worksheet = me.spreadsheet.get_or_create_worksheet(sh, f"Data")
    with open(f"{outdir}/me.csv") as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader]
        me.spreadsheet.csv_to_worksheet(worksheet, rows)
