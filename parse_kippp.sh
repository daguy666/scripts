#!/bin/bash
#------------------------------------------------------------------------------------
# I finally got fed up running each of these commands one by one. 
# I basically copied my bash history for each command I wanted to run. 
# This makes the following assumptions: 
# 1) You have all of your kippo logs merged into one file named k.log 
# 2) That all log files are the same. 
# I am using https://github.com/desaster/kippo
# ===================================================================================
# When I gather my logs together I run 
# ~/kippo/log: $  cat kippo.log.* > k.log 
# Then start going from there.  
#------------------------------------------------------------------------------------




cat << "EOF"
 ____  __.__                    __________                             
|    |/ _|__|_____ ______   ____\______   \_____ _______  ______ ____  
|      < |  \____ \\____ \ /  _ \|     ___/\__  \\_  __ \/  ___// __ \ 
|    |  \|  |  |_> >  |_> >  <_> )    |     / __ \|  | \/\___ \\  ___/ 
|____|__ \__|   __/|   __/ \____/|____|    (____  /__|  /____  >\___  >
        \/  |__|   |__|                         \/           \/     \/ 
Breaking down kippo logs. This might take a minuite ... 

EOF

mkdir -p output_files/

# Getting all commands both fonud and not found.
cat k.log | grep -in "Command not found"  > output_files/cmd_not_found
cat k.log | grep -in "Command found"  > output_files/cmd_found

# Grabbing all the passwords out of the file including dupes.
cat k.log | grep "login attempt" | awk '{ print $9 }' | sed -e 's/^.//g' -e 's/.$//g' | awk -F / '{print $2}' > output_files/all_passwords_dupes
# Grabbing all the username out of the file including dupes.
cat k.log | grep "login attempt" | awk '{ print $9 }' | sed -e 's/^.//g' -e 's/.$//g' | awk -F / '{print $1}' > output_files/all_username_dupes
# Grabbing all passwords with out dupes
cat k.log | grep "login attempt" | awk '{ print $9 }' | sed -e 's/^.//g' -e 's/.$//g' | awk -F / '{print $2}' | sort -u > output_files/all_passwords_no_dupes
# Getting all usernames with out dupes
cat k.log | grep "login attempt" | awk '{ print $9 }' | sed -e 's/^.//g' -e 's/.$//g' | awk -F / '{print $2}' | sort -u > output_files/all_passwords_no_dupes

# This will grab every ip from the entire log file 
cat k.log | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' > output_files/all_ip_addresses_dupes
# Gets all unique ips from the entire log file
cat k.log | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | sort -u > output_files/all_ip_addresses_no_dupes

# Attacker IP + Destination url for malware.
cat k.log | grep -i "CMD: wget" | awk -F , '{print "[>] Attacker_IP: " $3 }' | sed 's/] CMD: wget/ ===> Destination:/g' > output_files/wget_attacker_dest
# Get all attacker ips from wget 
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/].*//' > output_files/attacker_ip_dupes
# Get all attacker ips from wget with out dupes
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/].*//'| sort -u > output_files/attacker_ip_no_dupes

# Gets all sites hosting malware with dupes
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/^.*wget //g' | grep 'http:' | sed 's/.*http/http/g' > output_files/sites_hosting_malware_dupes
# Gets all sites hosting malware with out dupes 
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/^.*wget //g' | grep 'http:' | sed 's/.*http/http/g' | sort -u >output_files/sites_hosting_malware_no_dupes

# IP Address that malware is hosted at with dupes
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/^.*wget //g' | grep 'http:' | sed 's/.*http/http/g' | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' > output_files/malicious_ip_dupes
# IP Address that malware is hosted at no dupes
cat k.log | grep -i "CMD: wget" | awk -F , '{print  $3 }' | sed 's/^.*wget //g' | grep 'http:' | sed 's/.*http/http/g' | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | sort -u > output_files/malicious_ip_no_dupes

# Searches for "Command found" then only prints the command with dupes
cat k.log | grep -i 'command found' | awk -F : '{print $4}' | sed 's/^.//g' > output_files/cmd_found_dupes
# Searches for "Command found" then only prints the command with out dupes
cat k.log | grep -i 'command found' | awk -F : '{print $4}' | sed 's/^.//g' | sort -u > output_files/cmd_found_no_dupes

# Searches for "Command not found" then only prints the command with dupes
cat k.log | grep -i 'command not found' | awk -F : '{print $4}' | sed 's/^.//g' > output_files/cmd_not_found_dupes
# Searches for "Command not found" then only prints the command without dupes
cat k.log | grep -i 'command not found' | awk -F : '{print $4}' | sed 's/^.//g' | sort -u > output_files/cmd_not_found_no_dupes

# SSH successful logins with dupes 
cat k.log | grep -i "login attempt" | grep -v failed | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' > output_files/ssh_successful_logins_dupes
# SSH successful logins with out dupes
cat k.log | grep -i "login attempt" | grep -v failed | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'| sort -u > output_files/ssh_successful_logins_no_dupes

# SSH failed logins with dupes
cat k.log | grep -i "login attempt" | grep -v succeeded | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' > output_files/ssh_failed_logins_dupes

# SSH failed logins with out dupes
cat k.log | grep -i "login attempt" | grep -v succeeded | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | sort -u > output_files/ssh_failed_logins_no_dupes
