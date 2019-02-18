import multiprocessing as mp
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from shapely.affinity import scale
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Employee():
    def __init__(self, employee, df):
        self.employee = employee
        self.df = df.reset_index(drop=True)
        self.area_times = None
        self.near_area_times = None
        self.area_visits = None
        self.speed = None


    def calculate_point_within_area(self, area, row):

        point = Point(row[1]['long'], row[1]['lat'])
        polygon = Polygon(list(area.coordinates[0]))

        return polygon.contains(point)


    def calculate_point_within_or_near_area(self, area, row, near_factor=0.1):

        point = Point(row[1]['long'], row[1]['lat'])
        polygon = Polygon(list(area.coordinates[0]))
        polygon = scale(polygon, xfact=1+near_factor, yfact=1+near_factor, origin='centroid')
        
        return polygon.contains(point)


    def most_time_within_area(self, areas):

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        results = [pool.apply(self.calculate_point_within_area, args=(i, j,)) for i in areas for j in self.df.iterrows()]

        area_times = {}
        for x in range(len(areas)):
            area_times[x+1] = timedelta(days=0, hours=0, seconds=0, microseconds=0)

        for i, result in enumerate(results):
            if result is True:
                row_index = i % self.df.shape[0]
                area_number = int(i / self.df.shape[0]) + 1
                if row_index != self.df.shape[0] - 1:
                    start_time = datetime.strptime(self.df.loc[row_index, :]['time'], '%H:%M:%S')
                    end_time = datetime.strptime(self.df.loc[row_index+1, :]['time'], '%H:%M:%S')

                    total_time = end_time - start_time
                    area_times[area_number] = area_times[area_number] + total_time

        self.area_times = area_times 

    def most_time_within_or_near_area(self, areas):

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        results = [pool.apply(self.calculate_point_within_or_near_area, args=(i, j,)) for i in areas for j in self.df.iterrows()]

        near_area_times = {}
        for x in range(len(areas)):
            near_area_times[x+1] = timedelta(days=0, hours=0, seconds=0, microseconds=0)

        for i, result in enumerate(results):
            if result is True:
                row_index = i % self.df.shape[0]
                area_number = int(i / self.df.shape[0]) + 1
                if row_index != self.df.shape[0] - 1:
                    start_time = datetime.strptime(self.df.loc[row_index, :]['time'], '%H:%M:%S')
                    end_time = datetime.strptime(self.df.loc[row_index+1, :]['time'], '%H:%M:%S')

                    total_time = end_time - start_time
                    near_area_times[area_number] = near_area_times[area_number] + total_time

        self.near_area_times = near_area_times 

    def most_visited_area(self, areas):

        pool = mp.Pool(processes=(mp.cpu_count() - 1))
        results = [pool.apply(self.calculate_point_within_area, args=(i, j,)) for i in areas for j in self.df.iterrows()]

        area_visits = {}
        for x in range(len(areas)):
            area_visits[x+1] = 0

        areas_visited = []

        for i, result in enumerate(results):
            if result is True:
                row_index = i % self.df.shape[0]
                area_number = int(i / self.df.shape[0]) + 1

                if row_index != self.df.shape[0] - 1:
                    if results[i+1] == True and i not in areas_visited:

                            counter = 1
                            while results[i+counter] == True:
                                counter += 1

                            for x in range(i, i+counter):
                                areas_visited.append(x)
                            
                            area_visits[area_number] += 1 
                    
        self.area_visits = area_visits

    def calculate_speed(self):

        if self.employee == "Person 2": # This assumption is only for the Tech Test
            df = self.df
            df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
          
            dist = df.diff().fillna(0.)

            dist['Dist'] = np.sqrt(dist.lat**2 + dist.long**2)
            dist = dist.drop(dist.index[[0]])
            dist['time'] = dist['time'] / np.timedelta64(1, 's')

            dist['Speed'] = dist['Dist'] / dist['time']

            self.speed = dist['Speed']
