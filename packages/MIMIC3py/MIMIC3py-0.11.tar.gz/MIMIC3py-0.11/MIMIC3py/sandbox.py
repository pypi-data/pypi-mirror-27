# Spiro Ganas
#
# A sandbox for me to use while playing around with the code.

import pandas as pd

import MIMIC3py.config
from MIMIC3py.load_to_pandas import load_mimic_to_pandas



FilesToLoad = [ 'ADMISSIONS',  # 12 MB
                'CALLOUT',  # 6.1 MB
                'CAREGIVERS',  # 199 KB
                #'CHARTEVENTS',  # 33 GB ------BIG!!!
                'CPTEVENTS',  # 56 MB
                #'DATETIMEEVENTS',  # 502 MB
                'DIAGNOSES_ICD',  # 19 MB
                'DRGCODES',  # 11 MB
                'D_CPT',  # 14 KB
                'D_ICD_DIAGNOSES',  # 1.4 KB
                'D_ICD_PROCEDURES',  # 305 KB
                'D_ITEMS',  # 933 KB
                'D_LABITEMS',  # 43 KB
                'ICUSTAYS',  # 6.1 MB
                #'INPUTEVENTS_CV',  # 2.3 GB ------BIG!!!
                #'INPUTEVENTS_MV',  # 931 MB
                #'LABEVENTS',  # 1.8GB ------BIG!!!
                #'MICROBIOLOGYEVENTS',  # 70 MB
                #'NOTEEVENTS',  # 3.8 GB  ------BIG!!!
                #'OUTPUTEVENTS',  # 379 MB
                'PATIENTS',  # 2.6 MB
                #'PRESCRIPTIONS',  # 735 MB
                #'PROCEDUREEVENTS_MV',  # 47 MB
                'PROCEDURES_ICD',  # 6.5 MB
                'SERVICES',  # 3.4 MB
                #'TRANSFERS',  # 24 MB
            ]



# I only want a couple data sets
FilesToLoad = [ 'ADMISSIONS',  # 12 MB
                'PATIENTS',  # 2.6 MB

            ]




MyDF = load_mimic_to_pandas(CSV_Folder_Location = MIMIC3.config.local_save_folder, CSV_List = FilesToLoad, gunzip=True)


# SUBJECT_ID is a unique key for the PATIENTS table, so I'm setting it as the index


# TODO:  This part of the code needs a lot of work
MyDF['PATIENTS'] = MyDF['PATIENTS'].set_index(["SUBJECT_ID"])

#print(MyDF['ADMISSIONS'].head())
#print()
#print(MyDF['PATIENTS'].head())




#x = MyDF['PATIENTS'].join(MyDF['ADMISSIONS'],  lsuffix="_Patients", rsuffix="_Admissions")



x=MyDF['ADMISSIONS']

print(list(x))
print()
print(x['SUBJECT_ID'].head())

print()

# count the number of addmissions by patient ID
print(x['SUBJECT_ID'].value_counts()[:10])















