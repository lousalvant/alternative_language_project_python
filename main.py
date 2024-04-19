import csv
import re

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

def read_csv(file_path):
    cells = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cell = Cell(**row)
            cells.append(cell)
    return cells

if __name__ == "__main__":
    file_path = "cells.csv"
    cells = read_csv(file_path)
