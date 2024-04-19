import csv
import re
from collections import defaultdict

class Cell:
    def __init__(self, oem, model, launch_announced, launch_status, body_dimensions, body_weight, body_sim,
                 display_type, display_size, display_resolution, features_sensors, platform_os):
        self.oem = oem
        self.model = model
        self.launch_announced = self.parse_year(launch_announced)
        self.launch_status = self.parse_year_or_string(launch_status)
        self.body_dimensions = self.parse_string(body_dimensions)
        self.body_weight = self.parse_weight(body_weight)
        self.body_sim = self.parse_sim(body_sim)
        self.display_type = self.parse_string(display_type)
        self.display_size = self.parse_float(display_size)
        self.display_resolution = self.parse_string(display_resolution)
        self.features_sensors = self.parse_string(features_sensors)
        self.platform_os = self.parse_platform_os(platform_os)

    def parse_year(self, value):
        try:
            return int(re.search(r'\d{4}', value).group())
        except AttributeError:
            return 0

    def parse_year_or_string(self, value):
        if re.match(r'\d{4}', value):
            return self.parse_year(value)
        else:
            return value

    def parse_string(self, value):
        return None if value == "-" else value

    def parse_weight(self, value):
        try:
            return float(re.search(r'\d+(\.\d+)?', value).group())
        except AttributeError:
            return None

    def parse_sim(self, value):
        return None if value.lower() == "no" else value

    def parse_float(self, value):
        try:
            return float(re.search(r'\d+(\.\d+)?', value).group())
        except AttributeError:
            return None

    def parse_platform_os(self, value):
        return value.split(',')[0].strip() if ',' in value else value

    def __str__(self):
        return f"{self.oem} | {self.model} | {self.launch_announced} | {self.launch_status} | {self.body_dimensions} | {self.body_weight} | {self.body_sim} | {self.display_type} | {self.display_size} | {self.display_resolution} | {self.features_sensors} | {self.platform_os}"

def read_csv(file_path):
    cells = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cell = Cell(**row)
            cells.append(cell)
    return cells

def calculate_highest_avg_body_weight(cells):
    avg_weights = defaultdict(float)
    counts = defaultdict(int)
    for cell in cells:
        weight = cell.body_weight
        if weight is not None:
            avg_weights[cell.oem] += weight
            counts[cell.oem] += 1
    highest_avg_oem = max(avg_weights, key=lambda x: avg_weights[x] / counts[x])
    print("OEM with highest average body weight:", highest_avg_oem)

def find_phones_announced_released_different_year(cells):
    mismatched_announced_released = [(cell.oem, cell.model) for cell in cells if isinstance(cell.launch_announced, int) and isinstance(cell.launch_status, int) and cell.launch_announced != cell.launch_status]
    if mismatched_announced_released:
        print("Phones announced in one year and released in another:")
        for oem, model in mismatched_announced_released:
            print(f"OEM: {oem}, Model: {model}")
    else:
        print("No phones announced in one year and released in another.")

def count_phones_with_single_sensor(cells):
    count = sum(1 for cell in cells if cell.features_sensors and len(cell.features_sensors.split(',')) == 1)
    print("Number of phones with only one feature sensor:", count)

def find_year_with_most_launches(cells):
    launch_years = [cell.launch_announced for cell in cells if isinstance(cell.launch_announced, int) and cell.launch_announced > 1999]
    if launch_years:
        most_common_year = max(set(launch_years), key=launch_years.count)
        count_most_common_year = launch_years.count(most_common_year)
        print("Year with the most phones launched (later than 1999):", most_common_year, "with", count_most_common_year, "phones.")
    else:
        print("No phones launched later than 1999.")

if __name__ == "__main__":
    file_path = "cells.csv"
    cells = read_csv(file_path)

    print("OEM            | Model               | Launch Announced | Launch Status   | Body Dimensions    | Body Weight | Body SIM      | Display Type       | Display Size | Display Resolution | Features Sensors   | Platform OS        ")
    for cell in cells:
        print(cell)

    calculate_highest_avg_body_weight(cells)
    find_phones_announced_released_different_year(cells)
    count_phones_with_single_sensor(cells)
    find_year_with_most_launches(cells)
