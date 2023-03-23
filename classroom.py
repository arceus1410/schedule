import os
import pandas as pd
import numpy as np

class Classroom:

    def __init__(self, filepath):

        # Choose input file in .xlsx format (provide filepath)
        self.filepath = filepath
        # Read sheet contain Classroom data
        self.df = pd.read_excel(self.filepath, sheet_name='Phòng học')
        # Get two column contain necessary data (Classroom name and Classroom capacity)
        self.df = self.df[["Số phòng mới", "Số chỗ ngồi"]]
        # A dict contain classroom group by capacity
        
    def get_table(self):
        """Get the whole table"""
        return self.df

    def get_classroom_list(self):
        """Get only classrooms name set"""
        classroom_list = self.df["Số phòng mới"].to_list()
        return classroom_list

    def get_classroom_capacity(self, classroom_name):
        """Get the capacity of classroom"""
        class_capacity_index = self.df.index[self.df['Số phòng mới'] == classroom_name].astype(int)[0]
        return self.df.at[class_capacity_index, "Số chỗ ngồi"]
    
    def get_unique_classroom_capacity(self):
        "Get list of unique classroom capacity"
        cc = self.df["Số chỗ ngồi"].to_list()
        unique = []
        for capa in cc:
            if capa not in unique and capa != 0:
                unique.append(int(capa))
        return sorted(unique)
    
    def full_classroom(self):
        """Create a classroom dictionary, contains availabel slot of the course, remain for full of one class, used by what class"""
        classroom_dict = {}
        for room in self.get_classroom_list():
            classroom_dict[room] = {"available": 10, "evening": 9, "session remain": 2, "used by": {1: [], 2:[], 3:[]}}
        return classroom_dict
    
    def group_of_classroom_by_capacity(self):
        """Create a dictionary, keys are capacity of a room and value are a list contains classroom has this capacity"""
        classroom_dict = {}
        
        for capacity in self.get_unique_classroom_capacity():
            classroom_dict[capacity] = []
        for classroom in self.get_classroom_list():
            if self.get_classroom_capacity(classroom) != 0:
                classroom_dict[self.get_classroom_capacity(classroom)].append(classroom)
        return classroom_dict
