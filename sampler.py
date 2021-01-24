import pandas
import numpy

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
print(AudioMothName)



# Remove the files with an invalid length.
target_size = 46080360
df.drop(df[df['FileSize'] < target_size].index, inplace=True)

print(df)

hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

''' make a list of starting hours for each audiomoth device. then count the number of unique hours in each device. divide the hours by 24 (should be 1 per hour if there are  24 hours, more if not. store remainder in a new value (x) and pick a random x number of hours to pick an extra value from) and store to (num) and go through each hour and randomly choose (num) elements to add to the list. repeat for each hour in the day, for each device'''


output = pandas.DataFrame()

# i = 2849
#
# AudioMoth = "AM-1"
#
# hours = {}
#
# for start_hour in df['StartDateTime'] and df['AudioMothCode'].iloc[start_hour.index] == AudioMoth:
#     print("hi")




# For each AudioMoth device
# for AudioMoth in AudioMothName:
    # hour_dict = {}
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # while df['AudioMothCode'].iloc[i] == AudioMoth:
    #     for value in df['StartDateTime']:
    #         if value == "NA":
    #             continue;
    #         current_hour = value[11:13]
    #         if current_hour not in list(hour_dict):
    #             hour_dict[value[11:13]] = [];
    #     print(i)
    #     i += 1
    #
    # print(hour_dict)
    # num = len(hour_dict) / 24
    # rem = len(hour_dict) % 24
    # break
#for

# '''for i in range(len(device_names)):
#     print(device_names[i])
#
# A = df['Artist'].values.ravel()
# print(A)'''

#print(df)
