
import pandas as pd
from glob import glob

#--------------------------------------
# Read single CSV file
#--------------------------------------
single_file_acc = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")


single_file_gyro = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")


#--------------------------------------
# List all data in data/raw/MetaMotion
#--------------------------------------
files = glob("../../data/raw/MetaMotion\\*.csv")
print(files)
len(files)


#--------------------------------------
# Extract features from filename
#--------------------------------------

#--------------------------------------------------
''' 
I.Alternate method
import os

Assuming 'f' is the full path string
f = "../../data/raw/MetaMotion/A-bench-heavy2.csv"

# 1. Get just the filename (e.g., 'A-bench-heavy2.csv')
filename = os.path.basename(f)
#filename = A-bench-heavy2.csv

when splitted by hyphen, it will give
['A', 'bench', 'heavy2.csv'] and they are indexed as 0, 1, 2 respectively

# 2. Split by hyphen and take the first part ('A')
participant_id = filename.split("-")[0]
print(participant_id)

label = filename.split("-")[1]
print(label)

category = filename.split("-")[2].rstrip("123.csv")
print(category)

#-----------------------------------------------------------
'''

data_path = "../../data/raw/MetaMotion\\"
f = files[0]

participant = f.split("-")[0].replace(data_path, "")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123")
print(participant, label, category)
df = pd.read_csv(f)
df["participant"] = participant
df["label"] = label
df["category"] = category
print(df)


#--------------------------------------
# Read all files
#-------------------------------------
acc_df = pd.DataFrame()
gyro_df = pd.DataFrame()

acc_set = 1
gyro_set = 1

for f in files:
    participant = f.split("-")[0].replace(data_path, "")
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123_MetaWear_2019")
    df = pd.read_csv(f)
    
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    
    if "Accelerometer" in f:
        df["set"] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df], ignore_index=True)
    elif "Gyroscope" in f:
        df["set"] = gyro_set
        gyro_set += 1
        gyro_df = pd.concat([gyro_df, df], ignore_index=True)
#gyro_df[gyro_df["set"] == 1]
'''
-> The sets are like first set in accelerometer is the first csv file that has accelerometer in the list of files.the second set is the second csv file that has accelerometer in the list of files and so on. The same applies to gyroscope data.      
-> These help to identify which acts as unique identifier rather than using the participant, label, and category columns which are not unique. The set column is unique for each accelerometer and gyroscope data.
'''

#--------------------------------------
# Working with datetimes
#--------------------------------------
acc_df.info()

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"],unit ='ms')
gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"],unit ='ms')
del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

del gyro_df["epoch (ms)"]
del gyro_df["time (01:00)"]
del gyro_df["elapsed (s)"]
#--------------------------------------
# Turn into function
#--------------------------------------
def read_all_files(files):
    acc_df = pd.DataFrame()
    gyro_df = pd.DataFrame()

    acc_set = 1
    gyro_set = 1

    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123_MetaWear_2019")
        df = pd.read_csv(f)
        
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], ignore_index=True)
        elif "Gyroscope" in f:
            df["set"] = gyro_set
            gyro_set += 1
            gyro_df = pd.concat([gyro_df, df], ignore_index=True)
        acc_df.index = pd.to_datetime(acc_df["epoch (ms)"],unit ='ms')
    gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"],unit ='ms')
    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyro_df["epoch (ms)"]
    del gyro_df["time (01:00)"]
    del gyro_df["elapsed (s)"]
    
    return acc_df, gyro_df
acc_df, gyro_df = read_all_files(files)
#--------------------------------------
# Merging datasets
#--------------------------------------
data_merged = pd.concat([acc_df.iloc[:,:3], gyro_df], axis=1)

data_merged.columns = ['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'participant', 'label', 'category', 'set'] 
#--------------------------------------
# Resample data (frequency conversion)
#--------------------------------------



# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

sampling = {
    'acc_x': 'mean',
    'acc_y': 'mean',
    'acc_z': 'mean',
    'gyro_x': 'mean',
    'gyro_y': 'mean',
    'gyro_z': 'mean',
    'participant': 'last',
    'label': 'last',
    'category': 'last',
    'set': 'last'
    }

data_merged[:1000].resample(rule="200ms").apply(sampling)

days = [g for n, g in data_merged.groupby(pd.Grouper(freq='D'))]
data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])

data_resampled.info()

data_resampled["set"] = data_resampled["set"].astype(int)
#--------------------------------------
# Export dataset
#--------------------------------------
data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")



# %%



