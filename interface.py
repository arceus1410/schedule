from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
import pandas as pd
import numpy as np
from classroom import Classroom
from information import ClassInformation
import itertools
from itertools import combinations_with_replacement
from functools import reduce
from time import *
import random
import math 

class SieInterface(Tk):
    
    def __init__(self):
        super().__init__()

        self.title("SIE-HUST Scheduling Program")
        self.geometry("480x250")
        self.resizable(False, False) 
        
        self.displayMenu()
        self.displayBox()
        self.displayLabel()
        self.displayButton()
        self.displayCheckBox()
        self.iconbitmap("D:/lab/tkb/TKBSIE/NonScheduling-main/bitmap/hust_logo.ico")
        
    def choose_file(self):
        filetypes = (
            ('excel file', "*.xlsx"),
        )

        self.filename = fd.askopenfilename(
            title='Mở file',
            initialdir='/',
            filetypes=filetypes)
        
        self.filepath_entry.insert(END, self.filename)

    def export_file(self):
        
        export_filename = fd.asksaveasfilename(title="Lưu file", initialdir='/', filetypes=[('excel file', "*.xlsx")], defaultextension=".xlsx") 
        
        self.expected_timetable.to_excel(export_filename)
    
    def displayMenu(self):
        # Menu
        self.menubar = Menu(self)
    
        ## File menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Mở....", command=self.choose_file)
        self.filemenu.add_command(label="Lưu", command=self.export_file)
        
        self.filemenu.add_separator()
        
        self.filemenu.add_command(label="Thoát")
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        ## Help menu
        
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Hướng dẫn")
        
        self.helpmenu.add_separator()
        
        self.helpmenu.add_command(label="Liên hệ")
        self.menubar.add_cascade(label="Hỗ trợ", menu=self.helpmenu)
        
        # Add menu
        self.config(menu=self.menubar)
    
    # Box
    def displayBox(self):
        self.filepath_entry = Text(self, font=("Times New Roman", 15), width=28, height=1)
        self.filepath_entry.grid(column=1, row=1, columnspan=2, sticky=W)
        
    # Label
    def displayLabel(self):
        self.title_label = Label(self, text="SIE-HUST\nTIMETABLE SCHEDULING PROGRAM", font=("Times New Roman", 15, "italic bold"), anchor=CENTER)
        self.title_label.grid(column=0, row=0, pady=15, columnspan=4)
        
        self.entry_label = Label(self, text="Đường dẫn: ", font=("Times New Roman", 15))
        self.entry_label.grid(column=0, row=1, padx=10, sticky=W)
        
        self.option_label = Label(self, text="Lựa chọn: ", font=("Times New Roman", 15))
        self.option_label.grid(column=0, row=2, padx=10, pady=(15, 0), sticky=W)
        
    # Button
    def displayButton(self):
        
        self.choose_filepath_button = Button(self, text="...", font=("Oswald", 10, "bold"), command=self.choose_file)
        self.choose_filepath_button.grid(column=3, row=1, padx=10)
        
        self.export_file_button = Button(self, text="Xuất file", font=(10), width=7, command=self.export_file)
        self.export_file_button.place(x=369, y=190)
        
        self.running_button = Button(self, text="Chạy", font=(10), width=7, command=self.run_program)
        self.running_button.place(x=369, y=140)
        
    def displayCheckBox(self):
        
        self.tvar = IntVar()
        self.tvar.set(0)
        
        self.crvar = IntVar()
        self.crvar.set(0)
        
        self.cvar = IntVar()
        self.cvar.set(0)
        
        self.timetabel_check = Checkbutton(self, var=self.tvar, onvalue=1, offvalue=0, text="Thời khóa biểu", font=("Times New Roman", 15))
        self.timetabel_check.grid(column=1, row=2, pady=(15, 0), sticky=W)
        
        self.classroom_check = Checkbutton(self, var=self.crvar, onvalue=1, offvalue=0, text="Biểu đồ phòng", font=("Times New Roman", 15))
        self.classroom_check.grid(column=1, row=3, sticky=W)
        
        self.class_check = Checkbutton(self, var=self.cvar, onvalue=1, offvalue=0, text="Biểu đồ lớp", font=("Times New Roman", 15))
        self.class_check.grid(column=1, row=4, sticky=W)
    
    def run_program(self):
        
        try:
            running_time = 0
            
            start_time = time()
    
            # Khởi tạo hai đối tượng "phòng học" và "thông tin"
    
            classroom = self.get_classroom_from_interface()
            information = self.get_information_from_interface()
    
            # Tập hợp các phòng học
            classroom_set_by_capacity = classroom.group_of_classroom_by_capacity()
    
            temp_classroom_set_by_capacity = classroom.group_of_classroom_by_capacity()
            # Tập hợp các sức chứa có thể của một phòng 
            capacity_set = classroom.get_unique_classroom_capacity()
    
            # Tập hợp các mã học phần thông thường 
            course_normal_periods = information.get_set_of_course("normal")
    
            # Tập hợp các mã học phần chỉ có duy nhất một lớp học
            one_cgroup_dict = [course_code for course_code in course_normal_periods if information.get_num_of_class(course_code) == 1]
    
            # Tập hợp các mã học phần có nhiều lớp học 
            mul_cgroup_dict = [course_code for course_code in course_normal_periods if course_code not in one_cgroup_dict]
    
            # Tập hợp các mã học phần giáo dục thể chất
            pe_course = information.get_set_of_course("PE")
    
            # Tập hợp các mã học phần quân sự 
            mil_course = information.get_set_of_course("MIL")
    
            # Tập hợp các mã học phần ngoại ngữ
            eng_course = information.language_course_divider()["english"]
            ger_course = information.language_course_divider()["german"]
            jap_course = information.language_course_divider()["japanese"]
    
            # Tập hợp toàn bộ mã học phần đi kèm với khối lượng của nó 
            course_code_set = information.group_course(one_cgroup_dict)
            # course_code_set.update(eng_course)
            # course_code_set.update(information.group_course(mul_cgroup_dict))
    
            # Tập hợp các mã học phần sắp xếp theo nhóm sức chứa của phòng phù hợp với mã hp đó
            course_code_set_by_capacity = information.group_course_by_capacity(course_code_set)
    
            # Temp set
            temp_course_code_set = information.group_course_by_capacity(course_code_set)
    
            # Tập hợp các nhóm lớp
            # group_class_set = information.group_class_set()
    
            # Số lượng lớp con lớn nhất có thể trong một nhóm lớp
            # largest = information.largest_class_group(group_class_set)
    
            # Tập hợp mã lớp đi kèm với nhóm lớp học lớp đó 
            code_to_cgroup = information.group_of_class(course_normal_periods)
    
            # Tập hợp toàn bộ phòng học
            classroom_set = classroom.full_classroom()
    
            classroom_set_of_cgroup= {}
            for room in classroom.get_classroom_list():
                classroom_set_of_cgroup[room] = {"used by": {1: [], 2: [], 3: []}}
            # Tập hợp tiết học và thời gian bắt đầu tương ứng của nó 
            time_set = {"Sáng": 
                        {1: {"start": "6h45", "end": "7h30"}, 
                         2: {"start": "7h30", "end": "8h15"},
                         3: {"start": "8h25", "end": "9h10"}, 
                         4: {"start": "9h20", "end": "10h05"},
                         5: {"start": "10h15", "end": "10h50"}, 
                         6: {"start": "11h00", "end": "11h45"}
                        },
                        "Chiều":
                        {1: {"start": "12h30", "end": "13h15"}, 
                         2: {"start": "13h15", "end": "14h00"},
                         3: {"start": "14h10", "end": "14h55"}, 
                         4: {"start": "15h05", "end": "15h50"},
                         5: {"start": "16h00", "end": "16h45"}, 
                         6: {"start": "16h45", "end": "17h30"}
                         },
                         "Tối":
                         {1: {"start": "17h45", "end": "18h30"}, 
                          2: {"start": "18h30", "end": "19h15"},
                          3: {"start": "19h25", "end": "20h10"}
                        }
                    }
            # Tập hợp chứa mã hp đi cùng với các lớp học mã hp đó
            # group_of_classes = information.group_of_class(course_normal_periods)
            # group_course_by_class = information.group_course_by_cgroup(course_normal_periods)
    
            """Tập hợp các nhóm lớp, trong mỗi tập là lớp con của nhóm lớp đó (có thể chứa 1, 2, ... lớp con)
            các lớp con được nhóm tiếp thành các tập 1, 2, 3,... lớp con riêng biệt, mỗi lớp con là một
            dictionary chứa các mã lớp mà lớp con đó học"""
    
            # class_group_dict = information.class_g_dict(group_class_set, largest)
            #------------------------------------------------------------------------------
            def remove_sorted(temp_set, course_set):
                for course in temp_set:
                    # course_normal_periods.remove(course[0:6])
                    course_set.remove(course)
    
            def room_to_use(capacity, time_of_day):
                temp_classroom_set = temp_classroom_set_by_capacity[capacity]
                
                if time_of_day == "normal":
                    
                    for room in temp_classroom_set:
                        if classroom_set[room]["session remain"] == 0:
                            temp_classroom_set_by_capacity[capacity].remove(room)
                            
                    if len(temp_classroom_set) == 0:
                        capacity = capacity_set[capacity_set.index(capacity) + 1]
                        temp_classroom_set = temp_classroom_set_by_capacity[capacity]
                        # return temp_classroom_set[-1]
                        
                    for room in temp_classroom_set:
                        if classroom_set[room]["available"] > 1 and classroom_set[room]["session remain"] > 0:
                            return room
                elif time_of_day == "evening":
                    
                    for room in temp_classroom_set:
                        if classroom_set[room]["session remain"] == 0:
                            temp_classroom_set_by_capacity[capacity].remove(room)
                            
                    if len(temp_classroom_set) == 0:
                        capacity = capacity_set[capacity_set.index(capacity) + 1]
                        temp_classroom_set = temp_classroom_set_by_capacity[capacity]
                        # return temp_classroom_set[-1]
                        
                    for room in temp_classroom_set:
                        if classroom_set[room]["evening"] > 0:
                            return room
                    
            def get_full_periods(course_set):
                
                count_2 = sum([course_code_set[course] for course in course_set if course_code_set[course] == 2])
                count_3 = sum([course_code_set[course] for course in course_set if course_code_set[course] == 3])
                return [count_2, count_3]
    
            def group_course_to_sort(periods_group, course_set):
                out_set = []
                A = periods_group[0]
                B = periods_group[1]
    
                if A % 6 == 0 and B % 6 == 0:
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
    
                elif A % 6 == 0 and B % 6 == 3:
                        
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                        
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                        
                    temp = []
                    temp.append(course_set[0])
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
    
                elif A % 6 == 2 and B % 6 == 0:
                    
                    temp = []
                    temp.append(course_set[0])
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
                    
                    A -= 2
                    
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                            
                elif A % 6 == 4 and B % 6 == 0:
    
                    temp = course_set[0:2]
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
                    
                    A -= 4
                    
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                        
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
    
                elif A % 6 == 2 and B % 6 == 3:
    
                    temp = course_set[::len(course_set)-1]
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
                    
                    A -= 2
                    B -= 3
                    
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                        
                elif A % 6 == 4 and B % 6 == 3:
                    
                    temp = course_set[::len(course_set)-1]
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
                    
                    temp = []
                    temp.append(course_set[0])
                    out_set.append(temp)
                    remove_sorted(temp, course_set)
                    
                    A -= 4
                    B -= 3
                    
                    for loop2 in range(A // 6):
                        temp = course_set[0:3]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
                    
                    for loop3 in range(B // 6):
                        temp = course_set[0:2]
                        out_set.append(temp)
                        remove_sorted(temp, course_set)
    
                return out_set
    
            def group_course_each_cgroup(set_of_cgroup):
                for cgroup in set_of_cgroup:
                    periods_set = get_full_periods(set_of_cgroup[cgroup])
                    set_of_cgroup[cgroup] = group_course_to_sort(periods_set, set_of_cgroup[cgroup])
                    temp_course_code_set[capacity][cgroup.split(" ")[0]] = {"courses": set_of_cgroup[cgroup], "numbers": len(set_of_cgroup[cgroup])}
                    
            for capacity in capacity_set:
                temp_set = information.class_to_set_of_course(temp_course_code_set[capacity])
                temp_course_code_set[capacity] = {}
                group_course_each_cgroup(temp_set)
    
            def get_pers_set(capacity):
                length_set = [temp_course_code_set[capacity][cgroup]["numbers"] for cgroup in temp_course_code_set[capacity]]
                return length_set
    
            def make_set_of_class(capacity):
                x = sorted(get_pers_set(capacity))
                buckets = []
    
                while True:
                    if x == []:
                        break
    
                    last_elem = x.pop() 
                    new_bucket = [last_elem]  
                    new_bucket_sum = last_elem
    
                    num_added = 0
                    for num in x:
                        if num + new_bucket_sum > 5:
                            break
                        new_bucket.append(num) 
                        new_bucket_sum += num  
                        num_added += 1  
    
                    buckets.append(new_bucket) 
                    x = x[num_added:] 
                return buckets
    
            periods_sets = {}
            for capacity in capacity_set:
                periods_sets[capacity] = make_set_of_class(capacity)
    
            def need_to_change_room_set(capacity):
                room_in_need = math.ceil(len(periods_sets[capacity]) / 2)
                if room_in_need > len(classroom_set_by_capacity[capacity]):
                    return True
                return False
                
            def change_set_of_room_capacity(capacity):
                if need_to_change_room_set(capacity):
                    temp_change_class = periods_sets[capacity][-1]
                    set_of_class_by_capacity =  list(temp_course_code_set[capacity].keys())
                    
                    for course in set_of_class_by_capacity:
                        if temp_course_code_set[capacity][course]["numbers"] in temp_change_class:
                            temp_course_code_set[capacity_set[capacity_set.index(capacity) + 1]][course] = temp_course_code_set[capacity][course]
                            temp_course_code_set[capacity].pop(course)
                        
                    periods_sets[capacity_set[capacity_set.index(capacity) + 1]].append(temp_change_class)
                    periods_sets[capacity].remove(periods_sets[capacity][-1])
    
            for capacity in capacity_set:
                change_set_of_room_capacity(capacity)
    
            # study_time_set_no_language = {}
            cgroup_day_set = {}
            cgroup_room_set = {}
    
            def add_class_to_room(capacity):
                class_to_sort_set = temp_course_code_set[capacity]
                dynamic_class_to_sort_set = list(class_to_sort_set.keys())
                
                pers_set = periods_sets[capacity]
                
                if len(dynamic_class_to_sort_set) == 0:
                    pass
                else:
                    for i in range(len(pers_set)):
                        
                        room = room_to_use(capacity, "normal")
                        to_subtract = 0
                        
                        sorted_cgroup = []
                        length_pers_set = len(pers_set[i])
                        
                        for cgroup in dynamic_class_to_sort_set:
                            if class_to_sort_set[cgroup]["numbers"] in pers_set[i] and len(classroom_set[room]["used by"][i % 2 + 1]) < length_pers_set:
                                to_subtract += class_to_sort_set[cgroup]["numbers"]
                                classroom_set[room]["used by"][i % 2 + 1].append(class_to_sort_set[cgroup]["courses"])
                                classroom_set_of_cgroup[room]["used by"][i % 2 + 1].append(cgroup)
                                cgroup_room_set[cgroup] = room
                                cgroup_day_set[cgroup] =  i % 2 + 1
                                pers_set[i].remove(class_to_sort_set[cgroup]["numbers"])
                                sorted_cgroup.append(cgroup)
                                # study_day_set[room][i % 2 + 1].append(cgroup)
                            
                        if to_subtract > 0:
                            classroom_set[room]["session remain"] -= 1
                            
                        classroom_set[room]["available"] -= to_subtract
                        for cgroup in sorted_cgroup:
                            dynamic_class_to_sort_set.remove(cgroup)
                            
                    # set_of_class = []
                    # set_of_class.append(class_to_sort_set[cgroup])
                    # classroom_set[classroom]["used by"].append(course_to_sort_set[0])
                    # classroom_set[classroom]["available"] -= course_to_sort_set[0]["numbers"]
                    # course_to_sort_set.remove(course_to_sort_set[0])
                    
            for capacity in capacity_set:
                add_class_to_room(capacity)
            #-----------------------------------------------------------------------------#
    
            room_of_cgroup_set = {}
            for i, v in cgroup_room_set.items():
                room_of_cgroup_set[v] = [i] if v not in room_of_cgroup_set.keys() else room_of_cgroup_set[v] + [i]
    
            for room in classroom_set:
                if room not in room_of_cgroup_set:
                    room_of_cgroup_set[room] = []
                    
            study_time_set_language = {}
    
            japanese_course_set_norm = information.class_to_set_of_course(jap_course["normal"])
            germany_course_set = information.class_to_set_of_course(ger_course)
            english_course_set = information.class_to_set_of_course(eng_course)
    
            def get_unique_language_cgroup(language_set):
                
                unique= []
                current_cgroup = list(language_set.keys())
                temp_cgroup = [cgroup.split(" ")[0] for cgroup in language_set]
                for cgroup in temp_cgroup:
                    if cgroup not in unique:
                        unique.append(cgroup)
                return unique
    
            japanese_cgroup_set = get_unique_language_cgroup(japanese_course_set_norm)
            germany_cgroup_set = get_unique_language_cgroup(germany_course_set)
    
            def intersection(lst1, lst2):
                return list(set(lst1) & set(lst2))
    
            def change_classroom_set_for_language_course(room, language_set):
                
                # Tập hợp chứa các lớp học trong phòng
                cgroup_set_in_room = classroom_set_of_cgroup[room]["used by"][1] + classroom_set_of_cgroup[room]["used by"][2]
                # Tìm giao điểm của lớp học và tập lớp học ngoại ngữ
                overlap_cgroup = intersection(cgroup_set_in_room, language_set)
                # Nếu số lớp trùng lớn hơn hoặc bằng 2 sẽ phải thực hiện đổi phòng
                if len(overlap_cgroup) >= 2:
                    # Số phòng cần thêm để đổi bằng số phòng trùng - 1
                    room_need_more = len(overlap_cgroup) - 1
                    
            for room in classroom_set_of_cgroup:
                pass
    
            for room in classroom_set:
                for session in range(1, 3):
                    temp = []
                    for cgroup in classroom_set[room]["used by"][session]:
                        temp += cgroup
                    classroom_set[room]["used by"][session] = temp
    
            # Sort eng-course to evening slots
            for course in jap_course["evening"]:
                capacity_fit = information.fit_to_room(course)
                room_to_use_for_evening = room_to_use(capacity_fit, "evening")
                classroom_set[room_to_use_for_evening]["used by"][3].append(course)
                classroom_set[room_to_use_for_evening]["evening"] -= 3
                
            # Sort other language-course
    
            # Sort Japanese course
            temp_jap_set = {}
    
            for cgroup in japanese_course_set_norm:
                temp_jap_set[cgroup.split(" ")[0]] = 0
    
            for cgroup in japanese_course_set_norm:
                if cgroup not in temp_jap_set and cgroup.split(" ")[0] in temp_jap_set:
                    temp_jap_set[cgroup.split(" ")[0]] += 1
                elif cgroup in temp_jap_set:
                    temp_jap_set[cgroup] += 1
    
            temp_cgroup_of_japanese_course = list(temp_jap_set.keys())
            temp_of_japanese = []
                
            while len(temp_jap_set) > 0:
    
                temp_class = []
                temp_count = 0
                for cgroup in temp_cgroup_of_japanese_course:
                    if cgroup not in temp_jap_set:
                        continue
                    if temp_count + temp_jap_set[cgroup] <= 5:
                        temp_class.append(cgroup)
                        temp_count += temp_jap_set[cgroup]
                        del temp_jap_set[cgroup]
                temp_of_japanese.append(temp_class)
    
            room_can_use_for_japanese = [room for room in classroom_set_by_capacity[32] if classroom_set[room]["session remain"] > 1]
            room_nums_need_for_japanese = len(japanese_course_set_norm) 
            room_need_more_for_japanese = room_nums_need_for_japanese - len(room_can_use_for_japanese)
    
            room_can_use_in_45 = [room for room in classroom_set_by_capacity[45] if classroom_set[room]["session remain"] > 1]
            room_can_use_for_japanese += room_can_use_in_45[0:room_need_more_for_japanese]
    
            def get_studying_course_at_room(cgroup_set_list):
                room_set_of_cgroup = {}
                
                for cgroup_set in cgroup_set_list:
                    for cgroup in cgroup_set:
                        if cgroup in cgroup_room_set:
                            room_set_of_cgroup[cgroup_room_set[cgroup]] = {cgroup: cgroup_day_set[cgroup]}
                
                for cgroup in cgroup_room_set:
                    if cgroup_room_set[cgroup] in room_set_of_cgroup and cgroup not in room_set_of_cgroup[cgroup_room_set[cgroup]]:
                        room_set_of_cgroup[cgroup_room_set[cgroup]].update({cgroup: cgroup_day_set[cgroup]})
                
                return room_set_of_cgroup
    
            def change_session_day_cgroup(language_cgroup_set, cgroup_set_list):
                
                room_set_of_cgroup = get_studying_course_at_room(cgroup_set_list)
                
                for cgroup_set in list(room_set_of_cgroup.values()):
                    for cgroup in cgroup_set:
                        if cgroup.split(" ")[0] in cgroup_day_set and cgroup in language_cgroup_set:
                            temp = classroom_set[cgroup_room_set[cgroup]]["used by"][cgroup_day_set[cgroup]]
                            classroom_set[cgroup_room_set[cgroup]]["used by"][cgroup_day_set[cgroup]] = classroom_set[cgroup_room_set[cgroup]]["used by"][1]
                            classroom_set[cgroup_room_set[cgroup]]["used by"][1] = temp
                        
                        if cgroup in language_cgroup_set or cgroup_set[cgroup] == 1:
                            cgroup_set[cgroup] = 1
                            cgroup_day_set[cgroup] = 1
                        else:
                            cgroup_set[cgroup] = 2
                            cgroup_day_set[cgroup] = 2
                
            for cgroup_set in temp_of_japanese:
                change_session_day_cgroup(cgroup_set, temp_of_japanese)
                
            count_japanese_cgroup = len(japanese_course_set_norm)
                
            for cgroup in japanese_course_set_norm:
                classroom_set[room_can_use_for_japanese[list(japanese_course_set_norm.keys()).index(cgroup)]]["used by"][2] = [[course] for course in japanese_course_set_norm[cgroup]]
                classroom_set[room_can_use_for_japanese[list(japanese_course_set_norm.keys()).index(cgroup)]]["available"] -= 5
                classroom_set[room_can_use_for_japanese[list(japanese_course_set_norm.keys()).index(cgroup)]]["session remain"] -= 1
                classroom_set_of_cgroup[room_can_use_for_japanese[list(japanese_course_set_norm.keys()).index(cgroup)]]["used by"][2].append(cgroup)
            # Sort German course
            room_can_use_for_german = [room for room in classroom_set_by_capacity[50] if classroom_set[room]["session remain"] > 1] + \
                                        [room for room in classroom_set_by_capacity[60] if classroom_set[room]["session remain"] > 1] + \
                                        [room for room in classroom_set_by_capacity[84] if classroom_set[room]["session remain"] > 1]
            temp_german_course_set = {}
    
            res = {}
    
            temp_german_course_set = {7: [], 8: [], 12: []}
    
            for course in ger_course:
                create_check = [int(round(float(num))) for num in information.get_class_weight(course[0:3]).split("(")[1].split(")")[0].split("-")]
                check = create_check[0] + create_check[1]
                if check == 7:
                    temp_german_course_set[7].append(course)
                elif check == 8:
                    temp_german_course_set[8].append(course)
                elif check == 12:
                    temp_german_course_set[12].append(course)
                    
            for pers in temp_german_course_set:
                temp_german_course_set[pers] = information.class_to_set_of_course(temp_german_course_set[pers])
                
            room_for_german = {7: [], 8: [], 12:[]}
    
            room_nums_for_german_7 = int(np.ceil(len(temp_german_course_set[7]) * 0.3))
            room_nums_for_german_8 = int(np.ceil(len(temp_german_course_set[8]) * 0.4))
            room_nums_for_german_12 = int(np.ceil(len(temp_german_course_set[12]) * 0.6))
    
            room_for_german[7] = room_can_use_for_german[0: room_nums_for_german_7]
            room_for_german[8] = room_can_use_for_german[room_nums_for_german_7: room_nums_for_german_7 + room_nums_for_german_8]
            room_for_german[12] = room_can_use_for_german[room_nums_for_german_7 + room_nums_for_german_8: room_nums_for_german_7 + room_nums_for_german_8 + room_nums_for_german_12]
    
            temp_of_german = [list(temp_german_course_set[val].keys()) for val in temp_german_course_set]
            for cgroup_set in temp_of_german:
                unique = []
                for cgroup in cgroup_set:
                    if cgroup.split(" ")[0] not in unique:
                        unique.append(cgroup.split(" ")[0])
                temp_of_german[temp_of_german.index(cgroup_set)] = unique
                
            for cgroup_set in temp_of_german:
                change_session_day_cgroup(cgroup_set, temp_of_german)
    
            def sort_german(german_course_set, pers):
                
                if pers == 7:
                    room_7 = room_for_german[7]
                    course_7 = list(german_course_set[7].values())
                    cgroup_7 = list(german_course_set[7].keys())
                    
                    if len(room_7) == 1 and len(course_7) == 1:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0]], [course_7[0][1]]]
                        classroom_set[room_7[0]]["available"] -= 2
    
                    elif len(room_7) == 1 and len(course_7) == 2:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 3
    
                    elif len(room_7) == 1 and len(course_7) == 3:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0]], [course_7[0][1]], [course_7[1][1]], [course_7[2][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
    
                    elif len(room_7) == 2 and len(course_7) == 4:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[0][1]], [course_7[1][1]], [course_7[2][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 1
    
                    elif len(room_7) == 2 and len(course_7) == 5:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[0][1]], [course_7[1][1]], [course_7[2][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][0]], [course_7[4][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 3
    
                    elif len(room_7) == 2 and len(course_7) == 6:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[4][0], course_7[5][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][1]], [course_7[5][1]], [course_7[2][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 4
                    elif len(room_7) == 3 and len(course_7) == 7:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[4][0], course_7[5][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][1]], [course_7[5][1]], [course_7[6][0]], [course_7[2][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 5
                        classroom_set[room_7[2]]["used by"][2] = [[course_7[6][1]]]
                        classroom_set[room_7[2]]["available"] -= 1
                    elif len(room_7) == 3 and len(course_7) == 8:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[4][0], course_7[5][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][1]], [course_7[5][1]], [course_7[6][0], course_7[7][0]], [course_7[2][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 5
                        classroom_set[room_7[2]]["used by"][2] = [[course_7[6][1]], [course_7[7][1]]]
                        classroom_set[room_7[2]]["available"] -= 2 
                    elif len(room_7) == 3 and len(course_7) == 9:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[4][0], course_7[5][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][1]], [course_7[5][1]], [course_7[6][0], course_7[7][0]], [course_7[2][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 5
                        classroom_set[room_7[2]]["used by"][2] = [[course_7[6][1]], [course_7[7][1]], [course_7[8][0]], course_7[8][1]]
                        classroom_set[room_7[2]]["available"] -= 4
                    elif len(room_7) == 3 and len(course_7) == 10:
                        classroom_set[room_7[0]]["used by"][2] = [[course_7[0][0], course_7[1][0]], [course_7[2][0], course_7[3][0]], [course_7[4][0], course_7[5][0]], [course_7[0][1]], [course_7[1][1]]]
                        classroom_set[room_7[0]]["available"] -= 5
                        classroom_set[room_7[1]]["used by"][2] = [[course_7[4][1]], [course_7[5][1]], [course_7[6][0], course_7[7][0]], [course_7[2][1]], [course_7[3][1]]]
                        classroom_set[room_7[1]]["available"] -= 5
                        classroom_set[room_7[2]]["used by"][2] = [[course_7[6][1]], [course_7[7][1]], [course_7[8][0], course_7[9][0]], course_7[8][1], course_7[9][1]]
                        classroom_set[room_7[2]]["available"] -= 5
                        
                elif pers == 8:
                    room_8 = room_for_german[8]
                    course_8 = list(german_course_set[8].values())
                    cgroup_8 = list(german_course_set[8].keys())
                    temp_8 = []
                    for course_set in course_8:
                        for course in course_set:
                            temp_8.append(course)
                    
                    for i in range(len(temp_8)):
                        classroom_set[room_8[i // 5]]["used by"][2].append([temp_8[i]]) 
                        
                elif pers == 12:
                    room_12 = room_for_german[12]
                    course_12 = list(german_course_set[12].values())
                    cgroup_12 = list(german_course_set[12].keys())
                    
                    temp_12 = []
                    for course_set in course_12:
                        for course in course_set:
                            temp_12.append(course)
                    
                    for i in range(len(temp_12)):
                        classroom_set[room_12[i // 5]]["used by"][2].append([temp_12[i]]) 
                        
            for val in temp_german_course_set:
                sort_german(temp_german_course_set, val)
    
            course_code_set.update(jap_course["normal"])
            course_code_set.update(ger_course)
    
            #-----------------------------------------------------------------------------#
            study_time_set = {}
    
            for course in course_code_set:
                if len(information.get_participant_class(course)) == 1:
                    study_time_set[information.get_participant_class(course)[0]] = {i: 0 for i in range(1, 11)}
    
            # Sort English course
            room_can_use_for_eng = [room for room in classroom_set_by_capacity[32] if classroom_set[room]["available"] >= 1]
            cgroup_set = list(english_course_set.keys())
                
            def get_value_for_cgroup_in_study_time_set(cgroup):
                temp_pos = []
    
            for cgroup in study_time_set:
                pass
                
            def room_to_add_large_group(large_group):
                room_capacity_fit = information.fit_to_room(large_group)
                return room_to_use(room_capacity_fit)
    
            def add_large_group(large_group):
                room_in_use = room_to_add_large_group(large_group)
                pass
            #-----------------------------------------------------------------------------#
            study_day_set = {}
            for room in classroom_set:
                study_day_set[room] = {1: classroom_set[room]["used by"][1], 2: classroom_set[room]["used by"][2]}
    
            def get_learning_day_part(course_code):
    
                for room in study_day_set:
                    for session in range(1, 3):
                        for day in study_day_set[room][session]:
                            if course_code in day:
                                day_part = session
                if day_part == 1:
                    return "Sáng"
                elif day_part == 2:
                    return "Chiều"
                    
            def get_learning_day(course_code):
                
                for room in study_day_set:
                    for session in range(1, 3):
                        for day in study_day_set[room][session]:
                            if course_code in day:
                                study_day = study_day_set[room][session].index(day)
                if study_day == 0:
                    return 2
                if study_day == 1:
                    return 3
                if study_day == 2:
                    return 4
                if study_day == 3:
                    return 5
                if study_day == 4:
                    return 6
    
            def get_period(course_code, ptype):
                
                for room in study_day_set:
                    for session in range(1, 3):
                        for day in study_day_set[room][session]:
                            if course_code in day:
                                temp = day
                
                periods_set = [course_code_set[code] for code in temp]
                
                course_position = temp.index(course_code)
                
                before_length = []
                if course_position == 0:
                    before_length.append(periods_set[0])
                else:
                    before_length = periods_set[0:course_position]
                
                course_length = course_code_set[course_code]
                
                if course_position == 0:
                    start_period = 1
                else:
                    start_period = sum(before_length) + 1
                
                end_period = course_length - 1 + start_period
                
                if ptype == "end":
                    return end_period
                if ptype == "start":
                    return start_period
    
            def get_classroom_course_use(course_code):
                for room in study_day_set:
                    for day in range(1, 3):
                        for cgroup in study_day_set[room][day]:
                            if course_code in cgroup:
                                return room
                        
            def get_course_type(course_code):
                output_set = []
                temp = str(information.get_class_weight(course_code))
                if temp.isdigit():
                    return "LT+BT"
                else:
                    temp = temp.split("(")[1].split(")")[0].split("-")
                    if len(temp) < 2:
                        return "LT+BT"
                    else:
                        if temp[0] != 0:
                            output_set.append("LT")
                        if temp[1] != 0:
                            output_set.append("BT")
                return "+".join(output_set)
    
            def get_learn_time(course_code, start, end):
                return f"{time_set[get_learning_day_part(course_code)][start]['start']}-{time_set[get_learning_day_part(course_code)][end]['end']}"
    
            data = {}
            for course_code in course_code_set:
                start = get_period(course_code, "start")
                end = get_period(course_code, "end")
                data[course_code] = ["20221",
                                    information.get_school(course_code[0:3]),
                                    "139" + course_code[0:3],
                                    information.get_course_iden_code(course_code[0:3]),
                                    information.get_course_name(course_code[0:3]),
                                    information.get_class_weight(course_code[0:3]),
                                    information.course_note(course_code[0:3]),
                                    get_learning_day(course_code),
                                    get_learn_time(course_code, start, end),
                                    start,
                                    end, 
                                    get_learning_day_part(course_code),
                                    get_classroom_course_use(course_code),
                                    classroom.get_classroom_capacity(get_classroom_course_use(course_code)),
                                    information.get_student_number(course_code[0:3]),
                                    "Đang xếp TKB",
                                    get_course_type(course_code[0:3]),
                                    information.get_semester(course_code[0:3]),
                                    "SIE"]
    
            self.expected_timetable = pd.DataFrame.from_dict(data, orient='index',
                                                        columns=["Kỳ", "Trường", "Mã lớp", "Mã HP",
                                                                  "Tên HP", "Khối lượng", "Ghi chú", 
                                                                  "Thứ", "Thời gian", 
                                                                  "BĐ", "KT",
                                                                  "Kíp", "Phòng", "Sức chứa", "SL_Max", "Trạng thái", 
                                                                  "Loại lớp", "Kỳ học", "CTĐT"])
    
            end_time = time()
            running_time = end_time - start_time
            
        except Exception:
            messagebox.showerror(title="Lỗi", message="Tên file hoặc đường dẫn tới file không hợp lệ!")
            
    def get_classroom_from_interface(self):

        self.myClassroom = Classroom(self.filepath_entry.get("1.0",'end-1c'))
        
        return self.myClassroom
    
    def get_information_from_interface(self):
        
        self.myClassInformation = ClassInformation(self.filepath_entry.get("1.0",'end-1c'))
        
        return self.myClassInformation