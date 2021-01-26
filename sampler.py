import pandas
import numpy
import random

# Read the .csv file and parse it into a DataFrame
df = pandas.read_csv('Peru_2019_AudioMoth_Data_Full.csv')

# Get an array of the AudioMoth device names found in the .csv file
AudioMothName = df.drop_duplicates(subset=['AudioMothCode']).loc[:,'AudioMothCode'].values
# Devices that were known to have issues
invalid_devices = ['AM-8', 'AM-19', 'AM-21', 'AM-28']
# Find the devices that are not invalid in the array and add them to a temp array
temp_list = []
for device in AudioMothName:
    if device not in list(invalid_devices):
        temp_list.append(device)
# Set the temp array to the original array
AudioMothName = temp_list

for bad_device in invalid_devices:
    df.drop(df[df['AudioMothCode']  == bad_device].index, inplace=True)

# Remove the files with an invalid length.
target_size = 46080360
df.drop(df[df['FileSize'] < target_size].index, inplace=True)



#########################################################################################################################################################

''' make a list of starting hours for each audiomoth device. then count the number of unique hours in each device. divide the hours by 24 (should be 1 per hour if there are  24 hours, more if not. store remainder in a new value (x) and pick a random x number of hours to pick an extra value from) and store to (num) and go through each hour and randomly choose (num) elements to add to the list. repeat for each hour in the day, for each device'''

all_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

output = pandas.DataFrame(columns=df.columns)


hour_index = 0

for AudioMoth in AudioMothName:

    hours = {}
    start_hour = int((df['StartDateTime'].iloc[hour_index])[11:13])
    starting_index = all_hours.index(int(start_hour))



    while df['AudioMothCode'].iloc[hour_index] == AudioMoth:

        curr_hour_item = df['StartDateTime'].iloc[hour_index]
        curr_hour = int(curr_hour_item[11:13])
        if curr_hour not in hours:
            hours[curr_hour] = []

        if curr_hour in hours:
            hours[curr_hour].append(hour_index)
        if hour_index == len(df) -1:
            break
        hour_index += 1



    num_per_hour = int(len(hours) / 24)
    if num_per_hour != 0:
        num_per_hour = int(1/num_per_hour)
    extras = abs(len(hours) % 24)


    rows_list = []


    for select_hour in hours:
        for i in range(num_per_hour):
            random.seed()
            curr_list = hours[select_hour]

            rand_num = random.randint(0, len(curr_list)-1)

            rowToAdd = {}
            for column in df.columns:
                rowToAdd[column] = df.iloc[curr_list[rand_num]][str(column)]

            rows_list.append(rowToAdd)

            curr_list.remove(curr_list[rand_num]);



    for j in range(extras):
        random.seed()
        rand_choice = random.randint(0, len(hours)-1)

        random.seed()

        temp = list(hours.keys())
        key = temp[rand_choice]
        curr_list = hours[key]

        rand_num = random.randint(0, len(curr_list)-1)
        rowToAdd = {}

        for column in df.columns:
            rowToAdd[column] = df.iloc[curr_list[rand_num]][str(column)]
        rows_list.append(rowToAdd)
        curr_list.remove(curr_list[rand_num]);


    temp = pandas.DataFrame(rows_list)

    output = output.append(temp, ignore_index=True)


df.to_csv('stratified_random_sample.csv', index=False)
