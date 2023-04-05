# @Author :  NaveedMohammed
# @File   :  data_formatter.py

import pandas as pd
import numpy as np
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class DataFormatter:
    def __init__(self):
        self.prefs_offering_file = ''
        self.input_store_file = ''
        self.sessions_file = ''
        self.output_dir = ''
        self.offering_name = ''
        self.unit_name = ''
        self.app_name = ''
        self.output_store_file = ''
        self.prefs_file = ''
        self.offering_file = ''
        self.subjects_file = ''
        self.units_file = ''

        pref_columns = ['user', 'appName', 'key', 'value']
        self.prefDs = pd.DataFrame(data=np.zeros((0, len(pref_columns))), columns=pref_columns)
        subjects_columns = ['userName', 'subjectID']
        self.subjectsDs = pd.DataFrame(data=np.zeros((0, len(subjects_columns))), columns=subjects_columns)
        units_columns = ['name', 'offeringName', 'lessonName', 'appName']
        self.unitsDs = pd.DataFrame(data=np.zeros((0, len(units_columns))), columns=units_columns)
        offerings_columns = ['login', 'offering']
        self.offeringsDs = pd.DataFrame(data=np.zeros((0, len(offerings_columns))), columns=offerings_columns)
        store_columns = ['user', 'offeringName', 'appName', 'key', 'index', 'value']
        self.storeDs = pd.DataFrame(data=np.zeros((0, len(store_columns))), columns=store_columns)

        self.init_processing()

    def init_processing(self):
        """
        create a Tkinter window and add buttons.
        """
        root = Tk()
        root.geometry('300x400')
        root.resizable(False, False)
        root.title('Log Processor')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=0)
        root.rowconfigure(4, weight=0)
        root.rowconfigure(5, weight=0)

        # Labels for displaying the selected files to the user.
        store_label = Label(root, text="", height=2,
                            fg="blue", wraplength=300, justify="center")
        prefs_label = Label(root, text="", height=2,
                            fg="blue", wraplength=300, justify="center")
        sessions_label = Label(root, text="", height=2,
                               fg="blue", wraplength=300, justify="center")
        output_label = Label(root, text="", height=2,
                             fg="blue", wraplength=300, justify="center")

        def browse_files(filetype):
            """
            Functionality to open file explorer and select desired files and directory.
            :param filetype: String. possible options: ['store', 'prefs', 'sessions', 'output']
            """
            if filetype.__contains__("output"):
                filename = filedialog.askdirectory()
            else:
                filename = filedialog.askopenfilename(initialdir="", title="Select file",
                                                      filetypes=(
                                                          ("csv files", "*.csv"), ("all files", "*.*")))
            if filetype.__contains__("store"):
                store_label.configure(text="File opened: " + filename)
                self.input_store_file = filename
            elif filetype.__contains__("prefs"):
                prefs_label.configure(text="File opened: " + filename)
                self.prefs_offering_file = filename
            elif filetype.__contains__("sessions"):
                sessions_label.configure(text="File opened: " + filename)
                self.sessions_file = filename
            elif filetype.__contains__("output"):
                output_label.configure(text=filename)
                self.output_dir = filename
                self.setup_output_files(self.output_dir)

            if self.input_store_file and self.prefs_offering_file and self.sessions_file and self.output_dir:
                btn_process['state'] = NORMAL

        def process_data():
            """
            Take the input files and generate csv files required for BB analysis.
            Input files: Input store csv, prefs offering csv and sessions csv.
            Output files: Output store csv, Prefs csv, offering csv, sessions csv, subjects csv.
            """
            progress_bar.grid(column=0, row=10, padx=10, pady=20)
            if progress_bar['value'] < 100:
                progress_bar['value'] += 10
            self.generata_data_files(progress_bar)
            progress_bar.grid_remove()
            btn_process['state'] = DISABLED
            btn_result.grid(column=0, row=10)

        def open_file():
            location = output_label.cget("text")
            os.system('start ' + location)
            exit()

        # Buttons for importing and processing data.
        btn = Button(root, text='Import Store File', command=lambda: browse_files("store"), bd='5', width=20)
        btn_prefs = Button(root, text='Import prefs_offering File', command=lambda: browse_files("prefs"), bd='5',
                           width=20)
        btn_subjects = Button(root, text='Import sessions File', command=lambda: browse_files("sessions"), bd='5',
                              width=20)
        btn_output = Button(root, text='Set Output location', command=lambda: browse_files("output"), bd='5', width=20)
        btn_process = Button(root, text='Generate Data files', command=process_data, bd='5', width=20)
        btn_result = Button(root, text='Open Output folder', command=open_file, bd='5', width=20)

        progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, mode="determinate", length=280)

        btn.grid(column=0, row=0)
        store_label.grid(column=0, row=1)
        btn_prefs.grid(column=0, row=2)
        prefs_label.grid(column=0, row=3)
        btn_subjects.grid(column=0, row=4)
        sessions_label.grid(column=0, row=5)
        btn_output.grid(column=0, row=6)
        output_label.grid(column=0, row=7)
        ttk.Separator(root, orient=HORIZONTAL).grid(row=8,column=0,ipadx=200)
        btn_process.grid(column=0, row=9)
        btn_process['state'] = DISABLED

        root.mainloop()

    def generata_data_files(self, progress_bar):
        """
        Functionality to generate data files required for Bettys Bain Analysis based on the raw data
        collected in a Bettys Brain study.
        :return: csv files generated from input files and written to the selected directory.
        """
        # Reading prefs_offering csv file.
        prefs_offering_data = pd.read_csv(self.prefs_offering_file)
        user_list = prefs_offering_data['user'].tolist()
        offering_list = prefs_offering_data['offering'].tolist()
        app_list = prefs_offering_data['app'].tolist()
        key_list = prefs_offering_data['name'].tolist()
        value_list = prefs_offering_data['value'].tolist()

        # Reading store csv file
        store_data = pd.read_csv(self.input_store_file)
        self.unit_name = store_data.iloc[0, 2]
        self.offering_name = store_data.iloc[0, 1]
        self.app_name = store_data.iloc[0, 3]

        # Creating prefs csv file from raw prefs_offering_file
        # ['user', 'appName', 'key', 'value']
        self.prefDs['user'] = user_list
        self.prefDs['appName'] = app_list
        self.prefDs['key'] = key_list
        self.prefDs['value'] = value_list
        self.prefDs = self.prefDs.set_index('user')
        self.prefDs.to_csv(self.prefs_file, index='false', encoding='utf-8')
        if progress_bar['value'] < 100:
            progress_bar['value'] += 10

        # Creating offerings csv file from prefs_offering_file
        # ['login', 'offering']
        self.offeringsDs['login'] = user_list
        self.offeringsDs['offering'] = offering_list
        self.offeringsDs = self.offeringsDs.set_index('login')
        self.offeringsDs.to_csv(self.offering_file, index='false', encoding='utf-8')
        if progress_bar['value'] < 100:
            progress_bar['value'] += 20

        # Creating subjects csv file from prefs_offering_file
        # ['userName', 'subjectID']
        self.subjectsDs['userName'] = user_list
        self.subjectsDs['subjectID'] = user_list
        self.subjectsDs = self.subjectsDs.set_index('userName')
        self.subjectsDs.to_csv(self.subjects_file, index='false', encoding='utf-8')
        if progress_bar['value'] < 100:
            progress_bar['value'] += 20

        # Creating units csv file from raw_store file
        # ['name', 'offeringName', 'lessonName', 'appName']
        self.unitsDs.loc[0, 'name'] = self.unit_name
        self.unitsDs.loc[0, 'offeringName'] = self.offering_name
        self.unitsDs.loc[0, 'lessonName'] = self.unit_name
        self.unitsDs.loc[0, 'appName'] = self.app_name
        self.unitsDs = self.unitsDs.set_index('name')
        self.unitsDs.to_csv(self.units_file, index='false', encoding='utf-8')
        if progress_bar['value'] < 100:
            progress_bar['value'] += 20

        # Creating store csv file raw_store file
        # ['user', 'offeringName', 'appName', 'key', 'index', 'value']
        self.storeDs['user'] = store_data['user'].tolist()
        self.storeDs['offeringName'] = store_data['offering'].tolist()
        self.storeDs['appName'] = store_data['app'].tolist()
        self.storeDs['key'] = store_data['name'].tolist()
        self.storeDs['index'] = store_data['index'].tolist()
        self.storeDs['value'] = store_data['value'].tolist()
        self.storeDs = self.storeDs.set_index('user')
        output_store_filename = "store_" + self.offering_name + ".csv"
        self.output_store_file = os.path.join(self.output_store_file, output_store_filename)
        self.storeDs.to_csv(self.output_store_file, index='false', encoding='utf-8')
        if progress_bar['value'] < 100:
            progress_bar['value'] += 20

    def setup_output_files(self, output_location):
        """
        Method to set filenames based on the selected output location.
        :param output_location: Output directory to save the generated files.
        """
        self.prefs_file = os.path.join(output_location, 'prefs.csv')
        self.offering_file = os.path.join(output_location, 'offerings.csv')
        self.subjects_file = os.path.join(output_location, 'subjects.csv')
        self.units_file = os.path.join(output_location, 'units.csv')
        self.output_store_file = output_location


if __name__ == "__main__":
    data_formatter = DataFormatter()