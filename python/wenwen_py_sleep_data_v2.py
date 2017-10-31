# -*- coding:utf-8 -*-
import re
import os
import time

file_name="main_wakeup_mic"
line_pattern = re.compile(r' ')
time_pattern = re.compile(r'[:.]')
date_pattern = re.compile(r'-')
sleep_flag = 0
max_time_interval = 0
max_wakeup_cnt = 0
total_time_interval = 0

with open(file_name, "r") as input_file:
    for line in input_file:
#        print line.strip()
        split = line_pattern.split(line.strip())
        date = split[0]
        time = split[1]
        mute_flag = int(split[16][0], 10)
        wakeup_cnt = int(split[18], 10)
#        print "date:" + date
#        print "time:" + time
#        print "mute_flag:" + str(mute_flag)
#        print "wakeup_cnt:" + str(wakeup_cnt)
        if max_wakeup_cnt < wakeup_cnt:
            max_wakeup_cnt = wakeup_cnt
        if mute_flag == 3 :
            split_time = time_pattern.split(time)
#            print split_time
            split_date = date_pattern.split(date)
#            print split_date
            last_time = int(split_time[2]) 
            last_time += int(split_time[1]) * 60 # minute
            last_time += int(split_time[0]) * 3600  # hour
            last_time += int(split_date[1]) * 24 * 3600  # date
            last_wakeup_cnt = wakeup_cnt
            last_time_str = time
            if sleep_flag == 1:
                print "ERR: wakeuping cannot find after sleeping"
                print line.strip()
            sleep_flag = 1
        if sleep_flag == 1 and wakeup_cnt == last_wakeup_cnt + 1:
            split_time = time_pattern.split(time)
#            print split_time
            split_date = date_pattern.split(date)
#            print split_date
            this_time = int(split_time[2]) 
            this_time += int(split_time[1]) * 60 # minute
            this_time += int(split_time[0]) * 3600  # hour
            this_time += int(split_date[1]) * 24 * 3600  # date
            this_time_str = time
            time_interval = this_time - last_time
            total_time_interval += time_interval
            print " --% 2d-- date: %s, start: %s -- end: %s, %dh%dm%s"%(wakeup_cnt, date, last_time_str, this_time_str, time_interval/3600, (time_interval%3600)/60, time_interval%60)
            print "       total: %dh%dm%s"%(total_time_interval/3600, (total_time_interval%3600)/60, total_time_interval%60)
            sleep_flag = 0
            if time_interval > max_time_interval:
                max_time_interval = time_interval
#            print "     " + line.strip()


print "max_time_interval: %dh%dm%s"%(max_time_interval/3600, (max_time_interval%3600)/60, max_time_interval%60)
print "total_time_interval: %dh%dm%s"%(total_time_interval/3600, (total_time_interval%3600)/60, total_time_interval%60)
print "max_wakeup_cnt: %d"%(max_wakeup_cnt) 
