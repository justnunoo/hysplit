#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import *
import tkinter.font as font
from tkinter import filedialog
from selenium import webdriver
from urllib import request
import pandas as pd
from selenium.webdriver.support.ui import Select
import time
from tqdm import tqdm
import os
from tkinter import ttk
from retry import retry
from progressbar import ProgressBar, Bar, Percentage
import time


day = []
month = []
year = []
num_array = []
stringday = []
stringyear = []
stringmonth = []
week = ''
weeks = []
months = []
actual_date = []
header = ''
error = True


parent= os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
directory = r'\hysplit folder'
path = parent + directory
try:
    os.makedirs(path, exist_ok=True)
except:
    pass
destination = path + '\\first.txt'
final_location1 = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + r'\hysplit text file.txt'

def savelocation():
    global final_location
    final_location = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                 filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
open(destination, 'w').close()

try:
    #get date file location
    def browseFiles():
        global file_destination
        global location
        global second
        file_destination = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Excel files", "*.xlsx*"), ("all files", "*.*")))
        print("Excel file: " + file_destination)
        location = path + '\\Hysplit-dates.csv'
        second = path + '\\second.txt'


        excel = pd.read_excel(file_destination)
        excel.to_csv(location, index=0)
        file = pd.read_csv(location)
        text = str(file.to_numpy())
        text1 = text.replace('[', '')
        text2 = text1.replace(']', '')
        text3 = text2.replace('\'', '')
        text4 = text3.replace('-', ',')
        colist = text4.split('\n')

        openner = open(second, 'w')
        for lines in colist:
            openner.write(lines)
        openner.close()

        with open(second, 'r') as f:
            txt = f.read().replace(' ', ',')

        with open(second, 'w') as f:
            f.write(txt)

        with open(second, 'r') as f:
            txt = f.read().split(',')
            for lines in txt:
                num_array.append(lines)

        for r in range(0, len(num_array), 3):
            stringyear.append(num_array[r])

        for r in range(1, len(num_array), 3):
            stringmonth.append(num_array[r])

        for r in range(2, len(num_array), 3):
            stringday.append(num_array[r])

        for i in range(len(stringday)):
            t = int(stringday[i])
            day.append(t)

        for i in range(len(stringday)):
            t = int(stringyear[i])
            year.append(t)

        for i in range(len(stringday)):
            t = int(stringmonth[i])
            month.append(t)

        for m in day:
            if m >0 and m < 8:
                week = 'w1'
            elif m > 7 and m < 15:
                    week = 'w2'
            elif m > 14 and m < 22:
                    week = 'w3'
            elif m > 21 and m < 29:
                    week = 'w4'
            elif m > 28 and m < 32:
                    week = 'w5'
            else:
                print('day is invalid')
            weeks.append(week)

        for m in month:
            if m == 1:
                mon = 'jan'
            elif m == 2:
                mon = 'feb'
            elif m == 3:
                mon = 'mar'
            elif m == 4:
                mon = 'apr'
            elif m == 5:
                mon = 'may'
            elif m == 6:
                mon = 'jun'
            elif m == 7:
                mon = 'jul'
            elif m == 8:
                mon = 'aug'
            elif m == 9:
                mon = 'sep'
            elif m == 10:
                mon = 'oct'
            elif m == 11:
                mon = 'nov'
            elif m == 12:
                mon = 'dec'
            else: print('invalid month')
            months.append(mon)

        for x in range(len(day)):
            actual_date.append('gdas1.' + str(months[x]) + str(year[x]).replace('20', '') + '.' + str(weeks[x]))
except:
    pass

#this is to clear input to prevent redundancy
def clear():
    day.clear()
    month.clear()
    year.clear()
    num_array.clear()
    stringday.clear()
    stringyear.clear()
    stringmonth.clear
    weeks.clear()
    months.clear()
    actual_date.clear()
    os.remove(location)
    os.remove(second)

#window creation
root = Tk()
root.title('HYSPLIT TEXT FILE DOWNLOADER')
root.geometry('630x400')
root.resizable(0, 0)


#define font
my_fontstyle = font.Font(family='Times New Roman')
my_fontsize = font.Font(size=9)

#create sideframes
sideframe = Frame(root, width=260, height=430, bg='#BCC7C7')
sideframe.place(x=0, y=0)

#guidelines
guide = Label(root, text='This program is to collect HYSPLIT text data \nfrom the NOAA website. It will automatically \n'+
                         'compile all text files from different dates.\n All the user has to do is input the parameters,\n'+
                         'that is the location, starting time, duration and\n  choose the direction of trajectory for analysis.\n'+
                         'The dates in the excel date file to be selected\nmust be in the form \'day-month-year\'\n eg. \'18-12-20\'')
guide.place(x=5, y=5)

#latitude entry
latitude_val = StringVar(root)
lat = Label(root, text='Latitude')
lat.place(x=270, y=10)
latitude1 = Entry(root, textvariable=latitude_val)
latitude1.place(x=340, y=10)

#longitude entry
longitude_val = StringVar(root)
long = Label(root, text='longitude')
long.place(x=270, y=60)
longitude1 = Entry(root, textvariable=longitude_val)
longitude1.place(x=340, y=60)

#starting time for analysis
options = ['00', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22','23']
start_time_val = StringVar(root)
start_time_val.set(options[0])#default value

start_time_label = Label(root, text='Select starting time')
start_time_label.place(x=270, y=110)
start_time_menu = OptionMenu(root, start_time_val, *options)
start_time_menu.place(x=400, y=105)

#select duration
duration_val = StringVar(root)
duration_label = Label(root, text='Duration ')
duration_label.place(x=270, y=160)
duration_entry = Entry(root, textvariable=duration_val)
duration_entry.place(x=340, y=160)

#choose height
height_val = StringVar(root)
height_label = Label(root, text='Height')
height_label.place(x=410, y=220)
height_entry = Entry(root, textvariable=height_val)
height_entry.place(x=470, y=220)

#choose trajectory direction
direction_val = StringVar(root)
Radiobutton(root, text='Forward Trajectory', variable=direction_val, value='f').place(x=270, y=200)
Radiobutton(root, text='Backward Trajectory', variable=direction_val, value='b').place(x=270, y=240)


# wrap your function with the `retry` decorator
@retry(Exception, tries=5, delay=3)
#access longitude and latitude values
def trig():
    global latitude
    global longitude
    global duration
    global start_time
    global direction
    global height
    start_time = start_time_val.get()
    duration = duration_val.get()
    latitude = latitude_val.get()
    longitude = longitude_val.get()
    height = height_val.get()
    direction = direction_val.get()

    lat_xpath = '//*[@id="LatId"]'
    long_xpath = '//*[@id="LonId"]'
    next_xpath = '//*[@id="form1"]/div/center/input[2]'

    # opens URL in specified web browser; in case hysplit in chrome
    start = webdriver.Chrome(executable_path='C:\\chromedriver.exe')
    start.get('https://www.ready.noaa.gov/hypub-bin/trajasrc.pl')

    # enter the coordinates of the geographical location ie. longitude and latitude
    start.find_element_by_xpath(lat_xpath).send_keys(latitude)
    start.find_element_by_xpath(long_xpath).send_keys(longitude)
    start.find_element_by_xpath(next_xpath).click()
    
    #create progress bar
    with tqdm (total=len(day)) as pbar:
        for q in range(len(day)):
            # program selects date to use for study
            date_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table/tbody/tr[2]/td[2]/select'
            next1_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/center/input'
            select = Select(start.find_element_by_xpath(date_xpath))
            select.select_by_visible_text(actual_date[q])
            start.find_element_by_xpath(next1_xpath).click()

            # enter starting time
            start_time_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[2]/tbody/tr[1]/td[5]/select'
            select1 = Select(start.find_element_by_xpath(start_time_xpath))
            select1.select_by_visible_text(start_time)

            # enter starting day
            start_day_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[2]/tbody/tr[1]/td[4]/select'
            select2 = Select(start.find_element_by_xpath(start_day_xpath))
            if day[q] >= 0 and day[q] < 10:
                select2.select_by_visible_text('0' + str(day[q]))
            elif day[q] > 9 and day[q] < 32:
                select2.select_by_visible_text(str(day[q]))

            duration_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[2]/tbody/tr[3]/td[2]/input'
            element = start.find_element_by_xpath(duration_xpath)
            element.clear()
            element.send_keys(duration)

            height_xpath = '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[2]/tbody/tr[17]/td[2]/input'
            hgt = start.find_element_by_xpath(height_xpath)
            hgt.clear()
            hgt.send_keys(height)

            if direction == 'b':
                start.find_element_by_xpath(
                    '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[1]/tbody/tr[2]/td[2]/input').click()
            elif direction == 'f':
                start.find_element_by_xpath(
                    '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[1]/tbody/tr[1]/td[2]/input').click()
            else:
                start.find_element_by_xpath(
                    '//*[@id="page_center"]/table/tbody/tr/td/div[4]/form/div[2]/table[1]/tbody/tr[2]/td[2]/input').click()

            # request trajectory
            request_xpath = '//*[@id="bestTitle"]/div[2]/input'
            start.find_element_by_xpath(request_xpath).click()
            time.sleep(20)

            # get text file address
            href = start.find_element_by_link_text('Trajectory endpoints file.').get_attribute('href')
            text_url = 'https://www.ready.noaa.gov' + href[17:43]
            print(str(q+1) +'-'+ text_url)

            response = request.urlopen(text_url)
            pdfs = response.read()
            pdf_str = str(pdfs)
            liness = pdf_str.split('\\n')

            global header
            if q == 0:
                for line in liness[0:9]:
                    header = header + line + '\n'
            else:
                pass

            global destination
            op = open(destination, 'a')
            for line in liness[9:]:
                op.write(line + '\n')
            op.close()
            
            time.sleep(0.01)
            progress["value"] = q
            pbar.update(1)
            root.update()

            start.back()
            start.back()
    
    second_destination = path + '\\second.txt'
    second = open(second_destination, 'w')
    second.write(header + '\n')
    second.close()
    first = open(destination, 'r')
    second2 = open(second_destination, 'a')
    reade = str(first.read())
    read = reade.replace('\'', '')
    reader = read.split('\n')
    for lines in reader:
        if lines.strip('\n') != '':
            second2.write(lines + '\n')
    second2.close()

    second3 = open(second_destination, 'r')
    final = open(final_location, 'w')
    final_text = str(second3.read()).split('\n')
    for lines in final_text:
        if lines.strip('\n') != '':
            final.write(lines + '\n')

    start.quit()
    print('Done')

# wrap your function with the `retry` decorator
@retry(exceptions=(ConnectionError), tries=5, delay=3)
def trigger():
    trig()
        

progress = ttk.Progressbar(root, orient="horizontal", length=240, mode="determinate", maximum=len(day))
progress.place(x=5, y=300)
  
#creates a clear button
clear_button = Button(root, text='Clear', justify=CENTER, padx=20, command=clear)
clear_button.place(x=340, y=342)
    
#create date selection button
select_date_button = Button(root, text='select date file', justify=CENTER, padx=5, command=browseFiles)
select_date_button.place(x=270, y=300)

select_save_destination = Button(root, text='Save as text file', justify=CENTER, padx=5, command=savelocation)
select_save_destination.place(x=400, y=300)

#create start button
create_start_button = Button(root, text='start', justify=CENTER, padx=20, command=trigger)
create_start_button.place(x=540, y=300)

#create exit button
create_exit_button = Button(root, text='exit', justify=CENTER, padx=20, command=root.destroy)
create_exit_button.place(x=480, y=342)

root.mainloop()

