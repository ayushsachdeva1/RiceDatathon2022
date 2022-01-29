import pandas as pd
import sys
import requests
import re
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import math

def read_input(url):
    df = pd.read_csv(url, skiprows = 2, header=None, sep = ' ')
    print(df.head())

def format_data(url):
    response = requests.get(url)
    lines = response.text.split("\n")
    trimmed_lines = []
    for line in lines:
        trimmedLine = re.sub("\s+", ' ', line)
        trimmed_lines.append(trimmedLine)
    
    useful_lines = trimmed_lines[2:1327]
    parsed_lines = []
    for line in useful_lines:
        count = 0
        parsed_line = ""
        for i in range(len(line)):
            if line[i] == ' ':
                count+=1
            if count == 8:
                parsed_line = line[:i]
                break
        parsed_lines.append(parsed_line)
    
    array = []
    for line in parsed_lines:
        split_line = line.split(' ')
        array.append(split_line)
    
    useful_array = []
    for entry in array:
        res = True
        for data_point in entry:
            if data_point == 'MM':
                res = False
        
        if res:
            useful_array.append(entry)

    
    df = pd.DataFrame(useful_array, columns = ['year', 'month', 'day', 'hour', 'minutes', 'wind direction', 'wind speed', 'wind gust'])

    df['Source'] = url[len(url) - 8: len(url) - 4]

    return df


def multiplot(df):
    i = 0
    m = Basemap(projection='cass', resolution='h', width=2E6, height=2E6, lat_0=28.71, lon_0=-90.917)
    m.bluemarble()
    KIKT_loc = m(-88.289, 28.521)
    plt.plot(KIKT_loc[0], KIKT_loc[1], 'ok', markersize=5, color='white')
    plt.text(KIKT_loc[0], KIKT_loc[1], 'KIKT', fontsize=12, color='white')
    KBQX_loc = m(-95.620, 28.314)
    plt.plot(KBQX_loc[0], KBQX_loc[1], 'ok', markersize=5, color='white')
    plt.text(KBQX_loc[0], KBQX_loc[1], 'KBQX', fontsize=12, color='white')
    KMIS_loc = m(-88.842, 29.296)
    plt.plot(KMIS_loc[0], KMIS_loc[1], 'ok', markersize=5, color='white')
    plt.text(KMIS_loc[0], KMIS_loc[1], 'KMIS', fontsize=12, color='white')
    locations = (KIKT_loc, KBQX_loc, KMIS_loc)
    while i < df.shape[0]:
        tranch = []
        tranch.append(i)
        tranch_date = (df.loc[i, 'month'], df.loc[i, 'day'], df.loc[i, 'year'], df.loc[i, 'hour'], df.loc[i, 'minutes'])
        flag = False
        while i+1 < df.shape[0] and (df.loc[i+1, 'month'], df.loc[i+1, 'day'], df.loc[i+1, 'year'], df.loc[i+1, 'hour'], df.loc[i+1, 'minutes']) == tranch_date:
            flag = True
            tranch.append(i+1)
            i = i + 1
        if flag == False:
            i = i + 1

        input_array = []
        colors = []
        color_mapping = {'KIKT': 'r', 'KBQX':(.996, .644, 0.0), 'KMIS': (.996,.996,0.0)}
        origin_mapping = {'KIKT': locations[0], 'KBQX': locations[1], 'KMIS': locations[2]}
        origin_input = [[], []]
        for index in tranch:
            anglestr = df.loc[index, 'wind direction']
            speedstr = df.loc[index, 'wind speed']

            angle = float(anglestr)
            speed = float(speedstr)

            x = speed * math.cos(math.radians(90 - angle))
            y = speed * math.sin(math.radians(90 - angle))
            input_array.append([x,y])
            colors.append(color_mapping[df.loc[index, 'Source']])
            origin_tuple = origin_mapping[df.loc[index, 'Source']]
            origin_input[0].append(origin_tuple[0])
            origin_input[1].append(origin_tuple[1])
        
        vector = np.array(input_array)
        origin = np.array(origin_input)

        current_arrow = plt.quiver(*origin, vector[:,0], vector[:,1], color=colors, scale=60)
        date = tranch_date[0] + "/" + tranch_date[1] + "/" + tranch_date[2] + " " + tranch_date[3] + ":" + tranch_date[4]
        current_time = plt.text(50,500000, date, fontsize = 14)
        plt.pause(.002)
        current_arrow.remove()
        current_time.remove()
    plt.close()


def initialize_background():
    m = Basemap(projection='cass', resolution='l', width=2E6, height=2E6, lat_0=28.71, lon_0=-90.917)
    m.bluemarble()
    KIKT_loc = m(-88.289, 28.521)
    plt.plot(KIKT_loc[0], KIKT_loc[1], 'ok', markersize=5, color='black')
    plt.text(KIKT_loc[0], KIKT_loc[1], 'KIKT', fontsize=12, color='black')
    KBQX_loc = m(-95.620, 28.314)
    plt.plot(KBQX_loc[0], KBQX_loc[1], 'ok', markersize=5, color='black')
    plt.text(KBQX_loc[0], KBQX_loc[1], 'KBQX', fontsize=12, color='black')
    KMIS_loc = m(-88.842, 29.296)
    plt.plot(KMIS_loc[0], KMIS_loc[1], 'ok', markersize=5, color='black')
    plt.text(KMIS_loc[0], KMIS_loc[1], 'KMIS', fontsize=12, color='black')
    return KIKT_loc, KBQX_loc, KMIS_loc

    


def main():
    urlKIKT = "https://www.ndbc.noaa.gov/data/realtime2/KIKT.txt"
    urlKAPT = "https://www.ndbc.noaa.gov/data/realtime2/KBQX.txt"
    urlKMIS = "https://www.ndbc.noaa.gov/data/realtime2/KMIS.txt"
    kikt_data = format_data(urlKIKT)
    kapt_data = format_data(urlKAPT)
    kmis_data = format_data(urlKMIS)

    result = pd.concat([kikt_data,kapt_data,kmis_data], ignore_index=True)
    result.sort_values(by=['year', 'month', 'day', 'hour', 'minutes'], inplace=True, ignore_index=True)
    result.reindex()
    multiplot(result)
    
def print_formatted_data(data):
    print(data)

if __name__ == '__main__':
    main()
