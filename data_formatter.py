# @Author :  NaveedMohammed
# @File   :  data_formatter.py

import pandas as pd
import numpy as np
import os


class DataFormatter:
    def __init__(self, directory):
        self.prefs_offering_file = "D:/betty's stuff/Raw Betty's Brain data in csv/Raw data in csv/prefs.csv"
        self.input_store_file = "D:/betty's stuff/Raw Betty's Brain data in csv/Raw data in " \
                                "csv/store-offering1-20170313_200314-March_2017.csv"
        self.offering_name = ''
        self.unit_name = ''
        self.app_name = ''
        self.output_store_file = ""
        self.prefs_file = os.path.join(directory, 'prefs.csv')
        self.offering_file = os.path.join(directory, 'offerings.csv')
        self.sessions_file = ''
        self.subjects_file = os.path.join(directory, 'subjects.csv')
        self.units_file = os.path.join(directory, 'units.csv')

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
        self.generata_data_files()

    def generata_data_files(self):
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

        # Creating offerings csv file from prefs_offering_file
        # ['login', 'offering']
        self.offeringsDs['login'] = user_list
        self.offeringsDs['offering'] = offering_list
        self.offeringsDs = self.offeringsDs.set_index('login')
        self.offeringsDs.to_csv(self.offering_file, index='false', encoding='utf-8')

        # Creating subjects csv file from prefs_offering_file
        # ['userName', 'subjectID']
        self.subjectsDs['userName'] = user_list
        self.subjectsDs['subjectID'] = user_list
        self.subjectsDs = self.subjectsDs.set_index('userName')
        self.subjectsDs.to_csv(self.subjects_file, index='false', encoding='utf-8')

        # Creating units csv file from raw_store file
        # ['name', 'offeringName', 'lessonName', 'appName']
        self.unitsDs.loc[0, 'name'] = self.unit_name
        self.unitsDs.loc[0, 'offeringName'] = self.offering_name
        self.unitsDs.loc[0, 'lessonName'] = self.unit_name
        self.unitsDs.loc[0, 'appName'] = self.app_name
        self.unitsDs = self.unitsDs.set_index('name')
        self.unitsDs.to_csv(self.units_file, index='false', encoding='utf-8')

        # Creating store csv file raw_store file
        # ['user', 'offeringName', 'appName', 'key', 'index', 'value']
        self.storeDs['user'] = store_data['user'].tolist()
        self.storeDs['offeringName'] = store_data['offering'].tolist()
        self.storeDs['appName'] = store_data['app'].tolist()
        self.storeDs['key'] = store_data['name'].tolist()
        self.storeDs['index'] = store_data['index'].tolist()
        self.storeDs['value'] = store_data['value'].tolist()
        self.storeDs = self.storeDs.set_index('user')
        self.output_store_file = "store_" + self.offering_name + ".csv"
        self.storeDs.to_csv(self.output_store_file, index='false', encoding='utf-8')


if __name__ == "__main__":
    out_directory = os.getcwd()
    data_formatter = DataFormatter(out_directory)