import pandas as pd
import sys
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
import math

def read_input(url):
    df = pd.read_csv(url, skiprows = 2, header=None, sep = ' ')
    print(df.head())

def format_data(url):
    response = requests.get(url)
    # print(response.text)
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

            


    return df

def plot(df):
    plt.ion()
    for i in reversed(range(df.shape[0])):


        anglestr = df.loc[i, 'wind direction']
        speedstr = df.loc[i, 'wind speed']

        angle = float(anglestr)
        speed = float(speedstr)
        
        x = speed * math.cos(math.radians(90 - angle))
        y = speed * math.sin(math.radians(90 - angle))

        vector  = np.array([[x,y]])
        origin = np.array([[0], [0]])
        plt.quiver(*origin, vector[:,0], vector[:,1], color = ['r'], scale=21)
        plt.draw()
        date = df.loc[i, 'month'] + "/" + df.loc[i, 'day'] + "/" + df.loc[i, 'year'] + " " + df.loc[i, 'hour'] + ":" + df.loc[i, 'minutes']
        plt.text(-0.04, 0.04, date, fontsize = 14)
        plt.pause(0.02)

        plt.clf()






    


def main():
    urlKIKT = "https://www.ndbc.noaa.gov/data/realtime2/KIKT.txt"
    kikt_data = format_data(urlKIKT)
    # print_formatted_data(kikt_data)
    plot(kikt_data)
    




def print_formatted_data(data):
    print(data)



if __name__ == '__main__':
    main()
