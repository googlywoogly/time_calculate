#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import calendar
import csv
import sys
import getopt

############################################################
def get_start_and_stop_date():
    global start_date
    global start_time
    global stop_date
    global stop_time
    global holiday_file
    global weekoff_day1
    global weekoff_day2
    start_date = None
    start_time = None
    stop_date = None
    stop_time = None
    holiday_file = None
    weekoff_day1 = None
    weekoff_day2 = None

    argv = sys.argv[1:]
    #print(argv)

    try:
        opts, args = getopt.getopt(argv, 's:t:e:m:f:w:d:h', ["start_date=", "start_time=", "stop_date=", "stop_time=", "holiday_file=", "weekend1=", "weekend2=", "help"])
    except getopt.GetoptError as error:
        print(error)
        print "Invalid syntax."
        print "\nTry",sys.argv[0],"--help for more information."
        opts = []
        sys.exit(1)

    for opt, arg in opts:
        if opt in ['-s', '--start_date']:
            start_date = arg
        elif opt in ['-t', '--start_time']:
            start_time = arg
        elif opt in ['-e', '--stop_date']:
            stop_date = arg
        elif opt in ['-m', '--stop_time']:
            stop_time = arg
        elif opt in ['-f', '--holiday_file']:
            holiday_file = arg
        elif opt in ['-w', '--weekend1']:
            weekoff_day1 = arg
        elif opt in ['-d', '--weekend2']:
            weekoff_day2 = arg
        elif opt in ['-h', '--help']:
            print "\nCalculate business hours between two timestamps.\n"
            print "Syntax:\n ",sys.argv[0],"--start_date=mm/dd/yyyy --start_time=HH:MM --stop_date=mm/dd/yyyy --stop_time=HH:MM --holiday_file=filename --weekend1=day_of_week --weekend2=day_of_week\n"
            print "Example:\n ",sys.argv[0],"--start_date=08/05/2019 --start_time=09:00 --stop_date=08/09/2019 --stop_time=16:30 --holiday_file=holidays.csv --weekend1=Saturday --weekend2=Sunday"
            sys.exit(0)

    if start_date == None or start_time == None or stop_date == None or stop_time == None:
        print "Invalid syntax."
        print "\nTry",sys.argv[0],"--help for more information."
        sys.exit(1)
############################################################

############################################################
def same_day_time_calculation():
    day_count_time = 0
    day = calendar.day_name[ticket_start_date.weekday()]
    if day == weekoff_day1 or day == weekoff_day2:
        #print "This ticket open and close on",day,",so doesn't need to calulate time"
        ticket_start_day_weekoff = 1
    else:
        ticket_start_day_weekoff = 0

    ticket_start_day_holiday = 0
    holidays = csv.reader(open('holidays.csv'), delimiter=',')
    for row in holidays:
        if start_date == row[0]:
            #print "This ticket open and close on",row[0],"It is a holiday, so doesn't need to calulate time"
            ticket_start_day_holiday = 1

    if ticket_start_day_weekoff == 1 or ticket_start_day_holiday == 1:
        #print ticket_start_date,"Exclude from time calculation. It is either Weekoff or holiday"
        day_count_time = 0
    else:
        if ticket_start_timestamp < start_day_start_timestamp and ticket_start_timestamp < start_day_stop_timestamp:
            #print "use case 1"
            if ticket_stop_timestamp <= start_day_start_timestamp:
                day_count_time = 0
            elif ticket_stop_timestamp > start_day_start_timestamp and ticket_stop_timestamp <= start_day_stop_timestamp:
                day_count_time = ticket_stop_timestamp - start_day_start_timestamp
                day_count_time = day_count_time.seconds / 60
            elif ticket_stop_timestamp > start_day_stop_timestamp:
                day_count_time = start_day_stop_timestamp - start_day_start_timestamp
                day_count_time = day_count_time.seconds / 60 
            else:
                print "Time calculation is required for this use case - 1"
        elif ticket_start_timestamp >= start_day_start_timestamp and ticket_start_timestamp < start_day_stop_timestamp:
            #print "use case 2"
            if ticket_stop_timestamp <= start_day_stop_timestamp:
                day_count_time = ticket_stop_timestamp - ticket_start_timestamp
                day_count_time = day_count_time.seconds / 60
            elif ticket_stop_timestamp > start_day_stop_timestamp:
                day_count_time = start_day_stop_timestamp - ticket_start_timestamp
                day_count_time = day_count_time.seconds / 60
            else:
                print "Time calculation is required for this use case - 2"
        elif ticket_start_timestamp >= start_day_stop_timestamp:
            #print "use case 3"
            if ticket_stop_timestamp >= start_day_stop_timestamp:
                day_count_time = 0
            else: 
                print "Time calculation is required for this use case - 3"
        else:
            print "Time calculation is required for this use case"

    return day_count_time
############################################################
    
############################################################
def start_day_time_calculation():
    start_day_count_time = 0
    ticket_start_date_day = calendar.day_name[ticket_start_date.weekday()]
    if ticket_start_date_day == weekoff_day1 or ticket_start_date_day == weekoff_day2:
        #print "Since it is",ticket_start_date_day,"Exclude this day from time calculation"
        ticket_start_day_weekoff = 1
    else:
        ticket_start_day_weekoff = 0

    ticket_start_day_holiday = 0
    holidays = csv.reader(open('holidays.csv'), delimiter=',')
    for row in holidays:
        if start_date == row[0]:
            #print "This ticket open on",row[0],"It is a holiday, so doesn't need to calulate ticket start day time"
            ticket_start_day_holiday = 1

    if ticket_start_day_weekoff == 1 or ticket_start_day_holiday == 1:
        #print ticket_start_date,"Exclude from time calculation. It is either Weekoff or holiday"
        start_day_count_time = 0
    else:
        if ticket_start_timestamp <= start_day_start_timestamp and ticket_start_timestamp < start_day_stop_timestamp:
            start_day_count_time = start_day_stop_timestamp - start_day_start_timestamp
            start_day_count_time = start_day_count_time.seconds / 60
            #print ticket_start_date,"Start day time calculation is",start_day_count_time
        elif ticket_start_timestamp > start_day_start_timestamp and ticket_start_timestamp < start_day_stop_timestamp:
            start_day_count_time = start_day_stop_timestamp - ticket_start_timestamp
            start_day_count_time = start_day_count_time.seconds / 60
            #print ticket_start_date,"Start day time calculation is",start_day_count_time
        elif ticket_start_timestamp > start_day_start_timestamp and ticket_start_timestamp >= start_day_stop_timestamp:
            start_day_count_time = 0
            #print ticket_start_date,"Start day time calculation is",start_day_count_time
        else:
            print "Time calculation is required for this use case (Start Day)"
    return start_day_count_time
############################################################

############################################################
def stop_day_time_calculation():
    stop_day_count_time = 0
    ticket_stop_date_day = calendar.day_name[ticket_stop_date.weekday()]
    if ticket_stop_date_day == weekoff_day1 or ticket_stop_date_day == weekoff_day2:
        #print "Since it is",ticket_stop_date_day,"Exclude this day from time calculation"
        ticket_stop_day_weekoff = 1
    else:
        ticket_stop_day_weekoff = 0

    ticket_stop_day_holiday = 0
    holidays = csv.reader(open('holidays.csv'), delimiter=',')
    for row in holidays:
        if stop_date == row[0]:
            #print "This ticket open on",row[0],"It is a holiday, so doesn't need to calulate ticket stop day time"
            ticket_stop_day_holiday = 1

    if ticket_stop_day_weekoff == 1 or ticket_stop_day_holiday == 1:
        #print ticket_stop_date,"Exclude from time calculation. It is either Weekoff or holiday"
        stop_day_count_time = 0
    else:
        if ticket_stop_timestamp <= stop_day_start_timestamp and ticket_stop_timestamp < stop_day_stop_timestamp:
            stop_day_count_time = 0
            #print ticket_stop_date,"Stop day time calculation is",stop_day_count_time
        elif ticket_stop_timestamp > stop_day_start_timestamp and ticket_stop_timestamp < stop_day_stop_timestamp:
            stop_day_count_time = ticket_stop_timestamp - stop_day_start_timestamp
            stop_day_count_time = stop_day_count_time.seconds / 60
            #print ticket_stop_date,"Start day time calculation is",stop_day_count_time
        elif ticket_stop_timestamp > stop_day_start_timestamp and ticket_stop_timestamp >= stop_day_stop_timestamp:
            stop_day_count_time = stop_day_stop_timestamp - stop_day_start_timestamp
            stop_day_count_time = stop_day_count_time.seconds / 60
            #print ticket_stop_date,"Start day time calculation is",stop_day_count_time
        else:
            print "Time calculation is required for this use case (Stop Day)"
    return stop_day_count_time
############################################################

############################################################
def between_start_stop_date():
    start_date_00 = datetime.strptime(start_date, date_format)
    stop_date_00 = datetime.strptime(stop_date, date_format)
    between_days_count_time = 0
    while start_date_00 < stop_date_00:
        start_date_00 = start_date_00 + timedelta(days=1)
        if start_date_00 != stop_date_00:
            start_date_00_day = calendar.day_name[start_date_00.weekday()]
            if start_date_00_day  == weekoff_day1 or start_date_00_day == weekoff_day2:
                #print start_date_00,"Since it is weekoff exclude this day from time calculation"
                start_date_00_day_weekoff = 1
            else:
                start_date_00_day_weekoff = 0

            start_date_00_holiday = 0
            holidays = csv.reader(open('holidays.csv'), delimiter=',')
            for row in holidays:
                if start_date_00 == datetime.strptime(row[0], date_format):
                    start_date_00_holiday = 1
                    #print start_date_00,"Since it is a Holiday exclude this day from time calculation"

            if start_date_00_day_weekoff == 1 or start_date_00_holiday == 1:
                #print start_date_00,"Exclude from time calculation. It is either Weekoff or holiday"
                day_time_count = 0
            else:
                day_time_count = start_day_stop_timestamp - start_day_start_timestamp
                day_time_count = day_time_count.seconds / 60
                #print start_date_00,"Consider for time calculation --",day_time_count
            between_days_count_time = between_days_count_time + day_time_count

    #print "Between days time calculation is:",between_days_count_time
    return between_days_count_time
############################################################

get_start_and_stop_date()

weekoff_day1='Saturday'
weekoff_day2='Sunday'

date_format='%m/%d/%Y'
timestamp_format='%m/%d/%Y %H:%M'

day_start_time='08:00'
day_stop_time='17:00'

start_day_start_timestamp = datetime.strptime(start_date + " " + day_start_time, timestamp_format)
start_day_stop_timestamp = datetime.strptime(start_date + " " + day_stop_time, timestamp_format)

stop_day_start_timestamp = datetime.strptime(stop_date + " " + day_start_time, timestamp_format)
stop_day_stop_timestamp = datetime.strptime(stop_date + " " + day_stop_time, timestamp_format)

ticket_start_date = datetime.strptime(start_date, date_format)
ticket_stop_date = datetime.strptime(stop_date, date_format)

ticket_start_timestamp = datetime.strptime(start_date + " " + start_time, timestamp_format)
ticket_stop_timestamp = datetime.strptime(stop_date + " " + stop_time, timestamp_format)

if datetime.strptime(start_date, date_format) == datetime.strptime(stop_date, date_format):
    total_time = same_day_time_calculation()
    print "Total time taken to resolve ticket is",total_time,"minutes"
else:
    total_time = start_day_time_calculation() + between_start_stop_date() + stop_day_time_calculation()
    print "Total time taken to resolve ticket is",total_time,"minutes."
