import argparse
from pathlib import Path

import pandas as pd

import shapefile
from employee import Employee
from visualisation import *


class Area():
    def __init__(self, area_name, coordinates):
        self.area_name = area_name
        self.coordinates = coordinates


def check_filepaths(arg, filepath):
    if Path(filepath).is_file() and arg == "employee":
        return
    elif Path(filepath).is_dir() and arg == "aoi":
        return
    else:
        raise FileNotFoundError(filepath + " does not exist")


def create_employees(employee_filepath):
    employee_data = pd.read_csv(employee_filepath)
    employee_classes = []

    for x in employee_data['employee'].unique():
        single_employee_df = employee_data.loc[employee_data['employee'] == x].drop(['employee'], axis=1)
        employee_classes.append(Employee(x, single_employee_df))

    return employee_classes


def create_areas(aoi_filepath):
    aoi = []

    for shape_file in Path(aoi_filepath).iterdir():
        if shape_file.suffix == '.shp': # Check to ensure only loading .shp file
            shape = shapefile.Reader(str(shape_file))
            for i in range(len(shape.records())):
                area_name = shape.records()[i][1]
                coordinates = shape.shapeRecords()[i].shape.__geo_interface__['coordinates']
                aoi.append(Area(area_name, coordinates))

    return aoi


def main(args):
    # Checking Filepaths
    for arg, filepath in vars(args).items():
        if filepath is not None:
            check_filepaths(arg, filepath)

    # Creating Class Instances
    employee_classes = create_employees(args.employee)
    aoi_classes = create_areas(args.aoi)

    # Calculating Information
    for instance in employee_classes:
        instance.most_time_within_area(aoi_classes)
        instance.most_time_within_or_near_area(aoi_classes)
        instance.most_visited_area(aoi_classes)
        instance.calculate_speed()

    # Visualising Information
    stacked_bar_area_times(employee_classes, aoi_classes)
    stacked_bar_area_times_near(employee_classes, aoi_classes)
    pie_most_visited_area(employee_classes, aoi_classes)
    line_speed(employee_classes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Biarri Tech Test')
    parser.add_argument('employee', type=str,
                        help='Employee Locations CSV filepath')
    parser.add_argument('--aoi', type=str,
                        help='Filepath to Fflder containing .shp Area of Interest files')

    args = parser.parse_args()

    main(args)
