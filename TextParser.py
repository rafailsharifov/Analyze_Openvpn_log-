from datetime import datetime
from dateutil.parser import *
from dateutil.relativedelta import *
import os
import yaml
from Send_email import if_error_occured #Send_email.py is another script file that sends email

try:
    def parse_file(): #Read log file and find last one weeks connection restarted and initiated logs

        log_file = open("/root/log_files/openvpn.log", 'r', errors='replace') #Read log file
        sorted_by_date = open("/root/log_files/Sorted_by_date.txt", 'w') #creat output file sorted by date
        sorted_by_ATM = open("/root/log_files/Sorted_by_Client_name.txt", 'w') #creat output file sorted by VPN client name
        a_week_ago = datetime.today() - relativedelta(weeks=1)  #find date that is a week ago

        sort1_list = []
        row_dict = {}
        date_dict = {}
        time_dict = {}
        atm_name = {}
        new_row_dict ={}
        dict1 = {}
        dict2 = {}
        atm_name1 = ""

        number =0
        for line in log_file: #Parse log file

            split_columbs = line.split()
            log_date = ' '.join([str(element) for element in split_columbs[:3]])

            try:
                log_date_parsed = parse(log_date)

                if log_date_parsed.month > datetime.today().month: #If it is Januar and December`s log file read, script believe that it was last year log
                    log_date_parsed = log_date_parsed - relativedelta(years= 1)
                else: pass

            except :
                continue


            if log_date_parsed > a_week_ago: # Finds last week`s logs
                try:
                    row_in_log = ' '.join([str(element) for element in split_columbs[6:10] ])

                except :
                    continue


                if 'timeout' in row_in_log: #finds connection restarted
                    number += 1
                    row_dict [number] = log_date +" " + row_in_log.replace(' (--ping-restart),', '')
                    date_dict[number] = log_date_parsed

                    time_dict[number] = log_date
                    new_row_dict [number] = "Inactivity timeout"
                    atm_name [number] = split_columbs[6]


                elif 'Initiated' in row_in_log: #finds connection initiated
                    number += 1
                    row_dict [number] = log_date +" " + row_in_log
                    date_dict[number] = log_date_parsed

                    time_dict[number] = log_date
                    new_row_dict [number] = "Peer Connection Initiated"
                    atm_name [number] = split_columbs[6]

                else: continue
            else: continue


        sort1_list = sorted(date_dict.items(), key=lambda x: x[1]) #sorts by date
        for key in sort1_list: #for number in row, append line from log file
            last_result = row_dict [key[0]]
            sorted_by_date.write(last_result + '\n') #Write to a file


        sort2_list = sorted(atm_name.items(), key=lambda x: x[1]) #Sorts by name of VPN client
        for key in sort2_list: #for number in row, append Vpn client name and status

            if key[1] in  dict2.keys(): #Checks if client name is in list, else append client name to list
                dict1[time_dict[key[0]]] = new_row_dict[key[0]]
                dict2[atm_name[key[0]]] = dict1
            else:
                dict1 = {}
                dict1[time_dict[key[0]]] = new_row_dict[key[0]]
                dict2[atm_name[key[0]]] = dict1

        yaml.dump(dict2, sorted_by_Client_name, allow_unicode=True, sort_keys=False) #Write to a file as tree form



        log_file.close()
        sorted_by_date.close()
        sorted_by_Client_name.close()

        if_error_occured(got_error=False, error='') #calls mail sender script


    if __name__ == "__main__": #When TextParser.py called, runs ssh_connect() define
        parse_file()

except Exception as error:
    # If error happens in code above, script calls if_error_occured define and that sends email to me
    got_error = True
    if_error_occured(got_error, error)







