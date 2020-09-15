import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

test_data = pd.read_excel(r"C:\Users\prathu\Desktop\Flight Fare Pred\Test_set.xlsx")
test_data.dropna(inplace = True)

test_data["Journey_day"] = pd.to_datetime(test_data["Date_of_Journey"], format="%d/%m/%Y").dt.day
test_data["Journey_month"] = pd.to_datetime(test_data["Date_of_Journey"], format = "%d/%m/%Y").dt.month
# Since we have converted Date_of_Journey column into integers, Now we can drop as it is of no use.
test_data.drop(["Date_of_Journey"], axis = 1, inplace = True)

# Extracting Hours and Minutes
test_data["Dep_hour"] = pd.to_datetime(test_data["Dep_Time"]).dt.hour
test_data["Dep_min"] = pd.to_datetime(test_data["Dep_Time"]).dt.minute
test_data.drop(["Dep_Time"], axis = 1, inplace = True)

test_data["Arrival_hour"] = pd.to_datetime(test_data.Arrival_Time).dt.hour
test_data["Arrival_min"] = pd.to_datetime(test_data.Arrival_Time).dt.minute
test_data.drop(["Arrival_Time"], axis = 1, inplace = True)

duration = list(test_data["Duration"])
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

test_data["Duration_hours"] = duration_hours
test_data["Duration_mins"] = duration_mins
test_data.drop(["Duration"], axis=1, inplace = True)

# onehot encoding
Airline = test_data[["Airline"]]
Airline = pd.get_dummies(Airline, drop_first= True)

Source = test_data[["Source"]]
Source = pd.get_dummies(Source, drop_first= True)

Destination = test_data[["Destination"]]
Destination = pd.get_dummies(Destination, drop_first = True)

test_data.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

# labelencode
test_data.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)

data_test = pd.concat([test_data, Airline, Source, Destination], axis = 1)
data_test.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)
#print(data_test.head(), data_test.shape)

data_test.to_csv(r"C:\Users\prathu\Desktop\Flight Fare Pred\TestPrePro.csv", index = False)