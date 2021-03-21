---
title: "Creating a Dynamic 8-Bit Wallpaper for Linux with Python"
date: '2018-11-27'
excerpt: "Your desktop wallpaper may be the one image that you see most often in a given day so its probably worth your time to make it look the best it can. In this post, I offer a template for a dynmically-changing 8-Bit wallpaper which automatically syncs itself to sunrise and sunset times, produced using Python and compatible with Linux."
thumbnail: /gallery/thumbnails/dynamic-wallpaper.jpg
toc: true
categories:
- [System]
tags:
- linux
- python
- r
- data-mining
---
Recently, whilst browsing Reddit, I came across an old thread on [r/wallpapers](https://www.reddit.com/r/wallpapers/) showcasing a collection of 8-bit desktop wallpapers each of which displaying a beautiful landscape at a different time of day. The thread linked to the following [Imgur gallery](https://imgur.com/a/VZ9H2) containing all of the images.
![The 8-Bit wallpaper for late evening](/images/dynamic-wallpaper/Late-Evening.png)
These images by themselves have little use but over the next few years several contributors had grouped together, using these wallpapers, to produce a live wallpaper for android, an integration with Windows and OSX, and a web implementation. Yet the Linux community were not getting much love from the project. 

There are a few scripts kicking around on Github allowing users to manually set up a live version of the wallpaper but these all seem to use fixed time intervals to determine when to change the wallpaper and so in the summer and winter when the time the sun is up is far from the average value, the wallpaper is completely asynchronous to real life. What I wished to do was to set up an implementation for Linux which would use local sunrise and sunset times to adjust when the wallpaper changes to result in an experience that perfectly matches up with the real world.

I used data from the [UK Hydrographic Office](http://astro.ukho.gov.uk/surfbin/first_beta.cgi), a website offering free astronomical data for anybody to use. Using this site you can generate a text file containing the sunrise and sunset times for any location in the United Kingdom (with daylight savings already accounted for). I retrieved this data for the entirety of 2018. If you wanted complete accuracy this would need to be updated each year but with the annual difference of the sunrise/set times being in the handfuls of minutes, I don't think this is necessary.

This data comes in a very messy format and so I had to perform some cleaning with R:
{% codeblock lang:R %}
# required libraries
library(dplyr)
library(magrittr)
library(tidyr)

# extract data on months January to June
first_months <- read_table("rise_set_times.txt", 
                           skip = 7,
                           n_max = 37, 
                           col_names = FALSE) %>%
  # remove any row that is just NAs
  filter_all(any_vars(!is.na(.))) %>%
  # replace blank values with NAs
  mutate_all(funs(replace(., . == "", NA)))

# extract data on months July to December
last_months <- read_table("rise_set_times.txt", 
                           skip = 65,
                           n_max = 37, 
                           col_names = FALSE) %>%
  filter_all(any_vars(!is.na(.))) %>%
  # remove duplicate day column
  select(-1) %>%
  mutate_all(funs(replace(., . == "", NA)))

# combine all months
all_months <- bind_cols(first_months, last_months) %>%
  # convert all variables to integers after removing leading whitespace
  mutate_all(funs(as.integer(str_remove(., "$\\s"))))

# combine sunset and sunrise times (and hours and minutes) for gathering
for (i in 1:12) {
  all_months %<>% unite(col = !! i, !! {i + 1:4}, sep = " | ")
}

all_months %<>% rename(Day = X1)

# gather months into its own column
all_months %<>% gather("Month", "Set_Rise_Times", -Day)

# reorder columns
all_months %<>% .[c(2,1,3)]

# split sunset and sunrise times into two variables each (hours and minutes)
all_months %<>% separate(Set_Rise_Times, 
                         into = c("Rise_Hour", "Rise_Minute", 
                                  "Set_Hour", "Set_Minute"), 
                         convert = TRUE)

# output cleaned data as CSV
write_csv(all_months, "processed_times.csv")
{% endcodeblock %}


Cleaning this data is much easier in R than Python, yet to keep this blog post self-contained for anyone familiar with just the basic use of Python, I have packaged this code up into a Shiny web app which can be viewed [here](https://timhargreaves.shinyapps.io/SunsetAndSunriseTimeFileConverter/). Providing you collect the data from the source above using the same settings, you will be able to upload the returned text file to this web app and it will automatically clean the data for you and provide you with a CSV file to download.
![Screenshot of Shiny web app for processing and converting the time files](/images/dynamic-wallpaper/Converter.png)
Once your data is clean you can start setting up the wallpaper. You will first need Python 3 installed on your computer. You can then create a folder somewhere in your file system to contain the files relevant to this project. In this folder, you will need to download the images from the Imgur link and add the cleaned CSV file containing the sunset and sunrise times. You then need to copy any one of the wallpapers and rename it to `current.png`. The choice of wallpaper to copy makes no difference as it will be overridden when the wallpaper is updated. Next you need to create a Python script in this folder containing the following code with the blanks filled in:
{% codeblock lang:Python %}
#!/usr/bin/env python

import datetime
import os
import shutil
import pandas as pd
import numpy as np

# set the PATH to the location of the folder containing
# the wallpapers and sunrise/set times
PATH = 				"______"

# the filename of the current wallpapr
CURRENT = 			"current.png"

# the filename of the cleaned sunrise/set CSV file
time_data =         "______"
# the filenames of the wallpapers (e.g "early_morning.png")
early_morning = 	"______"
mid_morning = 		"______"
late_morning = 		"______"
early_afternoon =   "______"
mid_afternoon = 	"______"
late_afternoon = 	"______"
early_evening = 	"______"
mid_evening = 		"______"
late_evening = 		"______"
early_night = 		"______"
mid_night = 		"______"
late_night = 		"______"
# load sunrise/set times data
rise_set_times = pd.read_csv(PATH + "processed_times.csv")
# current datetime
month = datetime.datetime.now().month
day = datetime.datetime.now().day
hour = float(datetime.datetime.now().hour)
min = float(datetime.datetime.now().minute)
# time as a fraction of the day
time_frac = (hour + min / 60) / 24
# extract sunrise and sunset times for the particular day
day_times = rise_set_times.loc[(rise_set_times['Month'] == month) 
                                & (rise_set_times['Day'] == 5)]
# extract sunrise time
rise_hour = day_times.values[0, 2]
rise_min = day_times.values[0, 3]
# convert to fraction of the day
rise_frac = (rise_hour + rise_min / 60) / 24
# extract sunset time
set_hour = day_times.values[0, 4]
set_min = day_times.values[0, 5]
# convert to fraction of the day
set_frac = (set_hour + set_min / 60) / 24
# split day into intervals based on sunrise/set times
day_change_times = np.linspace(rise_frac, set_frac, 10)
# split night into intervals based on sunrise/set times
night_change_times = np.linspace(set_frac, rise_frac + 1, 4) % 1
# combine day and night times
change_times = np.append(day_change_times, night_change_times[1])
change_times = np.insert(change_times, 0, night_change_times[2])

# decide on the new wallpaper based on the current time of the day
if  time_frac <= change_times[0]:
    shutil.copy(PATH + mid_night, PATH + CURRENT)

elif time_frac <= change_times[1]:
    shutil.copy(PATH + late_night, PATH + CURRENT)

elif time_frac <= change_times[2]:
    shutil.copy(PATH + early_morning, PATH + CURRENT)

elif time_frac <= change_times[3]:
    shutil.copy(PATH + mid_morning, PATH + CURRENT)

elif time_frac <= change_times[4]:
    shutil.copy(PATH + late_morning, PATH + CURRENT)

elif time_frac <= change_times[5]:
    shutil.copy(PATH + early_afternoon, PATH + CURRENT)

elif time_frac <= change_times[6]:
    shutil.copy(PATH + mid_afternoon, PATH + CURRENT)

elif time_frac <= change_times[7]:
    shutil.copy(PATH + late_afternoon, PATH + CURRENT)

elif time_frac <= change_times[8]:
    shutil.copy(PATH + early_evening, PATH + CURRENT)

elif time_frac <= change_times[9]:
    shutil.copy(PATH + mid_evening, PATH + CURRENT)

elif time_frac <= change_times[10]:
    shutil.copy(PATH + late_evening, PATH + CURRENT)

elif time_frac <= change_times[11]:
    shutil.copy(PATH + early_night, PATH + CURRENT)

else :
    shutil.copy(PATH + mid_night, PATH + CURRENT)

# set the background image
os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri \"file:///" + PATH + CURRENT + "\"")
# alert the user that the background has been changed
print("Wallpaper changed.")
{% endcodeblock %}


The last step is to to use cron, a Linux utility for scheduling jobs to run. To edit the cron tab(le) for your user simply open up the Unix terminal and enter
{% codeblock lang:Bash %}
crontab -e
{% endcodeblock %}


This will open the cron tab(le) and you can enter the following two lines, replacing the place-holders with the relevant paths, at the bottom of the editor

{% codeblock %}
*/5 * * * * PATH_TO_PYTHON_INSTALLATION PATH_TO_WALLPAPER_CHANGING_SCRIPT
@reboot PATH_TO_WALLPAPER_CHANGING_SCRIPT
{% endcodeblock %}


Don't forget to leave a new line after these new entries else they will fail to interpretted. If you are unsure of the location of your Python installation, running `which python` in the terminal should give you the required path. The first line is used to rerun the wallpaper-updating script every 5 minutes and the second, unsurprisingly, runs it whenever the computer reboots.

If all has gone to plan, you should now have your own sun-tracking, live, 8-bit desktop wallpaper.
