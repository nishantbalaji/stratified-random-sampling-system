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

# Remove the files from devices known to be invalid
for bad_device in invalid_devices:
    df.drop(df[df['AudioMothCode']  == bad_device].index, inplace=True)

# Remove the files with an invalid length
target_size = 46000000
df.drop(df[df['FileSize'] < target_size].index, inplace=True)

# All the possible hours that can be shown
all_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# Store the current position on the DataFrame.
hour_index = 0

# Create a DataFrame with the same columns to store the outputs
output = pandas.DataFrame(columns=df.columns)

# Repeat the random sampling for each device
for AudioMoth in AudioMothName:

    # Create a dictionary to store the indices of the all the recordings for every hour
    hours = {}

    # For all the files in this device, add it to the dictionary under the corresponding hour
    while df['AudioMothCode'].iloc[hour_index] == AudioMoth:

        # Record the current hour
        temp = str(df['StartDateTime'].iloc[hour_index])

        # If the value isnt the date string then skip it (or end the loop)
        if len(temp) < 13:
            if hour_index == len(df) - 1:
                break
            hour_index += 1
        else:
            curr_hour = int(temp[11:13])

        # If the hour isn't in the dictionary yet, add it
        if curr_hour not in hours:
            hours[curr_hour] = []

        # If the hour is in the dictionary, add the index of the current row to that hour's list
        if curr_hour in hours:
            hours[curr_hour].append(hour_index)

        # If the hour_index is at the end of the DataFrame, stop iterating
        if hour_index == len(df) - 1:
            break

        # Go to the next row
        hour_index += 1

    # Find the number of clips needed from each hour
    if len(hours) < 24 and len(hours) != 0:
        num_per_hour = int(24 / len(hours))
    else:
        num_per_hour = int(len(hours) / 24)
        if num_per_hour != 0:
            num_per_hour = int( 1 / num_per_hour)

    # Find the remaining number of clips needed
    extras = abs(len(hours) % 24)
    if num_per_hour == 24:
        extras = 0

    # Make a list of dictionarys holding the row data to add to the output file
    rows_list = []

    # For each hour, randomly pick the `num_per_hour` amount of
    # samples to use and add them to row_list
    for select_hour in hours:
        for i in range(num_per_hour):

            # Pick a random index in the hour's list
            random.seed()
            curr_list = hours[select_hour]
            rand_num = random.randint(0, len(curr_list)-1)

            # Add the data of the sample at this index to the dictionary, and
            # add the dictionary to the row_list.
            rowToAdd = {}
            for column in df.columns:
                rowToAdd[column] = df.iloc[curr_list[rand_num]][str(column)]
            rows_list.append(rowToAdd)

            # Remove the used sample from the list
            # curr_list.remove(curr_list[rand_num]);


    # If there are extra samples needed, randomly pick that many hours and
    # take a sample from each.
    for j in range(extras):

        # Pick a random hour
        random.seed()
        rand_choice = random.randint(0, len(hours)-1)

        # Get the list of that hour
        temp = list(hours.keys())
        key = temp[rand_choice]
        curr_list = hours[key]

        # Pick a random index in the hour's list
        random.seed()
        rand_num = random.randint(0, len(curr_list)-1)

        # Add the data of the sample at this index to the dictionary, and
        # add the dictionary to the row_list.
        rowToAdd = {}
        for column in df.columns:
            rowToAdd[column] = df.iloc[curr_list[rand_num]][str(column)]
        rows_list.append(rowToAdd)

        # Remove the used sample from the list
        #curr_list.remove(curr_list[rand_num]);

    # Create a temporary DataFrame from the rows_list, and then add it to the output DataFrame
    temp = pandas.DataFrame(rows_list)
    output = output.append(temp, ignore_index=True)

# Convert the DataFrame to a .csv file
output.to_csv('stratified_random_sample.csv', index=False)

print('Sample Completed!')
