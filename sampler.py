import pandas
import numpy

df = pandas.read_csv('Peru_2019_AudioMoth_Data_Full.csv')

target_size = 46080360
device_names = []
invalid_devices = ['AM-8', 'AM-19', 'AM-21', 'AM-28']
i = 0

for AudioMothName in df["AudioMothCode"]:
    if AudioMothName not in device_names and AudioMothName not in invalid_devices:
        device_names.append(AudioMothName)



drop_rows = []
total_size = 0
for size in df['FileSize'] and :
    if int(size) < int(target_size) and i not in drop_rows:
        print(i)
        drop_rows.append(i)
    if
    i+=1



df = df.drop(drop_rows)
df = df.drop_duplicates()
print(drop_rows)
print(df)

'''for i in range(len(device_names)):
    print(device_names[i])

A = df['Artist'].values.ravel()
print(A)'''

#print(df)
