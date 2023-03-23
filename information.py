import os
import pandas as pd
import numpy as np
from classroom import Classroom

class ClassInformation():

    def __init__(self, filepath):

        # Choose input file in .xlsx format (provide filepath)
        self.filepath = filepath
        
        self.df = pd.read_excel(self.filepath, sheet_name='Báo dạy 20222')

        # Thêm cột mã lớp
        new_class_code = []
        self.df['STT theo mã HP'] = self.df['STT theo mã HP'].astype(str).str.zfill(3)
        number_code = self.df["STT theo mã HP"].tolist()
        
        for i in number_code:
            new_code = str(i)
            new_class_code.append(new_code)
        self.df.insert(0, "Mã lớp", new_class_code, True)
        self.classroom = Classroom(filepath)
        
        # Tập hợp các loại lớp 
        self.pe_course = []
        self.qt_course = []
        self.mil_course = []
        self.nor_course = []
        self.temp = []
        
        self.no_sort_course = []
        
        for code in self.get_class_code():
            if self.get_school_code(code) == "PE":
                self.pe_course.append(code)
            elif self.get_school_code(code) == "QT":
                self.qt_course.append(code)
            elif self.get_school_code(code) == "MIL":
                self.mil_course.append(code)
            else:
                self.nor_course.append(code)
                self.temp.append(code)
                
        for course in self.temp:
            if self.get_periods("theory", course) == 0 and self.get_periods("exercise", course) == 0:
                self.no_sort_course.append(course)
                self.nor_course.remove(course)
            
    def get_table(self):
        return self.df
    
    def get_student_number(self, class_code):
        '''Trả về số sinh viên từng Mã HP'''
        class_index = self.df.index[self.df['Mã lớp'] == class_code[0:3]].astype(int)[0]
        return self.df.at[class_index, 'Số SV lớp cố định'].astype(int)
    
    def get_course_iden_code(self, course_code):
        class_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
        return self.df.at[class_index, 'MÃ HP']
    
    def get_school_code(self, course_code):
        course_i_code = self.get_course_iden_code(course_code)
        not_to_append = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        outt = []
        for char in list(course_i_code):
            if char not in not_to_append:
                outt.append(char)
        if outt[-1] == "Q":
            outt.remove(outt[-1])
        return "".join(outt)
    
    def get_periods(self, type_of_periods, course_code):
        course_weight = self.get_class_weight(course_code)
        periods_set = course_weight.split("(")[1].split(")")[0].split("-")
    
        if type_of_periods == "credits":
            period_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
            periods_retrieve = str(self.df.at[period_index, 'KHỐI LƯỢNG '])
            if int(periods_retrieve[0]) <= 9:
                periods = str(periods_retrieve)[0]
            else:
                periods = str(periods_retrieve)[0] + str(periods_retrieve)[1]
            periods = int(periods)
            return periods
        
        if type_of_periods == "theory":
            return int(periods_set[0])
        
        if type_of_periods == "exercise":
            return int(periods_set[1])
        
        if type_of_periods == "lab":
            return int(periods_set[3])
        
        if type_of_periods == "self-study":
            return int(periods_set[2])
        
        if type_of_periods == "full":
            return sum([int(per) for per in periods[0:2]])
        
    def get_participant_class(self, class_code):
        '''Trả về tập hợp các lớp con tham gia một Mã HP'''
        participant_class_index = self.df.index[self.df['Mã lớp'] == class_code[0:3]].astype(int)[0]
        participant_class = self.df.at[participant_class_index, "Lớp"]
        participant_class_list = list(participant_class.split("+"))
        for i in participant_class_list:
            if i == 'B':
                B_index = participant_class_list.index('B')
                participant_class_list[B_index - 1] = participant_class_list[B_index - 1] + "+" + \
                                                      participant_class_list[B_index]
                participant_class_list.remove("B")
        return participant_class_list

    def get_class_code(self):
        class_code = self.df["Mã lớp"].to_list()
        return class_code

    def get_class_group(self, class_code):
        '''Trả về các lớp con tham gia một Mã HP'''
        participant_class_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        class_group = self.df.at[participant_class_index, "Lớp"]
        return class_group
    
    def get_class_weight(self, class_code):
        """Trả về khối lượng tín chỉ của học phần dựa vào mã lớp"""
        period_index = self.df.index[self.df['Mã lớp'] == class_code].astype(int)[0]
        periods_retrieve = self.df.at[period_index, 'KHỐI LƯỢNG ']
        return periods_retrieve
    
    def largest_class_group(self, group_class_set):
        """Trả về số lượng lớp con lớn nhất có thể có trong một nhóm lớp"""
        max = 0
        for cgroup in group_class_set:
            if len(cgroup) > max:
                max = len(cgroup)
        return max
    
    def class_group_with_num_of_subclass_equal_to(self, num):
        output = []
        for cgroup in self.group_class_set():
            if len(cgroup) == num:
                output.append(cgroup)
        return output
    
    def class_g_dict(self, group_class_set, largest):
        temp_group = []
        for cgroup in group_class_set:
            if len(cgroup) == largest:
                temp_group.append(cgroup)
                group_class_set.remove(cgroup)
                
        cgroup_dict = {}
        for i in range(len(temp_group)):
            cgroup_dict[f"G{i}"] = temp_group[i]
        
        return cgroup_dict
            
    def group_class_set(self):
        """Trả về các nhóm lớp"""
        temp = []
        for code in self.get_class_code():
           temp.append(sorted(self.get_participant_class(code)))
        group_class_set = []
        for group_class in temp:
            if group_class not in group_class_set:
                group_class_set.append(group_class)
        
        return group_class_set
    
    def group_course_by_cgroup(self, sort_course_set):
        """Trả về tập hợp có khóa là nhóm lớp, giá trị là các mã hp mà nhóm lớp đó học"""
        out_dict = {}
        
        temp_set = []
        for code in sort_course_set:
            temp_set.append(self.get_participant_class(code))
            
        unique = []
        for cgroup in temp_set:
            if cgroup not in unique and len(cgroup) == 1:
                unique.append(cgroup)
        
        final_set = []
        for cgroup in unique:
            final_set += cgroup
        
        for cgroup in final_set:
            out_dict[cgroup] = []
        
        for cgroup in out_dict:
            for code in sort_course_set:
                if cgroup in self.get_participant_class(code):
                    out_dict[cgroup].append(code)
        return out_dict
    
    def group_of_class(self, course_set):
        output_dict = {}
        for course_code in course_set:
            output_dict[course_code] = self.get_class_group(course_code)
        return output_dict
    
    def code_to_class(self, course_set):
        output_dict = {}
        for course_code in course_set:
            output_dict[course_code] = self.get_participant_class(course_code)
        return output_dict
    
    def class_to_set_of_course(self, course_set):
        out_dict = {}
        
        unique = []
        for course in course_set:
            if self.get_class_group(course[0:3]) not in unique:
                unique.append(self.get_class_group(course[0:3]))
                
        for cgroup in unique:
            out_dict[cgroup] = []
            
        for course in course_set:
            out_dict[self.get_class_group(course[0:3])].append(course)
            
        return out_dict
        
    def get_school(self, course_code):
        course_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
        return self.df.at[course_index, 'Viện chuyên ngành']
    
    def get_course_name(self, course_code):
        course_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
        return self.df.at[course_index, 'TÊN HP']
    
    def course_note(self, course_code):
        course_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
        return f"[SIE-{self.df.at[course_index, 'STT theo mã HP']}-{self.df.at[course_index, 'Ngôn ngữ dạy']}]-{self.get_class_group(course_code)}"
        
    def get_num_of_class(self, course_code):
        return len(self.get_participant_class(course_code))
    
    def get_class_group_student_number(self, class_group):
        '''Trả về sĩ số của nhóm lớp'''
        group_student_index = self.df.index[self.df['Lớp'] == class_group].astype(int)[0]
        class_group_student_number = self.df.at[group_student_index, "Số SV lớp cố định"]
        return class_group_student_number
    
    def group_course_by_capacity(self, course_code_set):
        """Nhóm các mã HP bởi sức chứa phòng phủ hợp với số SV của lớp đó"""
        course_dict = {}
        for capacity in self.classroom.get_unique_classroom_capacity():
            course_dict[capacity] = []
        for course in course_code_set.keys():
            for capacity in self.classroom.get_unique_classroom_capacity():
                if capacity != 0:
                    if self.get_student_number(course[0:3]) <= 0.9 * capacity:
                        course_dict[capacity].append(course)  
                        break
        for capacity in self.classroom.get_unique_classroom_capacity():
            course_dict[capacity] = sorted(course_dict[capacity], key=lambda x: course_code_set[x])
        return course_dict
    
    def fit_to_room(self, course_code):
        """Trả về sức chứa phù hợp cho một mã hp"""
        for capacity in self.classroom.get_unique_classroom_capacity():
            if capacity != 0 and self.get_student_number(course_code[0:3]) <= 0.9 * capacity:
                return capacity
            
    def group_course(self, course_code_set):

        course_dict = {}
        for course in course_code_set:
            theory = self.get_periods("theory", course)
            exercise = self.get_periods("exercise", course)
            lab = self.get_periods("lab", course)

            if theory + exercise == 0:
                course_dict[course] = [lab]
            elif theory + exercise == 1:
                course_dict[course] = [theory, lab]
            elif theory + exercise < 4:
                course_dict[course] = [theory + exercise]
            elif theory + exercise == 4:
                course_dict[course] = [2, 2]
            elif theory + exercise > 4:
                course_dict[course] = [theory, exercise]
        
        for key in course_code_set:
            if len(course_dict[key]) == 1:
                course_dict[key] = course_dict[key][0]
            else:
                num_of_class = len(course_dict[key])
                for i in range(num_of_class):
                    course_dict[f"{key}[{i + 1}]"] = course_dict[key][i]
                del course_dict[key]
                
        return course_dict
    
    def get_set_of_course(self, group):
        if group == "PE":
            return self.pe_course
        if group == "QT":
            return self.qt_course
        if group == "MIL":
            return self.mil_course
        if group == "normal":
            return self.nor_course
        
    def language_course_divider(self):
        
        japan_150_course = [3] * 3
        japan_270_course = [4, 4, 4, 3, 3]
        
        german_180_course = [4, 4, 4]
        german_105_course = [3, 4]
        german_120_course = [4, 4]
        
        # language_course_set = {}
        
        course_set = {"japanese": [], "english": [], "german": []}
        for course in self.qt_course:
            if self.get_course_name(course).split(" ")[1] == "Anh":
                course_set["english"].append(course)
            elif self.get_course_name(course).split(" ")[1] == "Đức":
                course_set["german"].append(course)
            elif self.get_course_name(course).split(" ")[1] == "Nhật":
                course_set["japanese"].append(course)
        
        # English
        temp = {}
        for course in course_set["english"]:
            for i in range(2):
                temp[f"{course}[{i + 1}]"] = 2
        course_set["english"] = temp
        
        # Japanese
        temp = {"normal": {}, "evening": {}}
        for course in course_set["japanese"]:
            if self.get_class_weight(course) == 150:
                for i in range(len(japan_150_course)):
                    temp["evening"][f"{course}[{i + 1}]"] = japan_150_course[i]
            elif self.get_class_weight(course) == 270:
                for i in range(len(japan_270_course)):
                    temp["normal"][f"{course}[{i + 1}]"] = japan_270_course[i]
        course_set["japanese"] = temp
        
        # German 
        german_course_set = {"180": [], "120": [], "105":[]}
        for course in course_set["german"]:
            create_check = [int(round(float(num))) for num in self.get_class_weight(course).split("(")[1].split(")")[0].split("-")]
            check = create_check[0] + create_check[1]
            if check == 12:
                german_course_set["180"].append(course)
            elif check == 8:
                german_course_set["120"].append(course)
            elif check == 7:
                german_course_set["105"].append(course)
        
        temp = {}
        for course in course_set["german"]:
            if course in german_course_set["180"]:
                for i in range(len(german_180_course)):
                    temp[f"{course}[{i + 1}]"] = german_180_course[i]
            elif course in german_course_set["120"]:
                for i in range(len(german_120_course)):
                    temp[f"{course}[{i + 1}]"] = german_120_course[i]
            elif course in german_course_set["105"]:
                for i in range(len(german_105_course)):
                    temp[f"{course}[{i + 1}]"] = german_105_course[i]
                    
        course_set["german"] = temp
        
        return course_set
    def get_semester(self, course_code):
        """
        Parameter: course_code
        Description: return learn semester of this course code (A or B or AB)
        """
        class_index = self.df.index[self.df['Mã lớp'] == course_code].astype(int)[0]
        return self.df.at[class_index, 'Kỳ học']