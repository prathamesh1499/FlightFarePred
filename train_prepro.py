import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

train_data = pd.read_excel(r"C:\Users\prathu\Desktop\Flight Fare Pred\Data_Train.xlsx")
train_data.dropna(inplace = True)

train_data["Journey_day"] = pd.to_datetime(train_data["Date_of_Journey"], format="%d/%m/%Y").dt.day
train_data["Journey_month"] = pd.to_datetime(train_data["Date_of_Journey"], format = "%d/%m/%Y").dt.month
# Since we have converted Date_of_Journey column into integers, Now we can drop as it is of no use.
train_data.drop(["Date_of_Journey"], axis = 1, inplace = True)

# Extracting Hours and Minutes
train_data["Dep_hour"] = pd.to_datetime(train_data["Dep_Time"]).dt.hour
train_data["Dep_min"] = pd.to_datetime(train_data["Dep_Time"]).dt.minute
train_data.drop(["Dep_Time"], axis = 1, inplace = True)

train_data["Arrival_hour"] = pd.to_datetime(train_data.Arrival_Time).dt.hour
train_data["Arrival_min"] = pd.to_datetime(train_data.Arrival_Time).dt.minute
train_data.drop(["Arrival_Time"], axis = 1, inplace = True)

duration = list(train_data["Duration"])
duration_hours = []
duration_mins = []

for i in range(len(duration)):
    if len(duration[i].split()) != 2:    # Check if duration contains only hour or mins
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"   # Adds 0 minute
        else:
            duration[i] = "0h " + duration[i]           # Adds 0 hour

for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))    
    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))

train_data["Duration_hours"] = duration_hours
train_data["Duration_mins"] = duration_mins
train_data.drop(["Duration"], axis=1, inplace = True)

# onehot encoding
Airline = train_data[["Airline"]]
Airline = pd.get_dummies(Airline, drop_first= True)

Source = train_data[["Source"]]
Source = pd.get_dummies(Source, drop_first= True)

Destination = train_data[["Destination"]]
Destination = pd.get_dummies(Destination, drop_first = True)

train_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

# labelencode
train_data.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)

data_train = pd.concat([train_data, Airline, Source, Destination], axis = 1)
data_train.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
#print(data_train.head(), data_train.shape)

data_train.to_csv(r"C:\Users\prathu\Desktop\Flight Fare Pred\TrainPrePro.csv", index = False)