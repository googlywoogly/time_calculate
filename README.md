################
# About script #
################

Python script identifies the time difference between two timestamps; considering only business hours, excluding any given holidays nd weekend.

For an instance, let say my working or business hours are from 08:00 AM to 05:00 PM. If a ticket opened at 11:00 AM and closed at 02:00 PM, then time to resolve a ticket is 3 hours or 180 minutes.

02:00 PM - 11:00 PM = 3 hours or 180 minutes

Another example is, let say ticket opened at 11:00 AM on Monday and closed on 02:00 PM on Wednesday. Since my working or business hours are from 08:00 AM to 05:00 PM. Time to resolve this ticket would be

#####################################################################################################
# Opened at Monday    #	11:00 AM    #	Day 1  # 	05:00 PM – 11:00 AM          #	360 minutes #
#---------------------------------------------------------------------------------------------------#
# Tuesday	      #	            #   Day2   #	Whole day will be consider   #	540 minutes #
#---------------------------------------------------------------------------------------------------#
# Closed on Wednesday #	02:00 PM    #	Day3   #	02:00 PM – 08:00 AM	     #  360 minutes #
#---------------------------------------------------------------------------------------------------#
#		      #	            #          #         Total time to solve ticket  #	1260 minutes#
#####################################################################################################


Script will also exclude weekend like Saturday, Sunday and exclude any given holidays. For instance, ticket opened at 11:00 AM on Friday and closed on 02:00 PM on Tuesday. Let say Monday is a given holiday and Saturday, Sunday will be exclude from time calculation and Time to resolve this ticket would be

#############################################################################################################
# Opened at Friday    #	11:00 AM    #	Day 1  # 	05:00 PM – 11:00 AM               #	360 minutes #
#-----------------------------------------------------------------------------------------------------------#
# Saturday	      #	            #   Day2   #	Weekend, don’t need to consider   #	  0 minutes #
#-----------------------------------------------------------------------------------------------------------#
# Sunday 	      #	            #   Day3   #	Weekend, don’t need to consider   #	  0 minutes #
#-----------------------------------------------------------------------------------------------------------#
# Monday 	      #	            #   Day4   #	Holiday, don’t need to consider   #	  0 minutes #
#-----------------------------------------------------------------------------------------------------------#
# Closed on Tuesday   #	02:00 PM    #	Day5   #	02:00 PM – 08:00 AM	          #     360 minutes #
#-----------------------------------------------------------------------------------------------------------#
#		      #	            #          #         Total time to solve ticket       #	720 minutes #
#############################################################################################################


##########################
# How to use this script #
##########################

  1.	Download python script in directory; let say /tmp/calculate_time
  2.	Create a file with name holiday.csv at location.  /tmp/calculate_time/holiday.csv
  	    Define your holidays in this file in following format
        
                mm/dd/yyyy, holiday_name

        Example:
                08/12/2019, holiday1
  3.	Use the script as following
            Syntax:
                ./calculate_ticket_business_hours.py --start_date=mm/dd/yyyy --start_time=HH:MM --stop_date=mm/dd/yyyy --stop_time=HH:MM

            Example:
                ./calculate_ticket_business_hours.py --start_date=08/05/2019 --start_time=09:00 --stop_date=08/05/2019 --stop_time=11:30

            Output:
                Total time taken to resolve ticket is 150 minutes
